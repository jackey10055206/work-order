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
| 製作金額 | `le_productionAmount` | `work_orders.production_amount` | bottom summary；由畫面計算後存檔 |
| 稅額 | `le_taxAmount` | `work_orders.tax_amount` | `製作金額 × 0.05` 後以 `ceil` 無條件進位 |
| 總計 | `le_totalAmount` | `work_orders.total_amount` | `製作金額 + 稅額(進位後)` |
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

### 本輪新增的 v2 header 欄位

為了保留 bottom summary 的 round-trip，本輪在 `work_orders` 補上：
- `production_amount DECIMAL(12,2) NULL`
- `tax_amount DECIMAL(12,2) NULL`
- `total_amount DECIMAL(12,2) NULL`

對應 migration：`sql/migrations/2026-04-23_add_summary_amounts_to_work_orders.sql`

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
- `le_productionAmount` -> `work_orders.production_amount`
- `le_taxAmount` -> `work_orders.tax_amount`
- `le_totalAmount` -> `work_orders.total_amount`

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

## 6. 實測驗證（2026-04-22）

### 執行方式

使用 preview 內建 demo 資料直接走既有 `btn_save` 同路徑的存檔流程：

```bash
QT_QPA_PLATFORM=offscreen prototype/pyside6-demo/.venv/bin/python \
  prototype/pyside6-demo/preview_generated_ui.py --save-demo
```

實際輸出：

```text
SAVE_DEMO_OK:3:4
```

代表：
- `work_orders.id = 3` 成功 upsert
- 同次流程成功寫入 `work_order_lines` 共 4 筆

### DB 查詢驗證

```sql
SELECT id, work_number, client_id, company_phone, contact_name, work_time,
       cleanup_time, work_address, status
FROM work_orders
WHERE id = 3;

SELECT work_order_id, line_no, production_item_id, width_mm, height_mm, quantity,
       material_id, lamination_id, board_type_id, board_thickness_id,
       extra_material_id, extra_material_quantity, cbm, cbm_unit_price,
       line_total, extra_material_total
FROM work_order_lines
WHERE work_order_id = 3
ORDER BY line_no;

SELECT COUNT(*) AS blank_rows_saved
FROM work_order_lines
WHERE work_order_id = 3
  AND production_item_id IS NULL
  AND width_mm IS NULL
  AND height_mm IS NULL
  AND quantity IS NULL
  AND material_id IS NULL
  AND lamination_id IS NULL
  AND board_type_id IS NULL
  AND board_thickness_id IS NULL
  AND extra_material_id IS NULL
  AND extra_material_quantity IS NULL
  AND cbm IS NULL
  AND cbm_unit_price IS NULL
  AND line_total IS NULL
  AND extra_material_total IS NULL;
```

實測結果重點：
- header 成功落到 `work_orders`
- lines 成功落到 `work_order_lines`
- `extra_material_total` 四筆分別為 `300.00 / 0.00 / 480.00 / 180.00`
- `blank_rows_saved = 0`，代表空白列沒有被誤存

### UI / build 標記驗證

另以 offscreen screenshot 驗證 preview 可正常啟動且保留既有白底 UI：

```bash
QT_QPA_PLATFORM=offscreen prototype/pyside6-demo/.venv/bin/python \
  prototype/pyside6-demo/preview_generated_ui.py \
  --screenshot prototype/pyside6-demo/out/verify-build-label.png
```

build label 來自：
- `git rev-parse --short HEAD`
- 畫面左下顯示格式：`build: <short-hash>`

## 7. 已接上的開啟流程（2026-04-22）

`preview_generated_ui.py` 現在已把既有 `btn_open` 掛上載入流程。

### 開啟規則

1. 讀取 `le_worknum`
2. 以 `work_orders.work_number` 查 header
3. 找到後回填：
   - `le_worknum`
   - `le_caseName`
   - `cb_customerName`（顯示 `clients.short_name`）
   - `le_phone`
   - `le_contactName`
   - `le_startTime`
   - `le_endTime`
   - `lle_address`
   - `te_remark`
4. 再用 `work_orders.id` 查 `work_order_lines`
5. 透過 join `option_items` 把 FK 轉回 `item_name`，回填 middle table

### `option_items` FK 還原策略

載入時不是把 id 直接塞回 UI，而是：
- `work_order_lines.production_item_id` -> join `option_items pi` -> `pi.item_name`
- `material_id` / `lamination_id` / `board_type_id` / `board_thickness_id` / `extra_material_id`
  也各自 join `option_items` 取回顯示文字
- UI table 看到的是 `item_name`，不是數字 FK

### 查不到工單號時的定義

- `le_worknum` 空白：直接報錯 `請先輸入工單號再開啟。`
- `work_orders` 查不到：直接報錯 `找不到工單號：xxx`
- 不做靜默失敗

### 未存內容目前的最小處理

這輪先不做完整 dirty-check，也不比對「是否真的有變更」。

目前行為：
- 若畫面上除了查詢用的 `le_worknum` 之外，header / remark / middle table 已有任何內容
- 按 `開啟` 時先跳確認視窗：
  `目前畫面內容會直接被載入的工單覆蓋；尚未做完整 dirty-check。要繼續開啟嗎？`
- 使用者按 Yes 才覆蓋；按 No 取消

### 補充

- middle table 目前會保留至少 15 列；若 DB 明細超過 15 列，會自動把 rowCount 擴到足夠載完
- `le_productionAmount` / `le_taxAmount` / `le_totalAmount` 現在會優先載入 `work_orders.production_amount / tax_amount / total_amount`
- 若 DB 舊資料尚未有這三欄值，開啟後會依當前明細重新計算，避免 UI 與明細矛盾

## 8. Round-trip 驗證（2026-04-22）

本輪補上「開啟既有工單 -> 修改 header/lines -> 再儲存 -> 再開啟」的自動驗證入口：

```bash
QT_QPA_PLATFORM=offscreen prototype/pyside6-demo/.venv/bin/python \
  prototype/pyside6-demo/preview_generated_ui.py \
  --roundtrip-verify 26-03-29-01
```

實際驗證流程：
1. 以 `work_number=26-03-29-01` 載入既有工單
2. 修改 header 至少 3 個欄位：`case_name` / `contact_name` / `remark`
3. 修改第 1 列既有明細數值
4. 在最後一列空白列輸入新明細，確認 auto-append 會再補一列新的空白尾列
5. 再次儲存
6. 重新載入同一張工單
7. 直接查 DB，比對 `work_orders` 與 `work_order_lines` 是否和 UI reload 後一致

驗證結果（實測輸出摘要）：

```text
ROUNDTRIP_VERIFY_OK:{
  'work_order_id': 3,
  'original_line_count': 4,
  'saved_line_count': 5,
  'reloaded_line_count': 5,
  'db_line_count': 5,
  'header_count': 1,
  'duplicated_line_nos': 0,
  'auto_append_rows_before': 15,
  'auto_append_rows_after': 16,
  'tab_sequence': [(0, 0), (0, 1), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 12), (0, 14), (1, 0)],
  'build_label': 'build: <short-hash>'
}
```

### DB 無重複驗證重點

- `work_orders` 仍只會有 **1 筆** `work_number=26-03-29-01`
- `work_order_lines` 會以同一個 `work_order_id` 整批 replace，不會把舊 rows append 回去
- `duplicated_line_nos = 0`，代表沒有同工單內重複的 `line_no`
- reload 後 UI snapshot 與 DB snapshot 完全一致

### 這輪順手補的穩定性修正

`_collect_line_payloads()` 原本直接用 `row_index + 1` 當 `line_no`。

這在「載回既有 4 筆 -> 畫面保留 15 列空白 -> 使用者在最後空白列新增第 5 筆」時，可能把新列存成 `line_no=16`；雖然不一定會 duplicate，但 round-trip 後 `line_no` 會不穩定。

現在改成：
- 只對「有意義資料列」重新連續編號
- `line_no = len(valid_lines) + 1`

效果：
- round-trip 後 line ordering 穩定
- 不受中間保留空白列影響
- 更符合 UI 視角下的第 1 / 2 / 3 ... 筆明細

## 9. middle table 清列 / 刪列 UX（2026-04-22）

這輪在 `tbl_lineItems` 補上 **row-level 右鍵選單**，不新增額外常駐按鈕，盡量維持現有白底工作單畫面與 bottom 區塊不變。

### 觸發方式

對 middle table 任一列按右鍵，會出現兩個動作：

- `清除此列`
- `刪除此列`

### 行為定義

#### 1. 清列（clear row）

適用情境：
- 某一列打錯很多欄位，想快速清空重打
- 想保留目前列位置，不做整體重排

規則：
- **有效列**：把該列所有可編輯欄位清空，`x` 欄維持固定字樣 `x`
- **空白列 / 最後預備列**：不執行，status bar 提示「目前是空白列，無需清列」
- 清列後該列會變成空列；存檔時依既有規則 **不會存進 DB**
- 若清的是中間有效列，畫面上暫時可能留下空洞；真正需要重排時應使用 `刪除此列`

#### 2. 刪列（delete row）

適用情境：
- 多打一列有效列，想直接移除
- 中間某列不要了，希望後面列往上補齊
- auto-append 後多出來的空白列，想把 table 列數縮回來

規則：
- **中間有效列**：直接移除該列，後面列整體上移；之後存檔時 `line_no` 仍會依有效列重新連續編號
- **最後一筆有效列**：可直接刪掉；刪完後仍會自動保留 1 列空白預備列
- **中間空白列**：允許刪除，適合把多餘空白列縮掉
- **最後預備列**：
  - 若目前總列數 **大於** 預設 15 列，可刪除，用來把 auto-append 造成的多餘空白列縮回來
  - 若目前總列數已經是基準 15 列，則不再往下刪，永遠保留至少 1 列最後預備列

### 為什麼分成清列 / 刪列兩個動作

- `清列` 是 **快速修正輸入錯誤**，不動其他列
- `刪列` 是 **改變明細結構**，會讓後續列往上遞補並縮減列數

這樣比較符合實際使用：
- 打錯內容 -> 清列
- 這筆不要了 / 多打一列 -> 刪列

## 10. 小計 / 計算規則（2026-04-23）

`preview_generated_ui.py` 這輪已正式把 bottom 區的：
- `btn_subtotal`（小計）
- `btn_calcuate`（計算）

接上實際計算邏輯。

### `btn_subtotal`：逐列回填 `才數` / `計價`

只針對 **有意義資料列** 執行；整列都空白的預備列會略過。

每列規則：
1. 才數 = `寬度 × 長度 / 900 × 數量`
2. 才數結果採 **無條件進位整數**（`ceil`）
3. 計價 = `才數 × 單價`
4. 結果回填：
   - 第 11 欄 `才數`
   - 第 13 欄 `計價`

### `btn_calcuate`：回填 bottom summary

只加總 **有意義資料列**；空白列不納入。

規則：
1. 製作金額 = 所有列 `計價` 加總 + 所有列 `備料計價` 加總
2. `備料計價` 空白視為 `0`
3. `備料計價` 若是非數字，也以 `0` 處理，避免整張單因單一欄位髒值而不能按計算
4. 稅額 = `ceil(製作金額 × 0.05)`
5. 總計 = `製作金額 + 稅額(進位後)`
6. 結果回填：
   - `le_productionAmount`
   - `le_taxAmount`
   - `le_totalAmount`

### 空白 / 非數字值處理策略

本輪按鈕計算採用以下一致策略：
- `寬度 / 長度 / 數量 / 單價 / 備料計價` 空白時視為 `0`
- `備料計價` 非數字時視為 `0`
- 其餘參與按鈕運算的數字欄若出現非數字，也同樣以 `0` 處理
- 但 **正式存檔到 DB 時**，仍沿用既有嚴格解析規則；若 numeric 欄位內容不合法，存檔會報錯，不會默默寫髒資料進 DB

### 實測驗證（2026-04-23）

新增自動驗證入口：

```bash
QT_QPA_PLATFORM=offscreen prototype/pyside6-demo/.venv/bin/python \
  prototype/pyside6-demo/preview_generated_ui.py \
  --calc-verify
```

驗證案例：
1. 第 1 列：`100 × 100 / 900 × 1 = 11.111...` -> `ceil = 12`，單價 `10` -> 計價 `120`
2. 第 2 列：`100 × 100 / 900 × 5 = 55.555...` -> `ceil = 56`，單價 `20` -> 計價 `1120`
3. 第 3 列：`200 × 150 / 900 × 1 = 33.333...` -> `ceil = 34`，單價 `15` -> 計價 `510`
4. 備料計價分別放入：`50 / 空白 / abc`
   - 空白視為 `0`
   - `abc` 視為 `0`
5. 第 4 列額外驗證 tax ceiling：`90 × 90 / 900 × 1 = 9`，單價 `10` -> `90`，備料計價 `1`
6. 整張底部結果應為：
   - 製作金額 = `120 + 1120 + 510 + 90 + 50 + 1 = 1891`
   - 稅額 = `ceil(1891 × 0.05) = ceil(94.55) = 95`
   - 總計 = `1986`

實測輸出會回傳：
- 每列回填後的 `才數` / `計價`
- bottom summary 三個欄位值
- Tab 序列驗證
- auto-append 前後列數
- build label

另保留既有驗證：
- `--roundtrip-verify 26-03-29-01`：驗證 save/open round-trip、Tab、auto-append、build label
- `--row-ux-verify 26-04-22-ux01`：驗證清列 / 刪列 UX 後，Tab / auto-append / round-trip 仍正常

## 11. 清列 / 刪列驗證（2026-04-22）

新增自動驗證入口：

```bash
QT_QPA_PLATFORM=offscreen prototype/pyside6-demo/.venv/bin/python \
  prototype/pyside6-demo/preview_generated_ui.py \
  --row-ux-verify 26-04-22-ux01
```

實測輸出：

```text
ROW_UX_VERIFY_OK:{
  'work_order_id': 12,
  'baseline_line_count': 4,
  'baseline_table_rows': 15,
  'after_clear_line_count': 3,
  'after_middle_delete_line_count': 3,
  'after_last_delete_line_count': 2,
  'reloaded_line_count': 2,
  'db_line_count': 2,
  'middle_delete_tab_sequence': [(0,0)...(0,14),(1,0)],
  'final_tab_sequence': [(0,0)...(0,14),(1,0)],
  'build_label': 'build: 070b61a'
}
```

### 本輪驗證重點

1. **清列後不會把空列存進 DB**
   - 先存 4 筆 demo 明細
   - 對第 2 列執行 `清除此列`
   - 再存後 DB 只剩 3 筆有效明細

2. **刪除中間有效列後，UI / DB 順序正確**
   - 重新載入 baseline
   - 對中間有效列執行 `刪除此列`
   - 再存 / 再開後，UI meaningful rows 與 DB `ORDER BY line_no` 結果一致
   - `duplicated_line_nos = 0`

3. **刪除最後一筆有效列後仍保留空白預備列**
   - 刪除最後一筆有效明細後
   - reload 後 table 最後一列仍是空白列，不會整張表被刪光或失去預備列

4. **Tab 順序沒有壞**
   - middle table 驗證序列仍為：
     `(0,0) -> (0,1) -> (0,3) -> (0,4) -> (0,5) -> (0,6) -> (0,7) -> (0,8) -> (0,9) -> (0,10) -> (0,12) -> (0,14) -> (1,0)`
   - `x` 欄仍會跳過
   - locked 欄（才數 / 計價）仍不進 tab chain

5. **auto-append / save-open round-trip 沒壞**
   - 既有 `--roundtrip-verify 26-03-29-01` 仍可通過
   - 代表新增 row UX 後，最後一列有效時自動補新列、存檔只存有效列、開啟再載回、build label 保留等行為都仍正常


## 12. bottom summary 存檔規則（2026-04-23）

這輪把 bottom 區三個欄位正式納入 v2 `work_orders`：
- `production_amount`
- `tax_amount`
- `total_amount`

### 存檔時的行為

`save_work_order_with_lines()` 會先重新執行一次整單 summary 計算，再把結果寫回 UI 與 DB，避免使用者忘記先按 `計算` 就直接存檔。

也就是說：
1. 先依明細加總得到 `production_amount`
2. `tax_amount = ceil(production_amount × 0.05)`
3. `total_amount = production_amount + tax_amount`
4. 再把三個值一併 upsert 到 `work_orders`

### 開啟舊工單的相容策略

- 若 DB 該筆已有 `production_amount / tax_amount / total_amount`，直接載回 UI
- 若是舊資料尚未補這三欄，則依 `work_order_lines` 即時計算後回填 UI
- 這樣可以兼顧新資料 round-trip 與舊資料相容，不需要去動 legacy DB
