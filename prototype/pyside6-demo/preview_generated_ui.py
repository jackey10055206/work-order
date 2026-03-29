from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QTableWidgetItem

from ui_project_generated import Ui_MainWindow


class GeneratedUiPreviewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._tune_generated_layout()
        self._seed_demo_values()

    def _tune_generated_layout(self) -> None:
        bottom_layout = getattr(self.ui, "horizontalLayout_17", None)
        remark_group = getattr(self.ui, "grp_remark", None)
        summary_actions = getattr(self.ui, "wdg_summaryActions", None)
        if bottom_layout is None or remark_group is None or summary_actions is None:
            return

        remark_group.setMaximumWidth(420)
        remark_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        summary_actions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bottom_layout.setStretch(0, 1)
        bottom_layout.setStretch(1, 3)

    def _seed_demo_values(self) -> None:
        self.setWindowTitle("project.ui preview (generated)")

        customers = ["采月廣告有限公司", "萬榮國際", "KING", "就肆電競"]
        if hasattr(self.ui, "cb_customerName"):
            self.ui.cb_customerName.addItems(customers)
            self.ui.cb_customerName.setCurrentIndex(0)

        defaults = {
            "le_worknum": "26-03-29-01",
            "le_contactName": "王小姐",
            "le_phone": "02-8647-8840",
            "le_caseName": "南港展場春季活動主視覺",
            "le_workTime": "2026/03/31 09:00",
            "le_endTime": "2026/03/31 18:00",
            "lle_address": "台北市南港區經貿二路 186 號 4 樓",
            "le_productionAmount": "13600",
            "le_taxAmount": "680",
            "le_totalAmount": "14280",
        }
        for attr, value in defaults.items():
            widget = getattr(self.ui, attr, None)
            if widget is not None:
                widget.setText(value)

        if hasattr(self.ui, "te_remark"):
            self.ui.te_remark.setPlainText("現場施工前 30 分鐘需與窗口聯絡；材料依樓層分批搬運。")

        sample_rows = [
            ["主舞台背板輸出裱板", "500", "240", "2", "PVC 貼圖", "冷裱 + 修邊", "KT 板", "5", "含收邊黑膠帶", "80 才", "2800", "5600", "需與舞台結構對位", ""],
            ["入口拱門雙面輸出", "320", "260", "1", "防水帆布", "車縫 + 打銅扣", "—", "—", "雙面對裱", "22 才", "6500", "6500", "現場綁束帶固定", ""],
            ["指引立牌裱板", "90", "180", "6", "PP 相紙", "冷裱", "豪卡板", "10", "含腳架孔位", "67.5 才", "950", "5700", "依樓層分批包裝", ""],
        ]
        if hasattr(self.ui, "tbl_lineItems"):
            for row_idx, row in enumerate(sample_rows):
                for col_idx, value in enumerate(row):
                    self.ui.tbl_lineItems.setItem(row_idx, col_idx, QTableWidgetItem(value))
            self.ui.tbl_lineItems.resizeColumnsToContents()


def main() -> int:
    app = QApplication(sys.argv)
    window = GeneratedUiPreviewWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
