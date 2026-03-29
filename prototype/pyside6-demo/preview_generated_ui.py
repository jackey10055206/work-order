from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStyleFactory,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui_project_generated import Ui_MainWindow


class GeneratedUiPreviewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._apply_preview_fixes()
        self._seed_demo_values()

    def _apply_preview_fixes(self) -> None:
        self.resize(1680, 980)
        self.setMinimumSize(1360, 900)

        self._apply_light_palette()
        self._repair_main_layout_sizing()
        self._repair_bottom_section_layout()
        self._improve_table_behavior()
        self._normalize_input_heights()

    def _apply_light_palette(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f4f6f8"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#1f2933"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#eef2f6"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#2563eb"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #f4f6f8;
                color: #1f2933;
            }
            QLineEdit, QComboBox, QTextEdit, QTableWidget {
                background: #ffffff;
                color: #111827;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
            }
            QTableWidget {
                gridline-color: #d7dee7;
                alternate-background-color: #f8fafc;
            }
            QHeaderView::section {
                background: #e8edf3;
                color: #1f2933;
                padding: 6px 8px;
                border: 1px solid #d7dee7;
                font-weight: 600;
            }
            QGroupBox {
                background: #ffffff;
                border: 1px solid #d7dee7;
                border-radius: 8px;
                margin-top: 10px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: #334155;
            }
            QPushButton {
                background: #ffffff;
                color: #111827;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: #f8fafc;
            }
            """
        )

    def _repair_main_layout_sizing(self) -> None:
        root_layout = self.ui.verticalLayout_2
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(14)
        root_layout.setStretch(0, 0)
        root_layout.setStretch(1, 1)
        root_layout.setStretch(2, 0)

        self.ui.wdg_topContent.setMinimumHeight(120)
        self.ui.wdg_lineItems.setMinimumHeight(420)
        self.ui.wdg_lineItems.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        self.ui.wdg_bottomSection.setMinimumHeight(250)
        self.ui.wdg_bottomSection.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding,
        )

    def _repair_bottom_section_layout(self) -> None:
        container = self.ui.widget10
        container.setParent(None)
        container.setGeometry(0, 0, 0, 0)

        bottom_layout = QHBoxLayout(self.ui.wdg_bottomSection)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(16)
        bottom_layout.addWidget(container, 3)

        container_layout = self.ui.horizontalLayout_17
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(16)
        container_layout.setStretch(0, 5)
        container_layout.setStretch(1, 7)

        self.ui.grp_remark.setMinimumWidth(380)
        self.ui.grp_remark.setMinimumHeight(230)
        self.ui.te_remark.setMinimumHeight(190)

        self.ui.wdg_summaryActions.setMinimumWidth(760)
        self.ui.wdg_summaryActions.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        summary_layout = QVBoxLayout(self.ui.wdg_summaryActions)
        summary_layout.setContentsMargins(0, 0, 0, 0)
        summary_layout.setSpacing(12)

        for widget in (self.ui.wdg_amountSummary, self.ui.wdg_actionButtons):
            widget.setParent(None)
            widget.setGeometry(0, 0, 0, 0)
            summary_layout.addWidget(widget)

        amount_layout = self.ui.horizontalLayout_13
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(12)

        self.ui.wdg_amountSummary.setMinimumHeight(72)
        self.ui.wdg_actionButtons.setMinimumHeight(110)

        action_host = self.ui.widget14
        action_host.setParent(None)
        action_host.setGeometry(0, 0, 0, 0)
        action_layout = QVBoxLayout(self.ui.wdg_actionButtons)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(0)
        action_layout.addWidget(action_host)

        self.ui.verticalLayout_3.setSpacing(12)
        self.ui.horizontalLayout_14.setSpacing(8)
        self.ui.horizontalLayout_16.setSpacing(8)
        self.ui.horizontalLayout_15.setSpacing(8)

        for button in self.findChildren(QPushButton):
            button.setMinimumHeight(34)
            button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.ui.btn_import.setMinimumSize(125, 36)
        self.ui.btn_invoice.setMinimumSize(125, 36)

    def _improve_table_behavior(self) -> None:
        table = self.ui.tbl_lineItems
        table.setAlternatingRowColors(True)
        table.verticalHeader().setDefaultSectionSize(30)
        table.horizontalHeader().setMinimumSectionSize(72)
        table.horizontalHeader().setStretchLastSection(True)
        table.setMinimumHeight(430)

    def _normalize_input_heights(self) -> None:
        for widget in self.findChildren(QWidget):
            name = widget.metaObject().className()
            if name in {"QLineEdit", "QComboBox"}:
                widget.setMinimumHeight(32)

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
            "le_startTime": "2026/03/31 09:00",
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
    app.setStyle(QStyleFactory.create("Fusion"))
    window = GeneratedUiPreviewWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
