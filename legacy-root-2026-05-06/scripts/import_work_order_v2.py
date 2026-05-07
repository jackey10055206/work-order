#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import pymysql

LINE_COUNT = 15

TABLE_COLUMNS = {
    "client": ["name", "full_name", "phone", "address", "taxID"],
    "central_data": ["product", "material", "process", "plate", "plate_thickness", "others"],
    "save_basic_data": [
        "worknum",
        "case_name",
        "company_name",
        "phone",
        "client_name",
        "worktime",
        "cleanuptime",
        "workaddress",
        "pack",
        "transport",
        "cemployee1",
        "cemployee2",
        "cemployee3",
        "cemployee4",
        "cemployee5",
        "crossbar_width",
        "crossbar_amount",
        "crossbar_remark",
        "150shelter",
        "180shelter",
        "iron_Shelter_amount",
        "iron_Shelter_remark",
        "paper_Shelter_height",
        "paper_Shelter_amount",
        "paper_Shelter_remark",
        "stand_style",
        "stand_amount",
        "stand_remark",
        "rent1",
        "rent2",
        "remark",
    ],
    "save_central_data": [
        "worknum",
        *[f"comboBox_product_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_width_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_height_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_amount_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"comboBox_material_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"comboBox_process_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"comboBox_plate_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"comboBox_thicknes_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"comboBox_others_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_others_amount_{i}" for i in range(1, LINE_COUNT + 1)],
    ],
    "save_price_data": [
        "worknum",
        *[f"lineEdit_CBM_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_CBMprice_{i}" for i in range(1, LINE_COUNT + 1)],
        *[f"lineEdit_single_price_{i}" for i in range(1, (LINE_COUNT * 2) + 1)],
        "lineEdit_tmpprice",
        "lineEdit_tax",
        "lineEdit_final_price",
    ],
}

GROUP_MAPPING = {
    "product": "production_item",
    "material": "material",
    "process": "lamination",
    "plate": "board_type",
    "plate_thickness": "board_thickness",
    "others": "extra_material",
}

LINE_GROUP_FIELDS = {
    "production_item": "comboBox_product_{i}",
    "material": "comboBox_material_{i}",
    "lamination": "comboBox_process_{i}",
    "board_type": "comboBox_plate_{i}",
    "board_thickness": "comboBox_thicknes_{i}",
    "extra_material": "comboBox_others_{i}",
}

INSERT_RE = re.compile(r"INSERT INTO `(?P<table>[^`]+)` VALUES (?P<values>.*?);", re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import legacy work_order data into work_order_v2")
    parser.add_argument("--dump-file", required=True, help="Path to legacy MySQL dump")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3308)
    parser.add_argument("--user", default="workorder_v2")
    parser.add_argument("--password", default="123456")
    parser.add_argument("--database", default="work_order_v2")
    parser.add_argument("--dry-run", action="store_true", help="Parse and summarize without writing DB")
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


def clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", text.strip()).strip("-").lower()
    return slug or text.strip().lower()


def parse_int(value: str | None) -> int | None:
    value = clean(value)
    if value is None:
        return None
    try:
        return int(Decimal(value))
    except (InvalidOperation, ValueError):
        return None


def parse_decimal(value: str | None) -> Decimal | None:
    value = clean(value)
    if value is None:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


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
        short_name = clean(row["name"])
        if short_name is None:
            continue
        cur.execute(
            sql,
            (
                short_name,
                clean(row["full_name"]),
                clean(row["phone"]),
                clean(row["address"]),
                clean(row["taxID"]),
            ),
        )
        count += 1
    return count


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
            value = clean(row[legacy_column])
            if value is None:
                continue
            key = (option_group, value)
            if key in seen:
                continue
            seen.add(key)
            cur.execute(sql, (option_group, value, slugify(value), row_index, legacy_column))
            count += 1
    return count


def rows_by_worknum(rows: Sequence[Dict[str, str | None]]) -> Dict[str, Dict[str, str | None]]:
    by_worknum: Dict[str, Dict[str, str | None]] = {}
    for row in rows:
        worknum = clean(row.get("worknum"))
        if worknum is None:
            continue
        by_worknum[worknum] = row
    return by_worknum


def load_client_ids(cur) -> Dict[str, int]:
    cur.execute("SELECT id, short_name FROM clients")
    return {row["short_name"]: int(row["id"]) for row in cur.fetchall() if row.get("short_name")}


def load_option_ids(cur) -> Dict[Tuple[str, str], int]:
    cur.execute("SELECT id, option_group, item_name FROM option_items")
    mapping: Dict[Tuple[str, str], int] = {}
    for row in cur.fetchall():
        group = row.get("option_group")
        name = clean(row.get("item_name"))
        if group and name:
            mapping[(str(group), name)] = int(row["id"])
    return mapping


def is_truthy_string(value: str | None) -> bool:
    value = clean(value)
    if value is None:
        return False
    return value not in {"0", "0.0", "0.00"}


def is_line_meaningful(central_row: Dict[str, str | None] | None, price_row: Dict[str, str | None] | None, index: int) -> bool:
    fields = []
    if central_row is not None:
        fields.extend(
            [
                central_row.get(f"comboBox_product_{index}"),
                central_row.get(f"lineEdit_width_{index}"),
                central_row.get(f"lineEdit_height_{index}"),
                central_row.get(f"lineEdit_amount_{index}"),
                central_row.get(f"comboBox_material_{index}"),
                central_row.get(f"comboBox_process_{index}"),
                central_row.get(f"comboBox_plate_{index}"),
                central_row.get(f"comboBox_thicknes_{index}"),
                central_row.get(f"comboBox_others_{index}"),
                central_row.get(f"lineEdit_others_amount_{index}"),
            ]
        )
    if price_row is not None:
        fields.extend(
            [
                price_row.get(f"lineEdit_CBM_{index}"),
                price_row.get(f"lineEdit_CBMprice_{index}"),
                price_row.get(f"lineEdit_single_price_{index}"),
                price_row.get(f"lineEdit_single_price_{index + LINE_COUNT}"),
            ]
        )
    return any(is_truthy_string(value) for value in fields)


def is_work_order_meaningful(
    basic_row: Dict[str, str | None] | None,
    central_row: Dict[str, str | None] | None,
    price_row: Dict[str, str | None] | None,
) -> bool:
    if basic_row is not None:
        header_fields = [
            basic_row.get("case_name"),
            basic_row.get("company_name"),
            basic_row.get("client_name"),
            basic_row.get("workaddress"),
            basic_row.get("remark"),
        ]
        if any(clean(value) for value in header_fields):
            return True
    if price_row is not None:
        totals = [
            price_row.get("lineEdit_tmpprice"),
            price_row.get("lineEdit_tax"),
            price_row.get("lineEdit_final_price"),
        ]
        if any(is_truthy_string(value) for value in totals):
            return True
    return any(is_line_meaningful(central_row, price_row, index) for index in range(1, LINE_COUNT + 1))


def resolve_option(option_ids: Dict[Tuple[str, str], int], group: str, raw_value: str | None) -> Tuple[int | None, str | None]:
    value = clean(raw_value)
    if value is None:
        return None, None
    option_id = option_ids.get((group, value))
    if option_id is not None:
        return option_id, None
    return None, value


def build_header_payload(
    worknum: str,
    basic_row: Dict[str, str | None] | None,
    price_row: Dict[str, str | None] | None,
    client_ids: Dict[str, int],
) -> Dict[str, object]:
    company_name = clean(basic_row.get("company_name") if basic_row else None)
    client_id = client_ids.get(company_name) if company_name else None

    return {
        "work_number": worknum,
        "case_name": clean(basic_row.get("case_name") if basic_row else None),
        "client_id": client_id,
        "customer_name_text": company_name,
        "company_phone": clean(basic_row.get("phone") if basic_row else None),
        "contact_name": clean(basic_row.get("client_name") if basic_row else None),
        "work_time": clean(basic_row.get("worktime") if basic_row else None),
        "cleanup_time": clean(basic_row.get("cleanuptime") if basic_row else None),
        "work_address": clean(basic_row.get("workaddress") if basic_row else None),
        "production_amount": parse_decimal(price_row.get("lineEdit_tmpprice") if price_row else None),
        "tax_amount": parse_decimal(price_row.get("lineEdit_tax") if price_row else None),
        "total_amount": parse_decimal(price_row.get("lineEdit_final_price") if price_row else None),
        "remark": clean(basic_row.get("remark") if basic_row else None),
        "status": "draft",
    }


def build_line_payloads(
    worknum: str,
    central_row: Dict[str, str | None] | None,
    price_row: Dict[str, str | None] | None,
    option_ids: Dict[Tuple[str, str], int],
) -> List[Dict[str, object]]:
    payloads: List[Dict[str, object]] = []
    for index in range(1, LINE_COUNT + 1):
        if not is_line_meaningful(central_row, price_row, index):
            continue

        production_item_id, production_item_text = resolve_option(option_ids, "production_item", central_row.get(f"comboBox_product_{index}") if central_row else None)
        material_id, material_text = resolve_option(option_ids, "material", central_row.get(f"comboBox_material_{index}") if central_row else None)
        lamination_id, lamination_text = resolve_option(option_ids, "lamination", central_row.get(f"comboBox_process_{index}") if central_row else None)
        board_type_id, board_type_text = resolve_option(option_ids, "board_type", central_row.get(f"comboBox_plate_{index}") if central_row else None)
        board_thickness_id, board_thickness_text = resolve_option(option_ids, "board_thickness", central_row.get(f"comboBox_thicknes_{index}") if central_row else None)
        extra_material_id, extra_material_text = resolve_option(option_ids, "extra_material", central_row.get(f"comboBox_others_{index}") if central_row else None)

        payloads.append(
            {
                "worknum": worknum,
                "line_no": index,
                "production_item_id": production_item_id,
                "production_item_text": production_item_text,
                "width_mm": parse_decimal(central_row.get(f"lineEdit_width_{index}") if central_row else None),
                "height_mm": parse_decimal(central_row.get(f"lineEdit_height_{index}") if central_row else None),
                "quantity": parse_int(central_row.get(f"lineEdit_amount_{index}") if central_row else None),
                "material_id": material_id,
                "material_text": material_text,
                "lamination_id": lamination_id,
                "lamination_text": lamination_text,
                "board_type_id": board_type_id,
                "board_type_text": board_type_text,
                "board_thickness_id": board_thickness_id,
                "board_thickness_text": board_thickness_text,
                "extra_material_id": extra_material_id,
                "extra_material_text": extra_material_text,
                "extra_material_quantity": parse_int(central_row.get(f"lineEdit_others_amount_{index}") if central_row else None),
                "cbm": parse_decimal(price_row.get(f"lineEdit_CBM_{index}") if price_row else None),
                "cbm_unit_price": parse_decimal(price_row.get(f"lineEdit_CBMprice_{index}") if price_row else None),
                "line_total": parse_decimal(price_row.get(f"lineEdit_single_price_{index}") if price_row else None),
                "extra_material_total": parse_decimal(price_row.get(f"lineEdit_single_price_{index + LINE_COUNT}") if price_row else None),
            }
        )
    return payloads


def upsert_work_order_header(cur, payload: Dict[str, object]) -> int:
    sql = """
        INSERT INTO work_orders (
            work_number, case_name, client_id, customer_name_text, company_phone,
            contact_name, work_time, cleanup_time, work_address,
            production_amount, tax_amount, total_amount, remark, status
        ) VALUES (
            %(work_number)s, %(case_name)s, %(client_id)s, %(customer_name_text)s, %(company_phone)s,
            %(contact_name)s, %(work_time)s, %(cleanup_time)s, %(work_address)s,
            %(production_amount)s, %(tax_amount)s, %(total_amount)s, %(remark)s, %(status)s
        )
        ON DUPLICATE KEY UPDATE
            case_name = VALUES(case_name),
            client_id = VALUES(client_id),
            customer_name_text = VALUES(customer_name_text),
            company_phone = VALUES(company_phone),
            contact_name = VALUES(contact_name),
            work_time = VALUES(work_time),
            cleanup_time = VALUES(cleanup_time),
            work_address = VALUES(work_address),
            production_amount = VALUES(production_amount),
            tax_amount = VALUES(tax_amount),
            total_amount = VALUES(total_amount),
            remark = VALUES(remark),
            status = VALUES(status),
            id = LAST_INSERT_ID(id)
    """
    cur.execute(sql, payload)
    return int(cur.lastrowid)


def replace_work_order_lines(cur, work_order_id: int, line_payloads: Sequence[Dict[str, object]]) -> int:
    cur.execute("DELETE FROM work_order_lines WHERE work_order_id = %s", (work_order_id,))
    if not line_payloads:
        return 0

    sql = """
        INSERT INTO work_order_lines (
            work_order_id, line_no, production_item_id, production_item_text, width_mm, height_mm, quantity,
            material_id, material_text, lamination_id, lamination_text, board_type_id, board_type_text,
            board_thickness_id, board_thickness_text, extra_material_id, extra_material_text,
            extra_material_quantity, cbm, cbm_unit_price, line_total, extra_material_total
        ) VALUES (
            %(work_order_id)s, %(line_no)s, %(production_item_id)s, %(production_item_text)s, %(width_mm)s, %(height_mm)s, %(quantity)s,
            %(material_id)s, %(material_text)s, %(lamination_id)s, %(lamination_text)s, %(board_type_id)s, %(board_type_text)s,
            %(board_thickness_id)s, %(board_thickness_text)s, %(extra_material_id)s, %(extra_material_text)s,
            %(extra_material_quantity)s, %(cbm)s, %(cbm_unit_price)s, %(line_total)s, %(extra_material_total)s
        )
    """
    rows = []
    for payload in line_payloads:
        row = dict(payload)
        row.pop("worknum", None)
        row["work_order_id"] = work_order_id
        rows.append(row)
    cur.executemany(sql, rows)
    return len(rows)


def main() -> None:
    args = parse_args()
    dump_path = Path(args.dump_file)
    dump_text = dump_path.read_text(encoding="utf-8", errors="replace")

    clients = extract_rows(dump_text, "client")
    central_data = extract_rows(dump_text, "central_data")
    save_basic_rows = extract_rows(dump_text, "save_basic_data")
    save_central_rows = extract_rows(dump_text, "save_central_data")
    save_price_rows = extract_rows(dump_text, "save_price_data")

    basic_by_worknum = rows_by_worknum(save_basic_rows)
    central_by_worknum = rows_by_worknum(save_central_rows)
    price_by_worknum = rows_by_worknum(save_price_rows)
    worknums = sorted(set(basic_by_worknum) | set(central_by_worknum) | set(price_by_worknum))

    conn = connect(args)
    results: Dict[str, object] = {}
    try:
        with conn.cursor() as cur:
            results["clients"] = import_clients(cur, clients)
            results["option_items"] = import_option_items(cur, central_data)

            client_ids = load_client_ids(cur)
            option_ids = load_option_ids(cur)

            skipped_empty = 0
            imported_orders = 0
            imported_lines = 0

            for worknum in worknums:
                basic_row = basic_by_worknum.get(worknum)
                central_row = central_by_worknum.get(worknum)
                price_row = price_by_worknum.get(worknum)

                if not is_work_order_meaningful(basic_row, central_row, price_row):
                    skipped_empty += 1
                    continue

                header_payload = build_header_payload(worknum, basic_row, price_row, client_ids)
                line_payloads = build_line_payloads(worknum, central_row, price_row, option_ids)

                if args.dry_run:
                    imported_orders += 1
                    imported_lines += len(line_payloads)
                    continue

                work_order_id = upsert_work_order_header(cur, header_payload)
                imported_orders += 1
                imported_lines += replace_work_order_lines(cur, work_order_id, line_payloads)

            results.update(
                {
                    "work_orders": imported_orders,
                    "work_order_lines": imported_lines,
                    "skipped_empty_work_orders": skipped_empty,
                }
            )

        if args.dry_run:
            conn.rollback()
        else:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
