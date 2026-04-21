# Work Order v2 畫面欄位對 DB mapping

> 這份文件以 `prototype/pyside6-demo/preview_generated_ui.py` 現況為準，目的是把「目前畫面」和 `work_order_v2` schema 的落點先釐清，方便下一輪接存檔。

## 1. 主表 `work_orders`

### 已有明確對應

| 畫面欄位 | widget/objectName | DB 欄位 | 備註 |
| --- | --- | --- | --- |
| 工單號 | `le_worknum` | `work_orders.work_number` | 唯一鍵 |
| 案名 | `le_caseName` | `work_orders.case_name` | |
| 客戶名稱 | `cb_customerName` | `work_orders.client_id` | UI 顯示 `clients.short_name`，存檔應轉成 `clients.id` |
| 公司電話 | `le_phone` | `work_orders.company_phone` | 可由 `clients.phone` 預帶，但仍應允許人工覆寫 |
| 聯絡人 | `le_contactName` | `work_orders.contact_name` | |
| 施工時間 | `le_startTime` | `work_orders.work_time` | 目前 schema 是 `VARCHAR(100)` |
| 地址 | `lle_address` | `work_orders.work_address` | 可由 `clients.address` 預帶，但仍應允許人工覆寫 |
| 收工時間 | `le_endTime` | `work_orders.cleanup_time` | 目前 schema 是 `VARCHAR(100)` |
| 備註 | `te_remark` | `work_orders.remark` | |

### 目前 UI 有顯示，但這輪刻意不接 v2

| 畫面區塊 | 舊系統概念 | v2 狀態 | 原因 |
| --- | --- | --- | --- |
| 包裝 / 運輸 | `pack` / `transport` | 先不接 `pack_transport_option_id` | 本輪明確要求先忽略 `pack_transport_options` |
| 員工欄位 | `cemployee1..5` | 不接 | 本輪明確要求先忽略 `employees` |
| 狀態 | 無明顯 widget | `work_orders.status` | 可先由存檔流程固定寫 `draft` |

### schema 已有、但畫面目前沒有直接輸入欄

| DB 欄位 | 建議來源 |
| --- | --- |
| `work_orders.status` | 存檔時預設 `draft` |
| `work_orders.created_at` / `updated_at` | DB 自動維護 |

## 2. 明細表 `work_order_lines`

畫面主表 `tbl_lineItems` 每一列應對應一筆 `work_order_lines`。

| 表格欄 | 標題 | 欄位型態 | DB 欄位 | 備註 |
| --- | --- | --- | --- | --- |
| 0 | 製作項目 | editable combo | `production_item_id` | 以 `option_items.option_group='production_item'` 查 id |
| 1 | 寬度 | line edit | `width_mm` | 建議存數值 |
| 2 | x | 固定字樣 | - | 純 UI 分隔，不入庫 |
| 3 | 長度 | line edit | `height_mm` | schema 用 `height_mm` |
| 4 | 數量 | line edit | `quantity` | 主數量 |
| 5 | 材質 | editable combo | `material_id` | `option_group='material'` |
| 6 | 冷裱加工 | editable combo | `lamination_id` | `option_group='lamination'` |
| 7 | 板材種類 | editable combo | `board_type_id` | `option_group='board_type'` |
| 8 | 板材厚度 | editable combo | `board_thickness_id` | `option_group='board_thickness'` |
| 9 | 其他備料 | editable combo | `extra_material_id` | `option_group='extra_material'` |
| 10 | 數量 | line edit | `extra_material_quantity` | 備料數量 |
| 11 | 才數 | locked/display | `cbm` | 目前 UI 是唯讀計算欄 |
| 12 | 單價 | line edit | `cbm_unit_price` | 才數單價 |
| 13 | 計價 | locked/display | `line_total` | 主計價，目前 UI 是唯讀計算欄 |
| 14 | 備料計價 | line edit/display | `extra_material_total` | 對應「其他備料」的獨立計價金額，不與主項 `line_total` 共用 |

### 明細一定要補的系統欄位

| DB 欄位 | 來源 |
| --- | --- |
| `work_order_id` | 存完 `work_orders` 後取得主鍵回填 |
| `line_no` | 以畫面列序 `row_index + 1` |
| `created_at` / `updated_at` | DB 自動維護 |

### 已補齊的 schema 對位

`tbl_lineItems` 的最後一欄「備料計價」現在對應 `work_order_v2.work_order_lines.extra_material_total`。

定義規則：
1. 這欄專門存「其他備料」的獨立計價結果。
2. `line_total` 仍保留給主品項 / 才數計價，不和備料金額混用。
3. 若該列沒有其他備料，`extra_material_total` 可為 `NULL`。

## 3. 客戶自動帶入策略

`clients` 目前有：
- `short_name`
- `full_name`
- `phone`
- `address`
- `tax_id`

這輪 preview 採用的策略：
- `cb_customerName` 顯示並搜尋 `short_name`
- 選到已存在客戶時，**僅在電話 / 地址欄位為空，或仍是上一筆自動帶入值時**，才自動填入 `phone` / `address`
- 若使用者已手動改過電話 / 地址，不自動覆蓋

這樣可以兼顧：
- 便利性
- 不破壞 editable UX
- 不搶寫使用者手動輸入

## 4. 已接上的表頭存檔流程（prototype 現況）

目前 `preview_generated_ui.py` 已把既有 `btn_save` 掛上表頭存檔：

1. 讀取 TOP 區欄位
2. `cb_customerName.currentText()` → lookup `clients.short_name` → 取得 `clients.id`
3. 以 `work_number` 為唯一鍵對 `work_orders` 做 upsert
4. 若同工單號已存在，更新既有 `work_orders`；若不存在，建立新資料
5. `status` 先固定寫 `draft`

實際寫入欄位：
- `le_worknum` -> `work_orders.work_number`
- `le_caseName` -> `work_orders.case_name`
- `cb_customerName` -> `work_orders.client_id`
- `le_phone` -> `work_orders.company_phone`
- `le_contactName` -> `work_orders.contact_name`
- `le_startTime` -> `work_orders.work_time`
- `le_endTime` -> `work_orders.cleanup_time`
- `lle_address` -> `work_orders.work_address`
- `te_remark` -> `work_orders.remark`

### `cb_customerName` 查不到時的定義

若使用者在 editable combo 輸入了新名字，但 `clients.short_name` 查不到：
- **本輪不自動建客戶**
- **也不存 `NULL client_id` 混過去**
- 直接阻擋存檔並回報：`客戶「xxx」不存在 clients，請先建立客戶再儲存。`

這樣可以避免工單先落庫、客戶卻是模糊字串，後續不好補救。

## 5. 目前已接上的明細存檔規則（prototype 現況）

`btn_save` 現在會在同一次存檔流程內：

1. upsert `work_orders`
2. 取得 `work_orders.id`
3. 掃 `tbl_lineItems`
4. 依 `option_group + item_name` lookup `option_items.id`
5. 先刪除該工單舊的 `work_order_lines`
6. 再把本次畫面上的有效列整批重寫進 `work_order_lines`

### 空列判定規則

只要以下任一欄位有非空文字，就視為「這列有資料」並會嘗試存檔：
- 製作項目
- 寬度 / 長度 / 數量
- 材質 / 冷裱加工 / 板材種類 / 板材厚度 / 其他備料
- 備料數量 / 才數 / 單價 / 計價 / 備料計價

若上述欄位全部為空，該列會直接略過，不建立 `work_order_lines`。

### `option_items` lookup 規則

- combo 欄位一律依 `option_group + item_name` 精準查 FK
- 空白值可存 `NULL`
- **只要使用者輸入了非空文字，但 DB 查不到對應項目，就直接阻擋整次儲存並報錯**
- 不允許 fallback 到錯的 id，也不靜默寫入自由字串

### 明細寫入欄位

每筆有效列會寫入：
- `line_no`
- `production_item_id`
- `width_mm`
- `height_mm`
- `quantity`
- `material_id`
- `lamination_id`
- `board_type_id`
- `board_thickness_id`
- `extra_material_id`
- `extra_material_quantity`
- `cbm`
- `cbm_unit_price`
- `line_total`
- `extra_material_total`
