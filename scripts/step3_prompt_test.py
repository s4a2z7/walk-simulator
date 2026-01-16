#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3 - 프롬프트 초안 테스트 러너(샘플)

목적:
- 기능별 프롬프트(리뷰 요약/대화 요약/키워드 추출) 초안을 작은 샘플 데이터로 빠르게 테스트
- 결과 샘플(out/step3_prompt_test_samples.md)과 원본 로그(out/step3_prompt_test_results.jsonl)를 생성

동작:
- OPENAI_API_KEY가 없으면 "dry-run"으로 프롬프트 렌더링만 저장한다.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _split_prompt(md: str) -> tuple[str, str]:
    """
    prompts/*.md는 아래 섹션을 가진다고 가정:
    - "## System" 이후 내용
    - "## User" 이후 내용
    """
    if "## System" not in md or "## User" not in md:
        raise ValueError("prompt format must include '## System' and '## User'")
    sys_part = md.split("## System", 1)[1].split("## User", 1)[0].strip()
    user_part = md.split("## User", 1)[1].strip()
    return sys_part, user_part


def _render(s: str, **kwargs: Any) -> str:
    for k, v in kwargs.items():
        s = s.replace("{{" + k + "}}", str(v))
    return s


def _call_openai(client: Any, model: str, system: str, user: str) -> str:
    # openai>=1.x (chat.completions)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    return (resp.choices[0].message.content or "").strip()


def _safe_call_openai(client: Any, model: str, system: str, user: str) -> tuple[str, str | None]:
    """
    API 호출 실패(쿼터/네트워크 등)로 스크립트가 중단되지 않도록 보호.
    반환: (raw_output, error_message_or_None)
    """
    try:
        return _call_openai(client, model, system, user), None
    except RateLimitError as e:  # quota / rate-limit
        return f"(error) RateLimitError: {e}", str(e)
    except Exception as e:
        return f"(error) {type(e).__name__}: {e}", str(e)


def _try_parse_json(s: str) -> Any:
    try:
        return json.loads(s)
    except Exception:
        return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input_csv", default=str(OUT_DIR / "step2_preprocessed.csv"), help="input preprocessed csv")
    p.add_argument("--n", type=int, default=10, help="sample size")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI model id")
    p.add_argument("--out_md", default=str(OUT_DIR / "step3_prompt_test_samples.md"), help="output markdown")
    p.add_argument("--out_jsonl", default=str(OUT_DIR / "step3_prompt_test_results.jsonl"), help="output jsonl log")
    args = p.parse_args()

    load_dotenv(ROOT / ".env")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    input_csv = Path(args.input_csv)
    out_md = Path(args.out_md)
    out_jsonl = Path(args.out_jsonl)

    df = pd.read_csv(input_csv)
    if "text" not in df.columns:
        raise ValueError("missing column: text")

    # 샘플 추출
    n = max(3, int(args.n))
    reviews = df[df.get("source_type", "").astype(str) == "review"].head(n).copy()
    generic = df.head(n).copy()

    # dialog은 데이터에 없으므로 inquiry 기반으로 "테스트용" 합성
    inquiries = df[df.get("source_type", "").astype(str) == "inquiry"].head(min(n, 5)).copy()
    dialogs: list[str] = []
    for r in inquiries.itertuples(index=False):
        t = getattr(r, "text", "")
        dialogs.append(f"U: {t}\nA: (테스트용) 안내드립니다. 관련 정책/가능 시간대를 확인 후 답변드릴게요.")

    # 프롬프트 로드
    review_sys, review_user = _split_prompt(_read_text(P_REVIEW))
    dialog_sys, dialog_user = _split_prompt(_read_text(P_DIALOG))
    kw_sys, kw_user = _split_prompt(_read_text(P_KEYWORDS))

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    dry_run = not api_key
    api_state: dict[str, str | None] = {"blocked_reason": None}

    client = None
    if not dry_run:
        if OpenAI is None:
            raise RuntimeError("openai 패키지를 불러올 수 없습니다. requirements.txt 설치를 확인하세요.")
        client = OpenAI()

    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = []
    lines.append("# Step 3 — 프롬프트 테스트 결과(샘플)")
    lines.append("")
    lines.append(f"- generated_at(UTC): `{now}`")
    lines.append(f"- input: `{input_csv.as_posix()}`")
    lines.append(f"- model: `{args.model}`")
    lines.append(f"- mode: `{'dry-run' if dry_run else 'live'}`")
    lines.append("")

    # jsonl writer(항상 새로 생성)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    f_jsonl = out_jsonl.open("w", encoding="utf-8")

    def run_one(task: str, system: str, user_tmpl: str, payload: dict) -> dict:
        user = _render(user_tmpl, **payload)
        raw = ""
        parsed = None
        err = None
        if dry_run:
            raw = "(dry-run) OPENAI_API_KEY가 없어 호출을 생략했습니다."
        elif api_state["blocked_reason"] is not None:
            raw = f"(blocked) {api_state['blocked_reason']}"
        else:
            raw, err = _safe_call_openai(client, args.model, system, user)
            parsed = _try_parse_json(raw) if err is None else None
            if err is not None and "insufficient_quota" in err:
                api_state["blocked_reason"] = "insufficient_quota (429) — billing/plan 확인 필요"

        rec = {
            "task": task,
            "payload": payload,
            "rendered": {"system": system, "user": user},
            "raw_output": raw,
            "parsed_json": parsed,
            "error": err,
            "dry_run": dry_run,
            "model": args.model,
            "generated_at": now,
        }
        f_jsonl.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    # 1) 리뷰 요약
    lines.append("## 1) 리뷰 요약(review_summary)")
    for i, r in enumerate(reviews.itertuples(index=False), start=1):
        text = getattr(r, "text", "")
        rec = run_one("review_summary", review_sys, review_user, {"text": text})
        lines.append(f"### 샘플 {i}")
        lines.append("")
        lines.append("입력:")
        lines.append("")
        lines.append(f"- text: {text}")
        lines.append("")
        lines.append("출력(raw):")
        lines.append("")
        lines.append("```json")
        lines.append(rec["raw_output"])
        lines.append("```")
        lines.append("")

    # 2) 대화 요약(합성)
    lines.append("## 2) 대화 요약(dialog_summary) — 테스트용 합성 대화")
    for i, d in enumerate(dialogs, start=1):
        rec = run_one("dialog_summary", dialog_sys, dialog_user, {"dialog": d})
        lines.append(f"### 샘플 {i}")
        lines.append("")
        lines.append("입력(dialog):")
        lines.append("")
        lines.append("```")
        lines.append(d)
        lines.append("```")
        lines.append("")
        lines.append("출력(raw):")
        lines.append("")
        lines.append("```json")
        lines.append(rec["raw_output"])
        lines.append("```")
        lines.append("")

    # 3) 키워드 추출
    lines.append("## 3) 키워드 추출(keyword_extraction)")
    for i, r in enumerate(generic.itertuples(index=False), start=1):
        text = getattr(r, "text", "")
        rec = run_one("keyword_extraction", kw_sys, kw_user, {"text": text})
        lines.append(f"### 샘플 {i}")
        lines.append("")
        lines.append("입력:")
        lines.append("")
        lines.append(f"- text: {text}")
        lines.append("")
        lines.append("출력(raw):")
        lines.append("")
        lines.append("```json")
        lines.append(rec["raw_output"])
        lines.append("```")
        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    f_jsonl.close()
    print("saved:")
    print(f"- {out_md}")
    print(f"- {out_jsonl}")
    print(f"mode: {'dry-run' if dry_run else 'live'}")


if __name__ == "__main__":
    main()

