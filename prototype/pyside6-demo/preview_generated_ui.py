from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QSizePolicy,
    QStyleFactory,
    QTableWidgetItem,
)

from ui_project_generated import Ui_MainWindow


TABLE_HEADERS = [
    "製作項目",
    "寬度",
    "x",
    "長度",
    "數量",
    "材質",
    "冷熱加工",
    "板材種類",
    "板材厚度",
    "其他備料",
    "數量",
    "才數",
    "單價",
    "計價",
    "備料計價",
]

# Excel / 工具表格感：寬欄給描述類欄位，中欄給數值，x 欄極窄固定顯示。
TABLE_COLUMN_WIDTHS = [220, 82, 36, 82, 68, 140, 136, 126, 86, 144, 68, 84, 88, 92, 104]
X_COLUMN_INDEX = 2
NUMERIC_COLUMN_INDEXES = {1, 3, 4, 10, 11, 12, 13, 14}
SELECT_LIKE_COLUMN_INDEXES = {0, 5, 6, 7, 8, 9}


def apply_light_preview_theme(app: QApplication) -> None:
    app.setStyle(QStyleFactory.create("Fusion"))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#f5f5f5"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#202124"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f7f7f7"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#202124"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#202124"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#202124"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#4c8bf5"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Light, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Midlight, QColor("#e6e6e6"))
    palette.setColor(QPalette.ColorRole.Mid, QColor("#cfcfcf"))
    palette.setColor(QPalette.ColorRole.Dark, QColor("#9e9e9e"))
    palette.setColor(QPalette.ColorRole.Shadow, QColor("#808080"))
    app.setPalette(palette)

    app.setStyleSheet(
        """
        QWidget {
            background-color: #f5f5f5;
            color: #202124;
        }
        QLineEdit, QTextEdit, QComboBox, QTableWidget {
            background-color: #ffffff;
            color: #202124;
            border: 1px solid #cfcfcf;
        }
        QTableWidget {
            gridline-color: #bfc5cc;
            alternate-background-color: #fafafa;
            selection-background-color: #dbe7ff;
            selection-color: #202124;
        }
        QHeaderView::section {
            background-color: #efefef;
            color: #202124;
            border: 1px solid #d8d8d8;
            padding: 4px;
        }
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #c5c5c5;
            padding: 4px 10px;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        QGroupBox {
            border: 1px solid #d0d0d0;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
        }
        """
    )


class GeneratedUiPreviewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._tune_generated_layout()
        self._seed_demo_values()

    def _tune_generated_layout(self) -> None:
        main_layout = getattr(self.ui, "verticalLayout_2", None)
        line_items_section = getattr(self.ui, "wdg_lineItems", None)
        line_items_layout = getattr(self.ui, "verticalLayout", None)
        bottom_section = getattr(self.ui, "wdg_bottomSection", None)
        bottom_container = getattr(self.ui, "widget10", None)
        bottom_layout = getattr(self.ui, "horizontalLayout_17", None)
        remark_group = getattr(self.ui, "grp_remark", None)
        summary_actions = getattr(self.ui, "wdg_summaryActions", None)
        remark_editor = getattr(self.ui, "te_remark", None)
        if bottom_layout is None or remark_group is None or summary_actions is None:
            return

        self._tune_line_items_table()

        if main_layout is not None:
            main_layout.setSpacing(0)
            main_layout.setStretch(0, 0)
            main_layout.setStretch(1, 1)
            main_layout.setStretch(2, 0)

        if line_items_section is not None:
            line_items_section.setMinimumHeight(0)
            line_items_section.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        top_content = getattr(self.ui, "wdg_topContent", None)
        if top_content is not None:
            top_content.setMinimumHeight(81)
            top_content.setMaximumHeight(81)
        if line_items_layout is not None:
            line_items_layout.setContentsMargins(0, 0, 0, 0)
            line_items_layout.setSpacing(0)

        if bottom_section is not None:
            bottom_section.setMinimumHeight(156)
            bottom_section.setMaximumHeight(156)
        if bottom_container is not None:
            bottom_container.setGeometry(20, 0, 1481, 156)

        remark_group.setMaximumWidth(16777215)
        remark_group.setMinimumWidth(600)
        remark_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        remark_group.setMinimumHeight(152)
        remark_group.setMaximumHeight(152)
        remark_layout = getattr(self.ui, "horizontalLayout_9", None)
        if remark_layout is not None:
            remark_layout.setContentsMargins(6, 6, 6, 6)
        if remark_editor is not None:
            remark_editor.setMinimumHeight(114)
            remark_editor.setMaximumHeight(114)

        amount_summary = getattr(self.ui, "wdg_amountSummary", None)
        action_buttons = getattr(self.ui, "wdg_actionButtons", None)
        amount_layout = getattr(self.ui, "horizontalLayout_13", None)
        top_buttons_layout = getattr(self.ui, "horizontalLayout_14", None)
        lower_buttons_layout = getattr(self.ui, "horizontalLayout_15", None)
        button_rows_layout = getattr(self.ui, "horizontalLayout_16", None)
        top_group = getattr(self.ui, "widget14", None)

        summary_outer_width = 718
        summary_inner_width = 706
        button_group_width = 674

        if amount_summary is not None:
            amount_summary.setGeometry(10, 4, summary_inner_width, 54)
        if action_buttons is not None:
            action_buttons.setGeometry(10, 58, summary_inner_width, 82)
        if top_group is not None:
            top_group.setGeometry(4, 0, button_group_width, 80)

        if amount_layout is not None:
            amount_layout.setContentsMargins(0, 0, 0, 0)
            amount_layout.setSpacing(6)

        summary_specs = [
            ("wdg_productionAmountField", "widget11", "lbl_productionAmount", "le_productionAmount", 68, 152, 220),
            ("wdg_taxAmountField", "widget12", "lbl_taxAmount", "le_taxAmount", 56, 152, 218),
            ("wdg_totalAmountField", "widget13", "lbl_totalAmount", "le_totalAmount", 56, 152, 218),
        ]
        for field_name, inner_name, label_name, lineedit_name, label_width, lineedit_width, inner_width in summary_specs:
            field = getattr(self.ui, field_name, None)
            inner = getattr(self.ui, inner_name, None)
            label = getattr(self.ui, label_name, None)
            lineedit = getattr(self.ui, lineedit_name, None)
            if field is not None:
                field.setMinimumWidth(inner_width + 20)
                field.setMaximumWidth(inner_width + 20)
                field.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            if inner is not None:
                inner.setGeometry(10, 10, inner_width, 30)
            if label is not None:
                label.setMinimumWidth(label_width)
                label.setMaximumWidth(label_width)
                label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            if lineedit is not None:
                lineedit.setMinimumWidth(lineedit_width)
                lineedit.setMaximumWidth(lineedit_width)
                lineedit.setMinimumHeight(30)
                lineedit.setTextMargins(8, 0, 10, 0)
                lineedit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                lineedit.setAlignment(Qt.AlignmentFlag.AlignRight)

        for layout_name in ("horizontalLayout_10", "horizontalLayout_11", "horizontalLayout_12"):
            field_layout = getattr(self.ui, layout_name, None)
            if field_layout is not None:
                field_layout.setContentsMargins(0, 0, 0, 0)
                field_layout.setSpacing(6)

        button_specs = {
            "btn_open": 106,
            "btn_save": 106,
            "btn_reset": 106,
            "btn_billing": 106,
            "btn_subtotal": 106,
            "btn_calcuate": 106,
            "btn_import": 106,
            "btn_invoice": 106,
        }
        for button_name, width in button_specs.items():
            button = getattr(self.ui, button_name, None)
            if button is not None:
                button.setMinimumWidth(width)
                button.setMaximumWidth(width)
                button.setMinimumHeight(38)
                button.setMaximumHeight(38)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        if top_buttons_layout is not None:
            top_buttons_layout.setContentsMargins(0, 0, 0, 0)
            top_buttons_layout.setSpacing(4)
        if lower_buttons_layout is not None:
            lower_buttons_layout.setContentsMargins(0, 2, 0, 0)
            lower_buttons_layout.setSpacing(4)
        if button_rows_layout is not None:
            button_rows_layout.setContentsMargins(0, 0, 0, 0)
            button_rows_layout.setSpacing(0)

        summary_actions.setMinimumWidth(summary_outer_width)
        summary_actions.setMaximumWidth(summary_outer_width)
        summary_actions.setMinimumHeight(152)
        summary_actions.setMaximumHeight(152)
        summary_actions.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        bottom_layout.setAlignment(summary_actions, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        bottom_layout.setSpacing(2)
        bottom_layout.setStretch(0, 5)
        bottom_layout.setStretch(1, 0)

    def _tune_line_items_table(self) -> None:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return

        table.clear()
        table.setColumnCount(len(TABLE_HEADERS))
        table.setHorizontalHeaderLabels(TABLE_HEADERS)
        table.setRowCount(15)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.setShowGrid(True)
        table.setCornerButtonEnabled(False)
        table.setSelectionBehavior(table.SelectionBehavior.SelectItems)
        table.setSelectionMode(table.SelectionMode.SingleSelection)
        table.setMinimumHeight(418)
        table.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #b9c0c7;
                background: #ffffff;
                gridline-color: #bcc3ca;
                alternate-background-color: #fafafa;
                selection-background-color: #dbe7ff;
                selection-color: #202124;
            }
            QTableWidget::item {
                padding: 4px 6px;
                border-right: 1px solid #d7dce1;
                border-bottom: 1px solid #d7dce1;
            }
            QHeaderView::section {
                background: #ececec;
                color: #202124;
                border-top: 1px solid #c4c8cc;
                border-left: 1px solid #c4c8cc;
                border-right: 1px solid #c4c8cc;
                border-bottom: 1px solid #adb3b9;
                padding: 6px 4px;
                font-weight: 700;
            }
            """
        )

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setMinimumSectionSize(28)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStretchLastSection(False)
        header.setHighlightSections(False)
        header.setFixedHeight(34)

        v_header = table.verticalHeader()
        v_header.setVisible(False)
        v_header.setDefaultSectionSize(36)
        v_header.setMinimumSectionSize(36)

        for index, width in enumerate(TABLE_COLUMN_WIDTHS):
            table.setColumnWidth(index, width)

        for row in range(table.rowCount()):
            table.setRowHeight(row, 36)

    def _make_table_item(self, text: str, column: int) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setForeground(QColor("#202124"))

        if column == X_COLUMN_INDEX:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setBackground(QColor("#efefef"))
            item.setForeground(QColor("#6b7280"))
        elif column in NUMERIC_COLUMN_INDEXES:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        elif column in SELECT_LIKE_COLUMN_INDEXES:
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        return item

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
            ["主舞台背板輸出裱板", "500", "x", "240", "2", "PVC 貼圖", "冷裱 + 修邊", "KT 板", "5mm", "含收邊黑膠帶", "2", "80", "2800", "5600", "300"],
            ["入口拱門雙面輸出", "320", "x", "260", "1", "防水帆布", "車縫 + 打銅扣", "塑鋁板", "3mm", "雙面對裱", "1", "22", "6500", "6500", "0"],
            ["指引立牌裱板", "90", "x", "180", "6", "PP 相紙", "冷裱", "豪卡板", "10mm", "含腳架孔位", "6", "67.5", "950", "5700", "480"],
            ["服務台桌裙", "240", "x", "75", "1", "單透布", "包邊車縫", "珍珠板", "2mm", "魔鬼氈 + 補強條", "1", "12.5", "1800", "1800", "180"],
        ]
        if hasattr(self.ui, "tbl_lineItems"):
            table = self.ui.tbl_lineItems
            table.clearContents()
            for row_idx, row in enumerate(sample_rows):
                for col_idx, value in enumerate(row):
                    table.setItem(row_idx, col_idx, self._make_table_item(value, col_idx))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshot", type=Path, help="Save a screenshot to this path and exit.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    app = QApplication(sys.argv)
    apply_light_preview_theme(app)
    window = GeneratedUiPreviewWindow()
    window.show()

    if args.screenshot:
        target = args.screenshot.expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)

        def save_and_quit() -> None:
            window.repaint()
            app.processEvents()
            window.grab().save(str(target))
            app.quit()

        QTimer.singleShot(250, save_and_quit)

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
