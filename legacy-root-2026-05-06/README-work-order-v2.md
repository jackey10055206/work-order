# work_order_v2 DB bootstrap

這份說明只處理新的 v2 資料庫，不會動到既有 `work_order` DB。

## 新 DB 命名

- Database: `work_order_v2`
- Docker service: `work-order-v2-db`
- Docker compose file: `docker/work-order-v2/compose.yml`
- Host port: `3308`

> 舊系統目前仍使用 `work_order` / 3307；v2 故意分開，避免互相污染。

## 目錄

- `docker/work-order-v2/compose.yml`：MySQL 8 容器
- `sql/work_order_v2_schema.sql`：v2 schema
- `sql/migrations/2026-04-21_add_extra_material_total_to_work_order_lines.sql`：替既有 v2 DB 補上 `extra_material_total`
- `scripts/import_work_order_v2.py`：從舊 dump 匯入基礎資料

## 啟動 DB

```bash
cd /Users/luoweijie/Desktop/OpenClaw/github/work-order
docker compose -f docker/work-order-v2/compose.yml up -d
```

查看狀態：

```bash
docker compose -f docker/work-order-v2/compose.yml ps
```

## Schema 初始化

第一次啟動時，MySQL 會自動載入：

- `sql/work_order_v2_schema.sql`

如果 volume 已存在、想整個重建一次：

```bash
docker compose -f docker/work-order-v2/compose.yml down -v
docker compose -f docker/work-order-v2/compose.yml up -d
```

若 DB 已經建立、但只想補上新版欄位（例如這次新增的 `work_order_lines.extra_material_total`），可手動執行：

```bash
docker exec -i work-order-v2-db mysql -uworkorder_v2 -p123456 < sql/migrations/2026-04-21_add_extra_material_total_to_work_order_lines.sql
```

這個 migration 只針對 `work_order_v2`，不要對舊 `work_order` 執行。

## 匯入舊資料

舊 dump 路徑：

```bash
/Users/luoweijie/.openclaw/media/inbound/work_order_20260331---d604cff2-950c-4091-b83c-b50de94c9db0
```

執行匯入：

```bash
cd /Users/luoweijie/Desktop/OpenClaw/github/work-order
python3 scripts/import_work_order_v2.py \
  --dump-file /Users/luoweijie/.openclaw/media/inbound/work_order_20260331---d604cff2-950c-4091-b83c-b50de94c9db0
```

## 匯入範圍

目前只匯入基礎字典 / 主資料：

- `client` -> `clients`
- `central_data` -> `option_items`

## `option_items` 設計

舊 `central_data` 的六個欄位被拆成統一字典表 `option_items`：

- `product` -> `production_item`
- `material` -> `material`
- `process` -> `lamination`
- `plate` -> `board_type`
- `plate_thickness` -> `board_thickness`
- `others` -> `extra_material`

設計重點：

- 不再保留舊 `central_data` 的橫向六欄結構
- 改為 `option_group + item_name` 的統一資料字典
- 同值去重，保留 `legacy_source_*` 欄位方便追來源
- 後續 UI / API 可以直接依 `option_group` 拉下拉選單

## 驗證 SQL

```bash
docker exec -it work-order-v2-db mysql -uworkorder_v2 -p123456 -D work_order_v2 -e "SHOW TABLES;"

docker exec -it work-order-v2-db mysql -uworkorder_v2 -p123456 -D work_order_v2 -e "SELECT COUNT(*) AS clients FROM clients; SELECT option_group, COUNT(*) AS cnt FROM option_items GROUP BY option_group ORDER BY option_group;"
```

## 第一版 schema 摘要

### `clients`
客戶主檔。

### `option_items`
統一選項字典，用來承接舊 `central_data`。

### `work_orders`
新工單主表，保留基礎欄位與 `client_id` 關聯。

### `work_order_lines`
新工單明細表，採正規化欄位，直接指向各類 `option_items`。

其中：
- UI 的「計價」對應 `work_order_lines.line_total`
- UI 的「備料計價」對應 `work_order_lines.extra_material_total`
- `extra_material_total` 用來存每筆明細中「其他備料」那一段的獨立計價結果，避免和主品項的 `line_total` 混在一起

## 備註

- 這版沒有搬舊工單內容，只先建立新 DB + 基礎字典資料。
- 若之後要接 UI，建議新程式改查 `work_order_v2`，不要直接沿用舊 `central_data` / `save_*` 表。
