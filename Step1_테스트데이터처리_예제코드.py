"""
Step 1 - 테스트 데이터 처리 예제 코드

목표:
- (예시) 의료업체(Provider) CSV를 읽고
- 필수 필드 검증
- 중복 제거(전화번호 우선, 없으면 이름+주소 기반)
- 정제 결과를 CSV로 저장

주의:
- API 키는 코드에 하드코딩하지 않는다.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Provider:
    provider_type: str  # HOSPITAL | PHARMACY | CHECKUP_CENTER
    name: str
    address: str
    phone: Optional[str] = None


REQUIRED_FIELDS = ("provider_type", "name", "address")


def normalize_phone(phone: str) -> str:
    return "".join(ch for ch in phone if ch.isdigit())


def make_dedup_key(row: dict) -> str:
    """
    중복 제거 키:
    1) phone이 있으면 phone 정규화 값
    2) phone이 없으면 name+address 해시
    """
    phone = (row.get("phone") or "").strip()
    if phone:
        return f"phone:{normalize_phone(phone)}"

    base = f'{(row.get("name") or "").strip().lower()}|{(row.get("address") or "").strip().lower()}'
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]
    return f"name_addr:{h}"


def validate_row(row: dict) -> list[str]:
    errors: list[str] = []
    for f in REQUIRED_FIELDS:
        if not (row.get(f) or "").strip():
            errors.append(f"missing:{f}")
    return errors


def read_providers_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
    return rows


def dedup_rows(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    """
    returns: (deduped_rows, dropped_rows)
    """
    seen: set[str] = set()
    deduped: list[dict] = []
    dropped: list[dict] = []

    for row in rows:
        key = make_dedup_key(row)
        if key in seen:
            dropped.append({**row, "_dropped_reason": "duplicate", "_dedup_key": key})
            continue
        seen.add(key)
        deduped.append({**row, "_dedup_key": key})

    return deduped, dropped


def filter_valid(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    valid: list[dict] = []
    invalid: list[dict] = []
    for row in rows:
        errs = validate_row(row)
        if errs:
            invalid.append({**row, "_errors": ",".join(errs)})
        else:
            valid.append(row)
    return valid, invalid


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    # 모든 키를 모아 컬럼 구성(일관성 확보)
    fieldnames: list[str] = sorted({k for r in rows for k in r.keys()})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    # 입력 파일 경로(필요 시 수정)
    in_path = Path("data/sample_providers.csv")

    rows = read_providers_csv(in_path)
    valid, invalid = filter_valid(rows)
    deduped, dropped = dedup_rows(valid)

    write_csv(Path("out/providers_valid_dedup.csv"), deduped)
    write_csv(Path("out/providers_invalid.csv"), invalid)
    write_csv(Path("out/providers_dropped.csv"), dropped)

    print(f"input={len(rows)} valid={len(valid)} invalid={len(invalid)} deduped={len(deduped)} dropped={len(dropped)}")
    print("outputs:")
    print("- out/providers_valid_dedup.csv")
    print("- out/providers_invalid.csv")
    print("- out/providers_dropped.csv")


if __name__ == "__main__":
    main()


