# PySide6 Work Order Prototype

這個 demo 是獨立於現有 PyQt5 專案之外的 prototype，延續第一版的上方「基本資料區」，並在第二版補上中間「工單明細表區」。

## 目前 prototype 範圍

### 第一版：基本資料區

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

這一區全部使用 Qt layout（`QVBoxLayout` / `QHBoxLayout` / `QFormLayout` / `QGridLayout`）組成，沒有用固定 `setGeometry` 當主布局。

### 第二版：工單明細表區

第二版新增中間工單明細表，改用 `QTableWidget` 來承載真正的表格資料，而不是用大量手工命名 widget 硬排。

目前表格欄位包含：

- 製作項目
- 寬
- 長
- 數量
- 材質
- 加工
- 板材
- 厚度
- 其他
- 數量/才數
- 單價
- 計價
- 備註

補了幾筆示意資料，方便直接檢視：

- 中段橫向資訊排列與原工單閱讀節奏是否接近
- 多欄位明細在桌面視窗中的密度與可讀性
- 後續如果接資料庫 / Excel 匯出，欄位 mapping 是否更自然

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

## 驗證方式

### 語法檢查

```bash
python3 -m py_compile app.py
```

### 離屏啟動（適合 CI / 無桌面環境）

```bash
QT_QPA_PLATFORM=offscreen python3 app.py
```

如果要自動確認視窗能建立、不進入互動事件迴圈太久，可以用這種方式：

```bash
QT_QPA_PLATFORM=offscreen python3 -c "import app; from PySide6.QtWidgets import QApplication; q=QApplication([]); w=app.WorkOrderPrototypeWindow(); w.show(); print(w.isVisible(), w.windowTitle()); q.processEvents()"
```

## Prototype 說明

- 延續第一版卡片式分組：案件資訊、聯絡資訊、進撤場時間、工作地點、包裝與運送。
- 第二版新增中間工單明細表區，使用 `QTableWidget` 表達工單項目、尺寸、材質、加工與計價資訊。
- 介面使用預設示意資料，方便直接看版。
- 目前未串接資料庫、Excel、舊版 PyQt5 表單或儲存流程。
- 目的是先驗證 PySide6 版面與使用感是否可行，尤其是中段明細改成表格後的可維護性。
