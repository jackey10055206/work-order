# Work Order v2

目前 repo root 以 `preview_generated_ui.py` 為主線，已可：

- 以工單號開啟既有工單
- 讀寫 `work_order_v2` MySQL
- 儲存 `work_orders` / `work_order_lines`
- 匯出請款 Excel
- 支援「客戶主檔 id」與「工單客戶文字」分開存放

## 主要檔案

- `preview_generated_ui.py`：主程式（目前正式 UI）
- `ui_project_generated.py`：由 `project.ui` 產生的 UI 類別
- `project.ui`：Qt Designer UI 檔
- `requirements.txt`：執行依賴
- `sql/work_order_v2_schema.sql`：v2 schema
- `sql/work_order_v2_export_2026-05-07.sql`：已驗證資料的完整匯出（schema + data）
- `legacy-root-2026-05-06/`：舊 root 封存與 migration 參考資料

## 本機執行

### macOS

```bash
cd /Users/luoweijie/Desktop/OpenClaw/github/work-order
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python preview_generated_ui.py
```

### Windows

```powershell
cd work-order
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py preview_generated_ui.py
```

## Windows 用 PyInstaller 打包

先在 Windows 自己的虛擬環境安裝：

```powershell
pip install -r requirements.txt pyinstaller
```

然後打包：

```powershell
pyinstaller --noconfirm --windowed --name work-order ^
  --add-data "project.ui;." ^
  --add-data "ui_project_generated.py;." ^
  --add-data "excel_all.xlsx;." ^
  --add-data "excel_payment.xlsx;." ^
  --add-data "icon1.ico;." ^
  preview_generated_ui.py
```

> 如果你用 PowerShell，也可以把 `^` 換成反引號 `` ` `` 或直接寫成一行。

## 建立公司新資料庫

### 方案 A：直接匯完整資料（最快）

把這份匯進新 MySQL：

- `sql/work_order_v2_export_2026-05-07.sql`

它包含：

- `clients`
- `option_items`
- `work_orders`
- `work_order_lines`
- 已匯入完成的歷史資料

### 方案 B：只建 schema

如果你只想先建空表：

- `sql/work_order_v2_schema.sql`

## 目前資料狀態

已驗證匯入結果：

- `work_orders`: 2341
- `work_order_lines`: 17061
- 略過空白工單：9
- `client_id` 為空、但保留 `customer_name_text` 的工單：60

## 客戶欄位規則

`work_orders` 現在同時支援：

- `client_id`：對到正式 `clients` 主檔
- `customer_name_text`：只保留工單上的客戶文字，不污染主檔

因此：

- 常用客戶可維持主檔化
- 路人客 / 一次性客戶也能正常存工單

## 注意事項

1. `preview_generated_ui.py` 才是主線，不是 `app.py`
2. 公司端若要重建 DB，請確認 MySQL 字元集是 `utf8mb4`
3. 若工單載入正常但客戶下拉沒對到，多半是落在 `customer_name_text`，不是壞資料
4. Windows 打包請在 Windows 上執行，不要拿 macOS build 直接用
5. 若之後再重匯歷史資料，請先確認目標 DB 是否要清空 `work_orders` / `work_order_lines`
