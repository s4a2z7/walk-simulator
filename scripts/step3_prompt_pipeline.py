#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3 - 통합 파이프라인(요약/키워드/분류) 실행 스크립트

목적:
- Step2 전처리 결과(out/step2_preprocessed.csv)를 입력으로 받아
  1) review_summary (리뷰에 한해)
  2) dialog_summary (inquiry에 한해, 단일 발화를 "U:"로 구성)
  3) keyword_extraction (모든 텍스트)
  4) text_classification (옵션)
  을 하나의 스크립트로 실행하고 out/에 저장한다.

주의:
- OPENAI_API_KEY가 없으면 dry-run으로 프롬프트 렌더링만 저장한다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from dotenv import load_dotenv

try:
    from openai import OpenAI  # type: ignore
    from openai import RateLimitError  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore
    RateLimitError = Exception  # type: ignore


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out"
PROMPTS_DIR = ROOT / "prompts"

P_REVIEW = PROMPTS_DIR / "step3_review_summary.md"
P_DIALOG = PROMPTS_DIR / "step3_dialog_summary.md"
P_KEYWORDS = PROMPTS_DIR / "step3_keyword_extraction.md"
P_CLASSIFY = PROMPTS_DIR / "step3_text_classification.md"


KEYWORD_STOPWORDS = {
    # 프롬프트에서 명시한 일반어 + 파이프라인에서 자주 섞이는 일반어
    "합니다",
    "있습니다",
    "가능",
    "가능한",
    "가능함",
    "여부",
    "문의",
    "확인",
    "진행",
    "방법",
    "대상",
    "정보",
    "관련",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _split_prompt(md: str) -> tuple[str, str]:
    if "## System" not in md or "## User" not in md:
        raise ValueError("prompt format must include '## System' and '## User'")
    sys_part = md.split("## System", 1)[1].split("## User", 1)[0].strip()
    user_part = md.split("## User", 1)[1].strip()
    return sys_part, user_part


def _render(s: str, **kwargs: Any) -> str:
    for k, v in kwargs.items():
        s = s.replace("{{" + k + "}}", str(v))
    return s


def _call_openai(client: Any, model: str, system: str, user: str, temperature: float) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()


def _safe_call_openai(
    client: Any, model: str, system: str, user: str, temperature: float
) -> tuple[str, str | None]:
    """
    API 호출 실패(쿼터/네트워크 등)로 스크립트가 중단되지 않도록 보호.
    반환: (raw_output, error_message_or_None)
    """
    try:
        return _call_openai(client, model, system, user, temperature), None
    except RateLimitError as e:
        return f"(error) RateLimitError: {e}", str(e)
    except Exception as e:
        return f"(error) {type(e).__name__}: {e}", str(e)


def _extract_json(s: str) -> Optional[Any]:
    """
    모델이 코드펜스/부가 텍스트를 섞는 경우를 대비해 JSON object/array만 최대한 추출한다.
    - 1) 그대로 json.loads 시도
    - 2) ```json ... ``` 제거 후 재시도
    - 3) 첫 '{'~마지막 '}' 구간 / 첫 '['~마지막 ']' 구간으로 재시도
    """
    s = (s or "").strip()
    if not s:
        return None

    def _try(x: str) -> Optional[Any]:
        try:
            return json.loads(x)
        except Exception:
            return None

    parsed = _try(s)
    if parsed is not None:
        return parsed

    # remove code fences
    if "```" in s:
        cleaned = []
        in_fence = False
        for line in s.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                cleaned.append(line)
        parsed = _try("\n".join(cleaned).strip())
        if parsed is not None:
            return parsed

    # object span
    if "{" in s and "}" in s:
        span = s[s.find("{") : s.rfind("}") + 1]
        parsed = _try(span)
        if parsed is not None:
            return parsed

    # array span
    if "[" in s and "]" in s:
        span = s[s.find("[") : s.rfind("]") + 1]
        parsed = _try(span)
        if parsed is not None:
            return parsed

    return None


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _tokenize_ko(text: str) -> list[str]:
    """
    매우 가벼운 토큰화(외부 라이브러리 없이):
    - 한글/영문/숫자 연속 덩어리 단위로 추출
    """
    return re.findall(r"[0-9A-Za-z가-힣]+", (text or "").strip())


def _strip_common_suffixes(token: str) -> str:
    """
    입력 기반 보충 시 '접수부터'처럼 조사가 붙은 토큰이 생기는 것을 완화.
    (완전한 형태소 분석은 아니며, 보수적으로 흔한 접미만 제거)
    """
    token = (token or "").strip()
    if not token:
        return token

    suffixes = [
        "부터",
        "까지",
        "으로",
        "로",
        "에서",
        "에게",
        "한테",
        "만",
        "도",
        "은",
        "는",
        "이",
        "가",
        "을",
        "를",
        "과",
        "와",
    ]
    for suf in suffixes:
        if token.endswith(suf) and len(token) > len(suf) + 1:
            return token[: -len(suf)]
    return token


def _postprocess_keywords(
    text: str,
    keywords_from_model: Optional[list[str]],
    min_k: int = 5,
    max_k: int = 10,
) -> dict[str, Any]:
    """
    키워드 자동 정제:
    - 일반어(불용어) 제거
    - 공백/빈문자 제거 + 중복 제거
    - min_k 미만이면 입력(text) 기반으로 보충(토큰/2-그램)
    """
    before = [str(x).strip() for x in (keywords_from_model or []) if str(x).strip()]
    before = _dedupe_keep_order(before)

    removed_stopwords: list[str] = []
    cleaned: list[str] = []
    for k in before:
        if k in KEYWORD_STOPWORDS:
            removed_stopwords.append(k)
            continue
        cleaned.append(k)
    cleaned = _dedupe_keep_order(cleaned)

    fill_added: list[str] = []
    if len(cleaned) < min_k:
        toks = [_strip_common_suffixes(t) for t in _tokenize_ko(text)]
        toks = [t for t in toks if t]
        # 1) 단일 토큰 후보
        candidates: list[str] = []
        for t in toks:
            t = t.strip()
            if not t:
                continue
            if t in KEYWORD_STOPWORDS:
                continue
            candidates.append(t)

        # 2) 인접 2-그램 후보(입력 기반 재조합)
        bigrams: list[str] = []
        for a, b in zip(toks, toks[1:]):
            a = a.strip()
            b = b.strip()
            if not a or not b:
                continue
            if a in KEYWORD_STOPWORDS or b in KEYWORD_STOPWORDS:
                continue
            bigrams.append(f"{a} {b}")

        candidates = _dedupe_keep_order(candidates + bigrams)

        for c in candidates:
            if len(cleaned) >= min_k:
                break
            if c in cleaned:
                continue
            cleaned.append(c)
            fill_added.append(c)

    # 상한 적용
    cleaned = cleaned[:max_k]

    return {
        "keywords_before": before,
        "keywords_after": cleaned,
        "removed_stopwords": removed_stopwords,
        "filled_from_input": fill_added,
        "min_k": min_k,
        "max_k": max_k,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input_csv", default=str(OUT_DIR / "step2_preprocessed.csv"), help="input preprocessed csv")
    p.add_argument("--n", type=int, default=12, help="샘플 실행 건수(소량 테스트용)")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI model id")
    p.add_argument("--temperature", type=float, default=0.2, help="LLM temperature")
    p.add_argument("--enable_classification", action="store_true", help="텍스트 분류 단계 실행")
    p.add_argument("--out_jsonl", default=str(OUT_DIR / "step3_pipeline_results.jsonl"), help="output jsonl log")
    p.add_argument("--out_md", default=str(OUT_DIR / "step3_pipeline_samples.md"), help="output markdown samples")
    args = p.parse_args()

    load_dotenv(ROOT / ".env")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    input_csv = Path(args.input_csv)
    out_jsonl = Path(args.out_jsonl)
    out_md = Path(args.out_md)

    df = pd.read_csv(input_csv)
    if "text" not in df.columns:
        raise ValueError("missing column: text")

    n = max(3, int(args.n))

    # 소량 통합 테스트는 source_type이 섞이도록 샘플링(가능하면)
    pieces = []
    for st in ["review", "inquiry", "faq", "notice", "dataset"]:
        sub = df[df.get("source_type", "").astype(str) == st].head(max(1, n // 5))
        if len(sub) > 0:
            pieces.append(sub)
    if pieces:
        sample_df = pd.concat(pieces, ignore_index=True).head(n)
    else:
        sample_df = df.head(n).copy()

    # 프롬프트 로드
    review_sys, review_user = _split_prompt(_read_text(P_REVIEW))
    dialog_sys, dialog_user = _split_prompt(_read_text(P_DIALOG))
    kw_sys, kw_user = _split_prompt(_read_text(P_KEYWORDS))
    classify_sys, classify_user = ("", "")
    if args.enable_classification:
        classify_sys, classify_user = _split_prompt(_read_text(P_CLASSIFY))

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    dry_run = not api_key
    api_state: dict[str, str | None] = {"blocked_reason": None}
    client = None
    if not dry_run:
        if OpenAI is None:
            raise RuntimeError("openai 패키지를 불러올 수 없습니다. requirements.txt 설치를 확인하세요.")
        client = OpenAI()

    now = datetime.now(timezone.utc).isoformat()

    # writer
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    f_jsonl = out_jsonl.open("w", encoding="utf-8")

    def run_task(task: str, system: str, user_tmpl: str, payload: dict) -> dict:
        user = _render(user_tmpl, **payload)
        raw = ""
        parsed = None
        err = None
        if dry_run:
            raw = "(dry-run) OPENAI_API_KEY가 없어 호출을 생략했습니다."
        elif api_state["blocked_reason"] is not None:
            raw = f"(blocked) {api_state['blocked_reason']}"
        else:
            raw, err = _safe_call_openai(client, args.model, system, user, args.temperature)
            if err is None:
                parsed = _extract_json(raw)
            else:
                # 쿼터 부족이면 이후 호출을 차단(불필요한 반복 실패 방지)
                if "insufficient_quota" in err:
                    api_state["blocked_reason"] = "insufficient_quota (429) — billing/plan 확인 필요"
        return {
            "task": task,
            "payload": payload,
            "rendered": {"system": system, "user": user},
            "raw_output": raw,
            "parsed_json": parsed,
            "error": err,
            "dry_run": dry_run,
            "model": args.model,
            "temperature": args.temperature,
            "generated_at": now,
        }

    # markdown 샘플
    md_lines: list[str] = []
    md_lines.append("# Step 3 — 통합 파이프라인 실행 결과(샘플)")
    md_lines.append("")
    md_lines.append(f"- generated_at(UTC): `{now}`")
    md_lines.append(f"- input: `{input_csv.as_posix()}`")
    md_lines.append(f"- model: `{args.model}`")
    md_lines.append(f"- temperature: `{args.temperature}`")
    md_lines.append(f"- mode: `{'dry-run' if dry_run else 'live'}`")
    md_lines.append(f"- enable_classification: `{bool(args.enable_classification)}`")
    md_lines.append("")

    for idx, r in enumerate(sample_df.itertuples(index=False), start=1):
        text_id = getattr(r, "text_id", f"row_{idx}")
        source_type = str(getattr(r, "source_type", ""))
        provider_type = str(getattr(r, "provider_type", ""))
        text = str(getattr(r, "text", ""))

        rec: dict[str, Any] = {
            "text_id": text_id,
            "source_type_gt": source_type,
            "provider_type_gt": provider_type,
            "text": text,
            "results": {},
        }

        # (옵션) 분류
        if args.enable_classification:
            cls = run_task("text_classification", classify_sys, classify_user, {"text": text})
            rec["results"]["text_classification"] = cls

        # 리뷰 요약
        if source_type == "review":
            s = run_task("review_summary", review_sys, review_user, {"text": text})
            rec["results"]["review_summary"] = s

        # 문의(inquiry)는 단일 발화를 대화 형태로 감싸서 테스트
        if source_type == "inquiry":
            # 상담원 발화가 없으면 "없다"고 단정(환각)하기 쉬우므로,
            # Step3 테스트 러너와 동일하게 '확인 후 안내' 형태의 중립 응답을 넣어 테스트한다.
            dialog = f"U: {text}\nA: (테스트용) 안내드립니다. 관련 정책/가능 시간대를 확인 후 답변드릴게요."
            s = run_task("dialog_summary", dialog_sys, dialog_user, {"dialog": dialog})
            rec["results"]["dialog_summary"] = s

        # 키워드(모든 텍스트)
        k = run_task("keyword_extraction", kw_sys, kw_user, {"text": text})

        # 후처리: 일반어 제거 + 최소 개수 보장
        kw_model = None
        try:
            if isinstance(k.get("parsed_json"), dict):
                kw_model = k["parsed_json"].get("keywords")
        except Exception:
            kw_model = None
        pp = _postprocess_keywords(text=text, keywords_from_model=kw_model, min_k=5, max_k=10)
        k["postprocess"] = pp
        # 파이프라인 최종 산출은 after를 사용(자동화 품질 고정)
        k["final_keywords"] = pp["keywords_after"]

        rec["results"]["keyword_extraction"] = k

        f_jsonl.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # markdown
        md_lines.append(f"## 샘플 {idx} — `{text_id}`")
        md_lines.append("")
        md_lines.append(f"- source_type(gt): `{source_type}` / provider_type(gt): `{provider_type}`")
        md_lines.append("")
        md_lines.append("입력(text):")
        md_lines.append("")
        md_lines.append(f"- {text}")
        md_lines.append("")
        for k_task, v in rec["results"].items():
            md_lines.append(f"### 출력({k_task}) raw")
            md_lines.append("")
            md_lines.append("```json")
            md_lines.append(v.get("raw_output", ""))
            md_lines.append("```")
            md_lines.append("")
            # keyword_extraction은 후처리 결과를 함께 보여준다(최종 파이프라인 산출)
            if k_task == "keyword_extraction" and isinstance(v, dict) and v.get("final_keywords") is not None:
                md_lines.append("### keyword_extraction 최종 키워드(postprocessed)")
                md_lines.append("")
                md_lines.append("```json")
                md_lines.append(json.dumps({"keywords": v.get("final_keywords")}, ensure_ascii=False))
                md_lines.append("```")
                md_lines.append("")

    f_jsonl.close()
    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    print("saved:")
    print(f"- {out_md}")
    print(f"- {out_jsonl}")
    print(f"mode: {'dry-run' if dry_run else 'live'}")


if __name__ == "__main__":
    main()

