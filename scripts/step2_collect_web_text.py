"""
Step 2 - 공식 FAQ/이용안내 페이지 텍스트 수집(robots 준수, 최소 수집)

입력: data/step2_source_urls.csv
출력: data/step2_web_text_raw.csv

주의:
- robots.txt 및 이용약관을 확인하고 허용 범위 내에서만 실행하세요.
- 저장 전/후로 PII(전화/이메일/URL)가 섞일 수 있으니 전처리 규정(v1)의 마스킹을 적용하세요.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests
from bs4 import BeautifulSoup


IN_PATH = Path("data/step2_source_urls.csv")
OUT_PATH = Path("data/step2_web_text_raw.csv")

USER_AGENT = "CareLogAI-Step2Collector/1.0 (+edu; respect robots.txt)"

_RE_MULTI_SPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class SeedRow:
    provider_type: str
    source_type: str
    provider_name: str
    source_url: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_text_id(provider_type: str, source_type: str, source_url: str, text: str) -> str:
    """
    재실행 시에도 id가 크게 흔들리지 않게 URL + 텍스트 해시 기반으로 생성.
    """
    h = hashlib.sha1()
    h.update(provider_type.encode("utf-8"))
    h.update(b"|")
    h.update(source_type.encode("utf-8"))
    h.update(b"|")
    h.update(source_url.encode("utf-8"))
    h.update(b"|")
    h.update(text.strip().encode("utf-8"))
    return "W" + h.hexdigest()[:12]


def _clean_text(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = _RE_MULTI_SPACE.sub(" ", s).strip()
    return s


def _extract_paragraph_texts(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    # 노이즈 태그 제거
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    chunks: list[str] = []
    for tag in soup.find_all(["p", "li", "h1", "h2", "h3", "h4"]):
        t = _clean_text(tag.get_text(" ", strip=True))
        if not t:
            continue
        # 너무 짧은 조각은 제외(문서 구조용 제목/불릿 노이즈 완화)
        if len(t) < 8:
            continue
        chunks.append(t)

    # 중복 제거(순서 유지)
    seen = set()
    out = []
    for c in chunks:
        key = c.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _robot_allowed(url: str, user_agent: str) -> bool:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        # robots.txt 접근 실패 시 보수적으로 차단
        return False

    return bool(rp.can_fetch(user_agent, url))


def _fetch(url: str, timeout_sec: int) -> str:
    resp = requests.get(
        url,
        timeout=timeout_sec,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "ko,en;q=0.8"},
    )
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def _load_seeds(path: Path) -> list[SeedRow]:
    df = pd.read_csv(path).fillna("")
    required = ["provider_type", "source_type", "source_url"]
    for c in required:
        if c not in df.columns:
            raise ValueError(f"missing column in seed file: {c} ({path})")

    seeds: list[SeedRow] = []
    for _, r in df.iterrows():
        url = str(r.get("source_url", "")).strip()
        if not url or url.startswith("#"):
            continue
        seeds.append(
            SeedRow(
                provider_type=str(r.get("provider_type", "")).strip(),
                source_type=str(r.get("source_type", "")).strip(),
                provider_name=str(r.get("provider_name", "")).strip(),
                source_url=url,
            )
        )
    return seeds


def collect(
    seeds: Iterable[SeedRow],
    sleep_sec: float,
    timeout_sec: int,
    max_texts_per_url: int,
    allow_without_robots: bool,
) -> pd.DataFrame:
    rows = []
    fetched_at = _now_iso()

    for s in seeds:
        if not s.source_url.lower().startswith(("http://", "https://")):
            print(f"[skip] invalid url: {s.source_url}")
            continue

        allowed = _robot_allowed(s.source_url, USER_AGENT)
        if not allowed and not allow_without_robots:
            print(f"[skip] robots disallow or robots unavailable: {s.source_url}")
            continue

        try:
            html = _fetch(s.source_url, timeout_sec=timeout_sec)
            texts = _extract_paragraph_texts(html)[:max_texts_per_url]
            if not texts:
                print(f"[warn] extracted 0 texts: {s.source_url}")
            for t in texts:
                rows.append(
                    {
                        "text_id": _stable_text_id(s.provider_type, s.source_type, s.source_url, t),
                        "provider_type": s.provider_type,
                        "source_type": s.source_type,
                        "provider_name": s.provider_name,
                        "source_url": s.source_url,
                        "fetched_at": fetched_at,
                        "text": t,
                    }
                )
        except Exception as e:
            print(f"[error] fetch failed: {s.source_url} err={type(e).__name__}: {e}")

        if sleep_sec > 0:
            time.sleep(sleep_sec)

    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", default=str(IN_PATH), help="seed csv path")
    p.add_argument("--out", dest="out_path", default=str(OUT_PATH), help="output csv path")
    p.add_argument("--sleep", dest="sleep_sec", type=float, default=1.2, help="sleep seconds between requests")
    p.add_argument("--timeout", dest="timeout_sec", type=int, default=20, help="request timeout seconds")
    p.add_argument("--max_texts_per_url", type=int, default=40, help="max extracted chunks per URL")
    p.add_argument(
        "--allow_without_robots",
        action="store_true",
        help="robots.txt 접근 실패 시에도 수집(권장하지 않음)",
    )
    args = p.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seeds = _load_seeds(in_path)
    if not seeds:
        raise ValueError(f"no seeds found in: {in_path}")

    df = collect(
        seeds,
        sleep_sec=args.sleep_sec,
        timeout_sec=args.timeout_sec,
        max_texts_per_url=args.max_texts_per_url,
        allow_without_robots=args.allow_without_robots,
    )
    df.to_csv(out_path, index=False, encoding="utf-8")

    print("saved:")
    print(f"- {out_path} rows={len(df)} urls={len(seeds)}")
    if len(df) == 0:
        print("hint: robots 차단/URL 오류/페이지 구조 차이로 추출 실패했을 수 있어요.")


if __name__ == "__main__":
    main()


