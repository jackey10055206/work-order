#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import pymysql

TABLE_COLUMNS = {
    "client": ["name", "full_name", "phone", "address", "taxID"],
    "employee": ["name"],
    "pack_transport": ["pack", "transport"],
    "central_data": ["product", "material", "process", "plate", "plate_thickness", "others"],
}

GROUP_MAPPING = {
    "product": "production_item",
    "material": "material",
    "process": "lamination",
    "plate": "board_type",
    "plate_thickness": "board_thickness",
    "others": "extra_material",
}

INSERT_RE = re.compile(r"INSERT INTO `(?P<table>[^`]+)` VALUES (?P<values>.*?);", re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import legacy work_order reference data into work_order_v2")
    parser.add_argument("--dump-file", required=True, help="Path to legacy MySQL dump")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3308)
    parser.add_argument("--user", default="workorder_v2")
    parser.add_argument("--password", default="123456")
    parser.add_argument("--database", default="work_order_v2")
    return parser.parse_args()


def split_tuples(values_blob: str) -> List[str]:
    tuples: List[str] = []
    current: List[str] = []
    depth = 0
    in_string = False
    escape = False

    for ch in values_blob:
        if depth == 0 and ch not in "(":
            continue

        if depth > 0 or ch == "(":
            current.append(ch)

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == "'":
                in_string = False
            continue

        if ch == "'":
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                tuples.append("".join(current).strip().rstrip(","))
                current = []

    return [t for t in tuples if t]


def parse_tuple(tuple_text: str) -> List[str | None]:
    inner = tuple_text.strip()
    if inner.startswith("(") and inner.endswith(")"):
        inner = inner[1:-1]

    values: List[str | None] = []
    current: List[str] = []
    in_string = False
    escape = False

    i = 0
    while i < len(inner):
        ch = inner[i]
        if in_string:
            if escape:
                current.append(ch)
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == "'":
                in_string = False
            else:
                current.append(ch)
        else:
            if ch == "'":
                in_string = True
            elif ch == ",":
                values.append(normalize_value("".join(current).strip()))
                current = []
            else:
                current.append(ch)
        i += 1

    values.append(normalize_value("".join(current).strip()))
    return values


def normalize_value(raw: str) -> str | None:
    if raw.upper() == "NULL":
        return None
    return raw


def extract_rows(dump_text: str, table: str) -> List[Dict[str, str | None]]:
    columns = TABLE_COLUMNS[table]
    rows: List[Dict[str, str | None]] = []
    for match in INSERT_RE.finditer(dump_text):
        if match.group("table") != table:
            continue
        for tuple_text in split_tuples(match.group("values")):
            values = parse_tuple(tuple_text)
            rows.append(dict(zip(columns, values, strict=False)))
    return rows


def connect(args: argparse.Namespace):
    return pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def import_clients(cur, rows: Sequence[Dict[str, str | None]]) -> int:
    sql = """
        INSERT INTO clients (short_name, full_name, phone, address, tax_id)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          full_name = VALUES(full_name),
          phone = VALUES(phone),
          address = VALUES(address),
          tax_id = VALUES(tax_id),
          is_active = 1
    """
    count = 0
    for row in rows:
        short_name = (row["name"] or "").strip()
        if not short_name:
            continue
        cur.execute(sql, (
            short_name,
            clean(row["full_name"]),
            clean(row["phone"]),
            clean(row["address"]),
            clean(row["taxID"]),
        ))
        count += 1
    return count


def import_employees(cur, rows: Sequence[Dict[str, str | None]]) -> int:
    sql = """
        INSERT INTO employees (name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE is_active = 1
    """
    count = 0
    for row in rows:
        name = (row["name"] or "").strip()
        if not name:
            continue
        cur.execute(sql, (name,))
        count += 1
    return count


def import_pack_transport(cur, rows: Sequence[Dict[str, str | None]]) -> int:
    sql = """
        INSERT INTO pack_transport_options (pack_name, transport_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE is_active = 1
    """
    count = 0
    for row in rows:
        pack = (row["pack"] or "").strip()
        transport = (row["transport"] or "").strip()
        if not pack and not transport:
            continue
        cur.execute(sql, (pack, transport))
        count += 1
    return count


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", text.strip()).strip("-").lower()
    return slug or text.strip().lower()


def import_option_items(cur, rows: Sequence[Dict[str, str | None]]) -> int:
    sql = """
        INSERT INTO option_items (option_group, item_name, slug, sort_order, legacy_source_table, legacy_source_column)
        VALUES (%s, %s, %s, %s, 'central_data', %s)
        ON DUPLICATE KEY UPDATE
          sort_order = LEAST(sort_order, VALUES(sort_order)),
          is_active = 1,
          legacy_source_table = VALUES(legacy_source_table),
          legacy_source_column = VALUES(legacy_source_column)
    """
    seen: set[Tuple[str, str]] = set()
    count = 0
    for row_index, row in enumerate(rows, start=1):
        for legacy_column, option_group in GROUP_MAPPING.items():
            value = (row[legacy_column] or "").strip()
            if not value:
                continue
            key = (option_group, value)
            if key in seen:
                continue
            seen.add(key)
            cur.execute(sql, (option_group, value, slugify(value), row_index, legacy_column))
            count += 1
    return count


def clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def main() -> None:
    args = parse_args()
    dump_path = Path(args.dump_file)
    dump_text = dump_path.read_text(encoding="utf-8", errors="replace")

    clients = extract_rows(dump_text, "client")
    employees = extract_rows(dump_text, "employee")
    pack_transport = extract_rows(dump_text, "pack_transport")
    central_data = extract_rows(dump_text, "central_data")

    conn = connect(args)
    try:
        with conn.cursor() as cur:
            results = {
                "clients": import_clients(cur, clients),
                "employees": import_employees(cur, employees),
                "pack_transport_options": import_pack_transport(cur, pack_transport),
                "option_items": import_option_items(cur, central_data),
            }
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    for table, count in results.items():
        print(f"{table}: imported/updated {count}")


if __name__ == "__main__":
    main()
