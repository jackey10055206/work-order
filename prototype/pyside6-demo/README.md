# PySide6 Work Order Prototype

這個 demo 是獨立於現有 PyQt5 專案之外的 prototype，重做工單最上方的「基本資料區」，只聚焦以下欄位：

- 案名
- 客戶名稱
- 電話
- 工單編號
- 聯絡人
- 工作時間
- 清場時間
- 工作地址
- 包裝
- 運送

UI 全部使用 Qt layout（`QVBoxLayout` / `QHBoxLayout` / `QFormLayout` / `QGridLayout`）組成，沒有用固定 `setGeometry` 當主布局。

## 檔案

- `app.py`：主程式
- `requirements.txt`：最小依賴
- `run_demo.sh`：mac / Linux 快速啟動腳本

## macOS 安裝與執行

### 1) 建議先建立虛擬環境

```bash
cd prototype/pyside6-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 2) 安裝 PySide6

```bash
pip install -r requirements.txt
```

### 3) 執行 demo

```bash
python3 app.py
```

或：

```bash
chmod +x run_demo.sh
./run_demo.sh
```

## Windows 安裝與執行

### 1) 開啟 PowerShell，建立虛擬環境

```powershell
cd prototype/pyside6-demo
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) 安裝 PySide6

```powershell
pip install -r requirements.txt
```

### 3) 執行 demo

```powershell
py app.py
```

## Prototype 說明

- 以卡片式分組重做基本資料區：案件資訊、聯絡資訊、進撤場時間、工作地點、包裝與運送。
- 介面使用預設示意資料，方便直接看版。
- 目前未串接資料庫、Excel、舊版 PyQt5 表單或儲存流程。
- 目的是先驗證 PySide6 版面與使用感是否可行。
