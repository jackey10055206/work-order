from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, QTimer, Qt
from PySide6.QtGui import QColor, QKeyEvent, QPalette, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QCompleter,
    QHeaderView,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QStyle,
    QStyleFactory,
    QStyleOptionHeader,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from ui_project_generated import Ui_MainWindow

try:
    import pymysql
except ImportError:  # pragma: no cover - fallback when PyMySQL is unavailable
    pymysql = None


TABLE_HEADERS = [
    "製作項目",
    "寬度",
    "x",
    "長度",
    "數量",
    "材質",
    "冷裱加工",
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
TABLE_COLUMN_WIDTHS = [196, 82, 36, 82, 68, 140, 136, 126, 108, 144, 68, 84, 88, 92, 104]
X_COLUMN_INDEX = 2
TABLE_LOCKED_COLUMN_INDEXES = {11, 13}
TABLE_SKIP_FOCUS_COLUMN_INDEXES = {X_COLUMN_INDEX, *TABLE_LOCKED_COLUMN_INDEXES}
NUMERIC_COLUMN_INDEXES = {1, 3, 4, 10, 11, 12, 13, 14}
SELECT_LIKE_COLUMN_INDEXES = {0, 5, 6, 7, 8, 9}
SUMMARY_LOCKED_FIELD_NAMES = {"le_productionAmount", "le_taxAmount", "le_totalAmount"}
COMBO_COLUMN_OPTIONS = {
    0: ["大圖輸出", "裱板施工", "立牌製作", "桌裙布置", "展場貼圖"],
    5: ["PVC 貼圖", "PP 相紙", "防水帆布", "單透布", "背膠海報"],
    6: ["冷裱", "冷裱 + 修邊", "不上膜", "雙面對裱", "包邊處理"],
    7: ["KT 板", "豪卡板", "塑鋁板", "珍珠板", "發泡板"],
    8: ["1mm", "2mm", "3mm", "5mm", "10mm"],
    9: ["無", "黑膠帶收邊", "腳架孔位", "魔鬼氈", "補強條"],
}
COMBO_COLUMN_GROUPS = {
    0: "production_item",
    5: "material",
    6: "lamination",
    7: "board_type",
    8: "board_thickness",
    9: "extra_material",
}
DB_V2_CONFIG = {
    "host": os.environ.get("WORK_ORDER_V2_DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("WORK_ORDER_V2_DB_PORT", "3308")),
    "user": os.environ.get("WORK_ORDER_V2_DB_USER", "workorder_v2"),
    "password": os.environ.get("WORK_ORDER_V2_DB_PASSWORD", "123456"),
    "database": os.environ.get("WORK_ORDER_V2_DB_NAME", "work_order_v2"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor if pymysql else None,
}
HEADER_YELLOW_COLUMNS = range(0, 11)
HEADER_PURPLE_COLUMNS = range(11, len(TABLE_HEADERS))
HEADER_YELLOW_BG = QColor("#f6e7a6")
HEADER_YELLOW_FG = QColor("#3f3110")
HEADER_PURPLE_BG = QColor("#c9b1ea")
HEADER_PURPLE_FG = QColor("#31204a")
SUMMARY_LABEL_BG = "#e8dcf8"
SUMMARY_LABEL_FG = "#4b3566"
SUMMARY_LABEL_BORDER = "#c9b1ea"
HEADER_DEFAULT_BG = QColor("#ececec")
HEADER_DEFAULT_FG = QColor("#202124")
HEADER_BORDER_TOP = QColor("#c4c8cc")
HEADER_BORDER_BOTTOM = QColor("#adb3b9")


def load_combo_options_from_v2() -> dict[int, list[str]]:
    if pymysql is None:
        return {column: list(options) for column, options in COMBO_COLUMN_OPTIONS.items()}

    query = """
        SELECT option_group, item_name
        FROM option_items
        WHERE is_active = 1
          AND option_group IN (%s, %s, %s, %s, %s, %s)
        ORDER BY option_group, sort_order, id
    """
    options_by_group = {group: [] for group in COMBO_COLUMN_GROUPS.values()}

    try:
        connect_kwargs = {key: value for key, value in DB_V2_CONFIG.items() if value is not None}
        with pymysql.connect(**connect_kwargs) as conn:
            with conn.cursor() as cur:
                cur.execute(query, tuple(COMBO_COLUMN_GROUPS.values()))
                for row in cur.fetchall():
                    group = row["option_group"]
                    item_name = (row["item_name"] or "").strip()
                    if item_name:
                        options_by_group.setdefault(group, []).append(item_name)
    except Exception:
        return {column: list(options) for column, options in COMBO_COLUMN_OPTIONS.items()}

    loaded_options: dict[int, list[str]] = {}
    for column, group in COMBO_COLUMN_GROUPS.items():
        loaded_options[column] = options_by_group.get(group) or list(COMBO_COLUMN_OPTIONS[column])
    return loaded_options


class BandHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None) -> None:
        super().__init__(orientation, parent)
        self.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setHighlightSections(False)

    def paintSection(self, painter: QPainter, rect, logical_index: int) -> None:
        if not rect.isValid():
            return

        painter.save()

        if logical_index in HEADER_YELLOW_COLUMNS:
            bg = HEADER_YELLOW_BG
            fg = HEADER_YELLOW_FG
        elif logical_index in HEADER_PURPLE_COLUMNS:
            bg = HEADER_PURPLE_BG
            fg = HEADER_PURPLE_FG
        else:
            bg = HEADER_DEFAULT_BG
            fg = HEADER_DEFAULT_FG

        painter.fillRect(rect, bg)
        painter.setPen(HEADER_BORDER_TOP)
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.setPen(HEADER_BORDER_BOTTOM)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        option = QStyleOptionHeader()
        self.initStyleOption(option)
        option.rect = rect.adjusted(4, 0, -4, 0)
        option.section = logical_index
        option.text = self.model().headerData(logical_index, self.orientation(), Qt.ItemDataRole.DisplayRole) or ""
        option.state &= ~QStyle.StateFlag.State_Sunken
        painter.setPen(fg)
        painter.drawText(option.rect, int(Qt.AlignmentFlag.AlignCenter), option.text)

        painter.restore()


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


class TableCellTabNavigator(QObject):
    def __init__(self, table: QTableWidget) -> None:
        super().__init__(table)
        self.table = table

    def register_widget(self, widget: QWidget, row: int, column: int) -> None:
        widget.setProperty("table_row", row)
        widget.setProperty("table_column", column)
        widget.installEventFilter(self)

        if widget.focusPolicy() == Qt.FocusPolicy.NoFocus and column not in TABLE_SKIP_FOCUS_COLUMN_INDEXES:
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        if isinstance(widget, QComboBox):
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            line_edit = widget.lineEdit()
            if line_edit is not None:
                line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                self.register_widget(line_edit, row, column)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() != QEvent.Type.KeyPress or not isinstance(event, QKeyEvent):
            return super().eventFilter(watched, event)

        if event.key() == Qt.Key.Key_Backtab:
            return self._focus_relative_cell(watched, forward=False)
        if event.key() == Qt.Key.Key_Tab:
            forward = not bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
            return self._focus_relative_cell(watched, forward=forward)

        return super().eventFilter(watched, event)

    def _focus_relative_cell(self, watched: QObject, *, forward: bool) -> bool:
        row = watched.property("table_row")
        column = watched.property("table_column")
        if row is None or column is None:
            return False

        next_cell = self._find_next_editable_cell(int(row), int(column), forward=forward)
        if next_cell is None:
            return False

        next_row, next_column = next_cell
        self.table.setCurrentCell(next_row, next_column)
        QTimer.singleShot(0, lambda: self._focus_cell(next_row, next_column))
        return True

    def _find_next_editable_cell(self, row: int, column: int, *, forward: bool) -> tuple[int, int] | None:
        column_count = self.table.columnCount()
        row_count = self.table.rowCount()
        if column_count <= 0 or row_count <= 0:
            return None

        flat_index = row * column_count + column
        step = 1 if forward else -1
        next_index = flat_index + step
        max_index = row_count * column_count

        while 0 <= next_index < max_index:
            next_row, next_column = divmod(next_index, column_count)
            if self._is_focusable_cell(next_row, next_column):
                return next_row, next_column
            next_index += step
        return None

    def _is_focusable_cell(self, row: int, column: int) -> bool:
        if column in TABLE_SKIP_FOCUS_COLUMN_INDEXES:
            return False

        cell_widget = self.table.cellWidget(row, column)
        if cell_widget is not None:
            return cell_widget.isEnabled() and cell_widget.focusPolicy() != Qt.FocusPolicy.NoFocus

        item = self.table.item(row, column)
        if item is None:
            return False
        flags = item.flags()
        return bool((flags & Qt.ItemFlag.ItemIsEnabled) and (flags & Qt.ItemFlag.ItemIsEditable))

    def _focus_cell(self, row: int, column: int) -> None:
        cell_widget = self.table.cellWidget(row, column)
        if cell_widget is not None:
            focus_target = self._preferred_focus_target(cell_widget)
            if focus_target is not None:
                focus_target.setFocus(Qt.FocusReason.TabFocusReason)
            return

        self.table.editItem(self.table.item(row, column))

    def _preferred_focus_target(self, widget: QWidget) -> QWidget | None:
        if isinstance(widget, QComboBox):
            line_edit = widget.lineEdit()
            if line_edit is not None:
                line_edit.selectAll()
                return line_edit
            return widget

        if isinstance(widget, QLineEdit):
            widget.selectAll()
            return widget

        focus_widget = widget.focusProxy()
        if isinstance(focus_widget, QWidget):
            return focus_widget
        if widget.focusPolicy() != Qt.FocusPolicy.NoFocus:
            return widget
        return widget.findChild(QWidget)


class GeneratedUiPreviewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.combo_column_options = load_combo_options_from_v2()
        self.table_tab_navigator: TableCellTabNavigator | None = None
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
                label.setStyleSheet(
                    f"background-color: {SUMMARY_LABEL_BG}; color: {SUMMARY_LABEL_FG}; "
                    f"border: 1px solid {SUMMARY_LABEL_BORDER}; border-radius: 4px; "
                    "font-weight: 600; padding: 0 10px;"
                )
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if lineedit is not None:
                lineedit.setMinimumWidth(lineedit_width)
                lineedit.setMaximumWidth(lineedit_width)
                lineedit.setMinimumHeight(30)
                lineedit.setTextMargins(8, 0, 10, 0)
                lineedit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                lineedit.setAlignment(Qt.AlignmentFlag.AlignRight)
                if lineedit_name in SUMMARY_LOCKED_FIELD_NAMES:
                    lineedit.setReadOnly(True)
                    lineedit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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
        self.table_tab_navigator = TableCellTabNavigator(table)
        table.setHorizontalHeader(BandHeaderView(Qt.Orientation.Horizontal, table))
        table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self._apply_line_items_header_colors(table)
        table.setRowCount(15)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.setShowGrid(True)
        table.setCornerButtonEnabled(False)
        table.setSelectionBehavior(table.SelectionBehavior.SelectItems)
        table.setSelectionMode(table.SelectionMode.SingleSelection)
        table.setTabKeyNavigation(False)
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

    def _apply_line_items_header_colors(self, table) -> None:
        for column in HEADER_YELLOW_COLUMNS:
            item = table.horizontalHeaderItem(column)
            if item is not None:
                item.setBackground(HEADER_YELLOW_BG)
                item.setForeground(HEADER_YELLOW_FG)

        for column in HEADER_PURPLE_COLUMNS:
            item = table.horizontalHeaderItem(column)
            if item is not None:
                item.setBackground(HEADER_PURPLE_BG)
                item.setForeground(HEADER_PURPLE_FG)

    def _make_table_item(self, text: str, column: int) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setForeground(QColor("#202124"))

        if column == X_COLUMN_INDEX:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setBackground(QColor("#efefef"))
            item.setForeground(QColor("#6b7280"))
        elif column in TABLE_LOCKED_COLUMN_INDEXES:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setBackground(QColor("#f5f5f5"))
            item.setForeground(QColor("#6b7280"))
        elif column in NUMERIC_COLUMN_INDEXES:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        elif column in SELECT_LIKE_COLUMN_INDEXES:
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        return item

    def _make_combo_box(self, column: int, current_text: str) -> QComboBox:
        combo = QComboBox()
        combo.addItems(self.combo_column_options[column])
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setFrame(True)
        combo.setMaxVisibleItems(8)
        combo.setMinimumHeight(28)
        combo.setMaximumHeight(28)

        completer = QCompleter(combo.model(), combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(completer)

        current_index = combo.findText(current_text)
        if current_index >= 0:
            combo.setCurrentIndex(current_index)
        elif current_text:
            combo.setEditText(current_text)
        else:
            combo.setCurrentIndex(-1)
            combo.clearEditText()
        return combo

    def _register_table_cell_widget(self, widget: QWidget, row: int, column: int) -> QWidget:
        if self.table_tab_navigator is not None:
            self.table_tab_navigator.register_widget(widget, row, column)
        return widget

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

        def option_at(column: int, index: int, fallback: str = "") -> str:
            options = self.combo_column_options.get(column, [])
            if options:
                return options[min(index, len(options) - 1)]
            return fallback

        sample_rows = [
            [option_at(0, 0, "大圖輸出"), "500", "x", "240", "2", option_at(5, 0, "PVC 貼圖"), option_at(6, 0, "冷裱 + 修邊"), option_at(7, 0, "KT 板"), option_at(8, 0, "5mm"), option_at(9, 0, "黑膠帶收邊"), "2", "80", "2800", "5600", "300"],
            [option_at(0, 1, "展場貼圖"), "320", "x", "260", "1", option_at(5, 1, "防水帆布"), option_at(6, 1, "雙面對裱"), option_at(7, 1, "塑鋁板"), option_at(8, 1, "3mm"), option_at(9, 1, "無"), "1", "22", "6500", "6500", "0"],
            [option_at(0, 2, "立牌製作"), "90", "x", "180", "6", option_at(5, 2, "PP 相紙"), option_at(6, 2, "冷裱"), option_at(7, 2, "豪卡板"), option_at(8, 2, "10mm"), option_at(9, 2, "腳架孔位"), "6", "67.5", "950", "5700", "480"],
            [option_at(0, 3, "桌裙布置"), "240", "x", "75", "1", option_at(5, 3, "單透布"), option_at(6, 3, "包邊處理"), option_at(7, 3, "珍珠板"), option_at(8, 3, "2mm"), option_at(9, 3, "魔鬼氈"), "1", "12.5", "1800", "1800", "180"],
        ]
        if hasattr(self.ui, "tbl_lineItems"):
            table = self.ui.tbl_lineItems
            table.clearContents()
            for row_idx in range(table.rowCount()):
                row = sample_rows[row_idx] if row_idx < len(sample_rows) else ["", "", "x", "", "", "", "", "", "", "", "", "", "", "", ""]
                for col_idx, value in enumerate(row):
                    if col_idx in COMBO_COLUMN_OPTIONS:
                        table.setCellWidget(
                            row_idx,
                            col_idx,
                            self._register_table_cell_widget(self._make_combo_box(col_idx, value), row_idx, col_idx),
                        )
                        placeholder = self._make_table_item("", col_idx)
                        placeholder.setFlags(placeholder.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                        table.setItem(row_idx, col_idx, placeholder)
                    else:
                        table.setItem(row_idx, col_idx, self._make_table_item(value, col_idx))
                table.setRowHeight(row_idx, 36)


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
