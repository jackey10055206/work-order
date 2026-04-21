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
| 14 | 備料計價 | line edit/display | **待確認** | schema 目前沒有獨立欄位 |

### 明細一定要補的系統欄位

| DB 欄位 | 來源 |
| --- | --- |
| `work_order_id` | 存完 `work_orders` 後取得主鍵回填 |
| `line_no` | 以畫面列序 `row_index + 1` |
| `created_at` / `updated_at` | DB 自動維護 |

### 目前 schema / UI 還有一個落差

`tbl_lineItems` 的最後一欄「備料計價」目前在畫面上存在，但 `work_order_v2.work_order_lines` 還沒有專屬欄位。

可選方向：
1. **短期**：先不入庫，或先併入 `note` / 暫存計算結果（不太理想）。
2. **較正規**：schema 後續補一個類似 `extra_material_line_total` 的 decimal 欄位。

如果下一輪要正式接存檔，這欄要先定義規則，不然 mapping 會留下洞。

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

## 4. 下一輪接存檔的最小路徑

1. `cb_customerName.currentText()` → 查 `clients.id`
2. 先 insert / update `work_orders`
3. 取得 `work_orders.id`
4. 掃 `tbl_lineItems` 非空列
5. 各 combo 文字再 lookup 對應 `option_items.id`
6. 逐列寫入 `work_order_lines`
7. 對於「備料計價」先決定 schema 去向，再一起收斂
