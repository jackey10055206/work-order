from __future__ import annotations

import argparse
import os
import subprocess
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, QTimer, Qt
from PySide6.QtGui import QColor, QKeyEvent, QPalette, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QCompleter,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QStyle,
    QStyleFactory,
    QStyleOptionHeader,
    QStyledItemDelegate,
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
LENGTH_COLUMN_INDEX = 3
TABLE_LOCKED_COLUMN_INDEXES = {11, 13}
MIDDLE_TAB_COLUMN_ORDER = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]
TABLE_SKIP_FOCUS_COLUMN_INDEXES = {X_COLUMN_INDEX, *TABLE_LOCKED_COLUMN_INDEXES}
DEFAULT_LINE_ITEM_ROW_COUNT = 15
BLANK_LINE_ROW_TEMPLATE = ["", "", "x", "", "", "", "", "", "", "", "", "", "", "", ""]
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


def resolve_build_commit_hash() -> str:
    repo_root = Path(__file__).resolve().parents[2]
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or "unknown"
    except Exception:
        return "unknown"


BUILD_COMMIT_HASH = resolve_build_commit_hash()
BUILD_LABEL_TEXT = f"build: {BUILD_COMMIT_HASH}"


def _connect_kwargs() -> dict:
    return {key: value for key, value in DB_V2_CONFIG.items() if value is not None}


def load_clients_from_v2() -> list[dict[str, str | int | None]]:
    if pymysql is None:
        return []

    query = """
        SELECT id, short_name, full_name, phone, address
        FROM clients
        WHERE is_active = 1
        ORDER BY short_name, id
    """
    try:
        with pymysql.connect(**_connect_kwargs()) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
    except Exception:
        return []

    normalized_rows: list[dict[str, str | int | None]] = []
    for row in rows:
        short_name = (row.get("short_name") or "").strip()
        if not short_name:
            continue
        normalized_rows.append(
            {
                "id": row.get("id"),
                "short_name": short_name,
                "full_name": (row.get("full_name") or "").strip() or None,
                "phone": (row.get("phone") or "").strip() or None,
                "address": (row.get("address") or "").strip() or None,
            }
        )
    return normalized_rows


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
        with pymysql.connect(**_connect_kwargs()) as conn:
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
    def __init__(self, table: QTableWidget, parent_window: "GeneratedUiPreviewWindow | None" = None) -> None:
        super().__init__(table)
        self.table = table
        self.parent_window = parent_window
        self.column_order = [column for column in MIDDLE_TAB_COLUMN_ORDER if column < table.columnCount()]

    def redirect_x_cell(self, row: int) -> bool:
        if row < 0 or row >= self.table.rowCount():
            return False
        if not self._is_focusable_cell(row, LENGTH_COLUMN_INDEX):
            return False

        self.table.setCurrentCell(row, LENGTH_COLUMN_INDEX)
        QTimer.singleShot(0, lambda: self._focus_cell(row, LENGTH_COLUMN_INDEX))
        return True

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

        row = int(row)
        column = int(column)
        if column == X_COLUMN_INDEX:
            return self.redirect_x_cell(row)

        next_cell = self._find_next_editable_cell(row, column, forward=forward)
        if next_cell is None:
            if self.parent_window is not None:
                self.parent_window.focus_after_table(forward=forward)
                return True
            return False

        next_row, next_column = next_cell
        self.table.setCurrentCell(next_row, next_column)
        QTimer.singleShot(0, lambda: self._focus_cell(next_row, next_column))
        return True

    def _find_next_editable_cell(self, row: int, column: int, *, forward: bool) -> tuple[int, int] | None:
        row_count = self.table.rowCount()
        if row_count <= 0 or not self.column_order:
            return None

        if forward:
            return self._find_next_cell_forward(row, column)
        return self._find_next_cell_backward(row, column)

    def _find_next_cell_forward(self, row: int, column: int) -> tuple[int, int] | None:
        start_row = max(row, 0)
        if start_row >= self.table.rowCount():
            return None

        current_position = self._column_position(column)
        for row_index in range(start_row, self.table.rowCount()):
            columns = self.column_order
            if row_index == start_row and current_position is not None:
                columns = self.column_order[current_position + 1 :]
            for candidate_column in columns:
                if self._is_focusable_cell(row_index, candidate_column):
                    return row_index, candidate_column
            current_position = None
        return None

    def _find_next_cell_backward(self, row: int, column: int) -> tuple[int, int] | None:
        start_row = min(row, self.table.rowCount() - 1)
        if start_row < 0:
            return None

        current_position = self._column_position(column)
        for row_index in range(start_row, -1, -1):
            columns = list(reversed(self.column_order))
            if row_index == start_row and current_position is not None:
                columns = list(reversed(self.column_order[:current_position]))
            for candidate_column in columns:
                if self._is_focusable_cell(row_index, candidate_column):
                    return row_index, candidate_column
            current_position = None
        return None

    def _column_position(self, column: int) -> int | None:
        try:
            return self.column_order.index(column)
        except ValueError:
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
            # Table 內 editable QComboBox 若直接把焦點代理到內部 lineEdit，
            # Qt 會把整個 combo 視為已經「進入又離開」，導致下一次 Tab
            # 直接跳過後續同列的 combo 欄位。這裡必須停在 combo 本體，
            # 才能讓材質/冷裱加工/板材種類/板材厚度/其他備料都成為可停留點。
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


class TableItemDelegate(QStyledItemDelegate):
    def __init__(self, navigator: TableCellTabNavigator, parent: QTableWidget) -> None:
        super().__init__(parent)
        self.navigator = navigator

    def createEditor(self, parent: QWidget, option, index):
        if not index.isValid() or index.column() in TABLE_SKIP_FOCUS_COLUMN_INDEXES:
            return None

        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QWidget):
            self.navigator.register_widget(editor, index.row(), index.column())
        return editor


def normalize_line_edit_value(widget: object) -> str | None:
    if isinstance(widget, QLineEdit):
        value = widget.text().strip()
        return value or None
    return None


def normalize_text_edit_value(widget: object) -> str | None:
    value = widget.toPlainText().strip() if widget is not None and hasattr(widget, "toPlainText") else ""
    return value or None


def parse_decimal_or_none(raw_value: str | None) -> Decimal | None:
    if raw_value is None:
        return None
    normalized = raw_value.strip().replace(",", "")
    if not normalized:
        return None
    try:
        return Decimal(normalized)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"數值格式錯誤：{raw_value}") from exc


def parse_int_or_none(raw_value: str | None) -> int | None:
    decimal_value = parse_decimal_or_none(raw_value)
    if decimal_value is None:
        return None
    if decimal_value != decimal_value.to_integral_value():
        raise ValueError(f"整數欄位不可輸入小數：{raw_value}")
    return int(decimal_value)


def format_decimal_for_ui(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Decimal):
        normalized = format(value.normalize(), "f")
        return "0" if normalized == "-0" else normalized
    return str(value)


def load_option_item_ids_from_v2() -> dict[str, dict[str, int]]:
    lookup = {group: {} for group in COMBO_COLUMN_GROUPS.values()}
    if pymysql is None:
        return lookup

    query = """
        SELECT id, option_group, item_name
        FROM option_items
        WHERE is_active = 1
          AND option_group IN (%s, %s, %s, %s, %s, %s)
        ORDER BY option_group, sort_order, id
    """
    try:
        with pymysql.connect(**_connect_kwargs()) as conn:
            with conn.cursor() as cur:
                cur.execute(query, tuple(COMBO_COLUMN_GROUPS.values()))
                for row in cur.fetchall():
                    group = str(row["option_group"])
                    item_name = (row.get("item_name") or "").strip()
                    item_id = row.get("id")
                    if group and item_name and item_id is not None:
                        lookup.setdefault(group, {})[item_name] = int(item_id)
    except Exception:
        return lookup

    return lookup


class GeneratedUiPreviewWindow(QMainWindow):
    TOP_TAB_ORDER = [
        "le_worknum",
        "cb_customerName",
        "le_contactName",
        "le_startTime",
        "le_caseName",
        "le_phone",
        "lle_address",
        "le_endTime",
    ]
    BOTTOM_TAB_ORDER = [
        "te_remark",
        "btn_open",
        "btn_save",
        "btn_reset",
        "btn_billing",
        "btn_subtotal",
        "btn_calcuate",
        "btn_import",
        "btn_invoice",
    ]

    def __init__(self) -> None:
        super().__init__()
        self.combo_column_options = load_combo_options_from_v2()
        self.option_item_ids_by_group = load_option_item_ids_from_v2()
        self.option_item_names_by_group_and_id = self._invert_option_item_lookup(self.option_item_ids_by_group)
        self.clients = load_clients_from_v2()
        self.client_rows_by_short_name = {
            str(row["short_name"]): row for row in self.clients if row.get("short_name")
        }
        self._last_auto_filled_phone = ""
        self._last_auto_filled_address = ""
        self.table_tab_navigator: TableCellTabNavigator | None = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.build_label: QLabel | None = None
        self._suspend_auto_append_checks = False
        self._configure_customer_name_combo()
        self._tune_generated_layout()
        self._initialize_blank_work_order()
        self._configure_save_flow()
        self._configure_open_flow()
        self._configure_focus_chain()

    def _configure_customer_name_combo(self) -> None:
        combo = getattr(self.ui, "cb_customerName", None)
        if not isinstance(combo, QComboBox):
            return

        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setMaxVisibleItems(8)
        combo.clear()
        for row in self.clients:
            combo.addItem(str(row["short_name"]), row)

        completer = QCompleter(combo.model(), combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(completer)
        combo.currentTextChanged.connect(self._handle_customer_name_changed)

    def _handle_customer_name_changed(self, customer_name: str) -> None:
        row = self.client_rows_by_short_name.get(customer_name.strip())
        if row is None:
            return
        self._apply_customer_contact_defaults(row)

    @staticmethod
    def _invert_option_item_lookup(option_item_ids_by_group: dict[str, dict[str, int]]) -> dict[str, dict[int, str]]:
        return {
            group: {item_id: item_name for item_name, item_id in items.items()}
            for group, items in option_item_ids_by_group.items()
        }

    def _configure_save_flow(self) -> None:
        save_button = getattr(self.ui, "btn_save", None)
        if save_button is not None:
            save_button.clicked.connect(self._handle_save_clicked)

    def _configure_open_flow(self) -> None:
        open_button = getattr(self.ui, "btn_open", None)
        if open_button is not None:
            open_button.clicked.connect(self._handle_open_clicked)

    def _set_status_message(self, message: str, timeout_ms: int = 8000) -> None:
        self.statusBar().showMessage(message, timeout_ms)

    def _header_payload(self) -> dict[str, str | int | None]:
        customer_name = ""
        customer_combo = getattr(self.ui, "cb_customerName", None)
        if isinstance(customer_combo, QComboBox):
            customer_name = customer_combo.currentText().strip()

        client_row = self.client_rows_by_short_name.get(customer_name) if customer_name else None
        if customer_name and client_row is None:
            raise ValueError(f"客戶「{customer_name}」不存在 clients，請先建立客戶再儲存。")

        work_number = normalize_line_edit_value(getattr(self.ui, "le_worknum", None))
        if not work_number:
            raise ValueError("工單號不可為空。")

        return {
            "work_number": work_number,
            "case_name": normalize_line_edit_value(getattr(self.ui, "le_caseName", None)),
            "client_id": client_row.get("id") if client_row else None,
            "company_phone": normalize_line_edit_value(getattr(self.ui, "le_phone", None)),
            "contact_name": normalize_line_edit_value(getattr(self.ui, "le_contactName", None)),
            "work_time": normalize_line_edit_value(getattr(self.ui, "le_startTime", None)),
            "cleanup_time": normalize_line_edit_value(getattr(self.ui, "le_endTime", None)),
            "work_address": normalize_line_edit_value(getattr(self.ui, "lle_address", None)),
            "remark": normalize_text_edit_value(getattr(self.ui, "te_remark", None)),
            "status": "draft",
        }

    def _table_cell_text(self, row: int, column: int) -> str:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return ""

        cell_widget = table.cellWidget(row, column)
        if isinstance(cell_widget, QComboBox):
            return cell_widget.currentText().strip()
        if isinstance(cell_widget, QLineEdit):
            return cell_widget.text().strip()

        item = table.item(row, column)
        return item.text().strip() if item is not None else ""

    def _line_row_has_meaningful_data(self, row: int) -> bool:
        meaningful_columns = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for column in meaningful_columns:
            if self._table_cell_text(row, column):
                return True
        return False

    def _lookup_option_item_id(self, option_group: str, item_name: str, row_number: int, column_label: str) -> int | None:
        normalized_name = item_name.strip()
        if not normalized_name:
            return None

        item_id = self.option_item_ids_by_group.get(option_group, {}).get(normalized_name)
        if item_id is None:
            raise ValueError(
                f"第 {row_number} 列「{column_label}」找不到 option_items 對應：group={option_group}, item_name={normalized_name}"
            )
        return item_id

    def _collect_line_payloads(self) -> list[dict[str, object | None]]:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return []

        line_payloads: list[dict[str, object | None]] = []
        for row in range(table.rowCount()):
            row_number = row + 1
            if not self._line_row_has_meaningful_data(row):
                continue

            production_item = self._table_cell_text(row, 0)
            width_mm = self._table_cell_text(row, 1)
            height_mm = self._table_cell_text(row, 3)
            quantity = self._table_cell_text(row, 4)
            material = self._table_cell_text(row, 5)
            lamination = self._table_cell_text(row, 6)
            board_type = self._table_cell_text(row, 7)
            board_thickness = self._table_cell_text(row, 8)
            extra_material = self._table_cell_text(row, 9)
            extra_material_quantity = self._table_cell_text(row, 10)
            cbm = self._table_cell_text(row, 11)
            cbm_unit_price = self._table_cell_text(row, 12)
            line_total = self._table_cell_text(row, 13)
            extra_material_total = self._table_cell_text(row, 14)

            line_payloads.append(
                {
                    "line_no": row_number,
                    "production_item_id": self._lookup_option_item_id("production_item", production_item, row_number, "製作項目"),
                    "width_mm": parse_decimal_or_none(width_mm),
                    "height_mm": parse_decimal_or_none(height_mm),
                    "quantity": parse_int_or_none(quantity),
                    "material_id": self._lookup_option_item_id("material", material, row_number, "材質"),
                    "lamination_id": self._lookup_option_item_id("lamination", lamination, row_number, "冷裱加工"),
                    "board_type_id": self._lookup_option_item_id("board_type", board_type, row_number, "板材種類"),
                    "board_thickness_id": self._lookup_option_item_id("board_thickness", board_thickness, row_number, "板材厚度"),
                    "extra_material_id": self._lookup_option_item_id("extra_material", extra_material, row_number, "其他備料"),
                    "extra_material_quantity": parse_int_or_none(extra_material_quantity),
                    "cbm": parse_decimal_or_none(cbm),
                    "cbm_unit_price": parse_decimal_or_none(cbm_unit_price),
                    "line_total": parse_decimal_or_none(line_total),
                    "extra_material_total": parse_decimal_or_none(extra_material_total),
                }
            )

        return line_payloads

    def _upsert_work_order_header(self, cur, payload: dict[str, str | int | None]) -> int:
        insert_sql = """
            INSERT INTO work_orders (
                work_number, case_name, client_id, company_phone,
                contact_name, work_time, cleanup_time, work_address, remark, status
            ) VALUES (
                %(work_number)s, %(case_name)s, %(client_id)s, %(company_phone)s,
                %(contact_name)s, %(work_time)s, %(cleanup_time)s, %(work_address)s, %(remark)s, %(status)s
            )
            ON DUPLICATE KEY UPDATE
                case_name = VALUES(case_name),
                client_id = VALUES(client_id),
                company_phone = VALUES(company_phone),
                contact_name = VALUES(contact_name),
                work_time = VALUES(work_time),
                cleanup_time = VALUES(cleanup_time),
                work_address = VALUES(work_address),
                remark = VALUES(remark),
                status = VALUES(status),
                id = LAST_INSERT_ID(id)
        """
        cur.execute(insert_sql, payload)
        return int(cur.lastrowid)

    def _replace_work_order_lines(self, cur, work_order_id: int, line_payloads: list[dict[str, object | None]]) -> None:
        cur.execute("DELETE FROM work_order_lines WHERE work_order_id = %s", (work_order_id,))
        if not line_payloads:
            return

        insert_sql = """
            INSERT INTO work_order_lines (
                work_order_id, line_no, production_item_id, width_mm, height_mm, quantity,
                material_id, lamination_id, board_type_id, board_thickness_id,
                extra_material_id, extra_material_quantity, cbm, cbm_unit_price,
                line_total, extra_material_total
            ) VALUES (
                %(work_order_id)s, %(line_no)s, %(production_item_id)s, %(width_mm)s, %(height_mm)s, %(quantity)s,
                %(material_id)s, %(lamination_id)s, %(board_type_id)s, %(board_thickness_id)s,
                %(extra_material_id)s, %(extra_material_quantity)s, %(cbm)s, %(cbm_unit_price)s,
                %(line_total)s, %(extra_material_total)s
            )
        """
        rows = []
        for payload in line_payloads:
            row_payload = dict(payload)
            row_payload["work_order_id"] = work_order_id
            rows.append(row_payload)
        cur.executemany(insert_sql, rows)

    def save_header_to_work_orders(self) -> int:
        if pymysql is None:
            raise RuntimeError("缺少 PyMySQL，無法儲存到 work_order_v2。")

        payload = self._header_payload()
        with pymysql.connect(**_connect_kwargs()) as conn:
            with conn.cursor() as cur:
                work_order_id = self._upsert_work_order_header(cur, payload)
            conn.commit()
        return work_order_id

    def _fetch_work_order_bundle(self, work_number: str) -> tuple[dict[str, object], list[dict[str, object]]]:
        if pymysql is None:
            raise RuntimeError("缺少 PyMySQL，無法讀取 work_order_v2。")
        normalized_work_number = work_number.strip()
        if not normalized_work_number:
            raise ValueError("請先輸入工單號再開啟。")

        header_sql = """
            SELECT
                wo.id,
                wo.work_number,
                wo.case_name,
                wo.client_id,
                c.short_name AS client_short_name,
                wo.company_phone,
                wo.contact_name,
                wo.work_time,
                wo.cleanup_time,
                wo.work_address,
                wo.remark,
                wo.status
            FROM work_orders wo
            LEFT JOIN clients c ON c.id = wo.client_id
            WHERE wo.work_number = %s
            LIMIT 1
        """
        line_sql = """
            SELECT
                wol.line_no,
                wol.width_mm,
                wol.height_mm,
                wol.quantity,
                wol.extra_material_quantity,
                wol.cbm,
                wol.cbm_unit_price,
                wol.line_total,
                wol.extra_material_total,
                pi.item_name AS production_item_name,
                mi.item_name AS material_name,
                li.item_name AS lamination_name,
                bti.item_name AS board_type_name,
                bthi.item_name AS board_thickness_name,
                emi.item_name AS extra_material_name
            FROM work_order_lines wol
            LEFT JOIN option_items pi ON pi.id = wol.production_item_id
            LEFT JOIN option_items mi ON mi.id = wol.material_id
            LEFT JOIN option_items li ON li.id = wol.lamination_id
            LEFT JOIN option_items bti ON bti.id = wol.board_type_id
            LEFT JOIN option_items bthi ON bthi.id = wol.board_thickness_id
            LEFT JOIN option_items emi ON emi.id = wol.extra_material_id
            WHERE wol.work_order_id = %s
            ORDER BY wol.line_no, wol.id
        """

        with pymysql.connect(**_connect_kwargs()) as conn:
            with conn.cursor() as cur:
                cur.execute(header_sql, (normalized_work_number,))
                header_row = cur.fetchone()
                if header_row is None:
                    raise LookupError(f"找不到工單號：{normalized_work_number}")
                cur.execute(line_sql, (header_row["id"],))
                line_rows = cur.fetchall()
        return header_row, line_rows

    def _coerce_option_item_name(self, option_group: str, value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, int):
            return self.option_item_names_by_group_and_id.get(option_group, {}).get(value, "")
        if isinstance(value, str):
            return value.strip()
        try:
            return self.option_item_names_by_group_and_id.get(option_group, {}).get(int(value), "")
        except (TypeError, ValueError):
            return str(value).strip()

    def _build_table_rows_from_line_payloads(self, line_rows: list[dict[str, object]]) -> list[list[str]]:
        target_row_count = max(DEFAULT_LINE_ITEM_ROW_COUNT, len(line_rows) + 1)
        built_rows: list[list[str]] = []
        for line_row in line_rows:
            built_rows.append(
                [
                    self._coerce_option_item_name("production_item", line_row.get("production_item_name")),
                    format_decimal_for_ui(line_row.get("width_mm")),
                    "x",
                    format_decimal_for_ui(line_row.get("height_mm")),
                    format_decimal_for_ui(line_row.get("quantity")),
                    self._coerce_option_item_name("material", line_row.get("material_name")),
                    self._coerce_option_item_name("lamination", line_row.get("lamination_name")),
                    self._coerce_option_item_name("board_type", line_row.get("board_type_name")),
                    self._coerce_option_item_name("board_thickness", line_row.get("board_thickness_name")),
                    self._coerce_option_item_name("extra_material", line_row.get("extra_material_name")),
                    format_decimal_for_ui(line_row.get("extra_material_quantity")),
                    format_decimal_for_ui(line_row.get("cbm")),
                    format_decimal_for_ui(line_row.get("cbm_unit_price")),
                    format_decimal_for_ui(line_row.get("line_total")),
                    format_decimal_for_ui(line_row.get("extra_material_total")),
                ]
            )

        while len(built_rows) < target_row_count:
            built_rows.append(list(BLANK_LINE_ROW_TEMPLATE))
        return built_rows

    def load_work_order_by_number(self, work_number: str) -> tuple[int, int]:
        header_row, line_rows = self._fetch_work_order_bundle(work_number)

        customer_combo = getattr(self.ui, "cb_customerName", None)
        if isinstance(customer_combo, QComboBox):
            customer_name = str(header_row.get("client_short_name") or "").strip()
            customer_index = customer_combo.findText(customer_name) if customer_name else -1
            if customer_index >= 0:
                customer_combo.setCurrentIndex(customer_index)
            else:
                customer_combo.setCurrentIndex(-1)
                customer_combo.setEditText(customer_name)

        field_mappings = {
            "le_worknum": header_row.get("work_number"),
            "le_caseName": header_row.get("case_name"),
            "le_phone": header_row.get("company_phone"),
            "le_contactName": header_row.get("contact_name"),
            "le_startTime": header_row.get("work_time"),
            "le_endTime": header_row.get("cleanup_time"),
            "lle_address": header_row.get("work_address"),
            "le_productionAmount": "",
            "le_taxAmount": "",
            "le_totalAmount": "",
        }
        for attr, value in field_mappings.items():
            widget = getattr(self.ui, attr, None)
            if isinstance(widget, QLineEdit):
                widget.setText(str(value or ""))

        if hasattr(self.ui, "te_remark"):
            self.ui.te_remark.setPlainText(str(header_row.get("remark") or ""))

        table_rows = self._build_table_rows_from_line_payloads(line_rows)
        self._populate_line_items_table_with_rows(table_rows)
        self._last_auto_filled_phone = str(header_row.get("company_phone") or "")
        self._last_auto_filled_address = str(header_row.get("work_address") or "")
        return int(header_row["id"]), len(line_rows)

    def _has_loaded_content_on_screen(self) -> bool:
        customer_combo = getattr(self.ui, "cb_customerName", None)
        if isinstance(customer_combo, QComboBox) and customer_combo.currentText().strip():
            return True

        for attr in (
            "le_contactName",
            "le_phone",
            "le_caseName",
            "le_startTime",
            "le_endTime",
            "lle_address",
            "le_productionAmount",
            "le_taxAmount",
            "le_totalAmount",
        ):
            widget = getattr(self.ui, attr, None)
            if isinstance(widget, QLineEdit) and widget.text().strip():
                return True

        if hasattr(self.ui, "te_remark") and self.ui.te_remark.toPlainText().strip():
            return True

        table = getattr(self.ui, "tbl_lineItems", None)
        if table is not None:
            for row in range(table.rowCount()):
                if self._line_row_has_meaningful_data(row):
                    return True
        return False

    def _handle_open_clicked(self) -> None:
        work_number = normalize_line_edit_value(getattr(self.ui, "le_worknum", None)) or ""
        if self._has_loaded_content_on_screen():
            confirm = QMessageBox.question(
                self,
                "開啟工單",
                "目前畫面內容會直接被載入的工單覆蓋；尚未做完整 dirty-check。\n\n要繼續開啟嗎？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirm != QMessageBox.StandardButton.Yes:
                self._set_status_message("已取消開啟工單。")
                return

        try:
            work_order_id, line_count = self.load_work_order_by_number(work_number)
        except Exception as exc:
            message = str(exc) or exc.__class__.__name__
            QMessageBox.warning(self, "開啟失敗", message)
            self._set_status_message(f"開啟失敗：{message}")
            return

        success_message = f"已開啟 work_orders #{work_order_id}（工單 {work_number}，明細 {line_count} 筆）"
        QMessageBox.information(self, "開啟成功", success_message)
        self._set_status_message(success_message)

    def save_work_order_with_lines(self) -> tuple[int, int]:
        if pymysql is None:
            raise RuntimeError("缺少 PyMySQL，無法儲存到 work_order_v2。")

        header_payload = self._header_payload()
        line_payloads = self._collect_line_payloads()
        with pymysql.connect(**_connect_kwargs()) as conn:
            with conn.cursor() as cur:
                work_order_id = self._upsert_work_order_header(cur, header_payload)
                self._replace_work_order_lines(cur, work_order_id, line_payloads)
            conn.commit()
        return work_order_id, len(line_payloads)

    def _handle_save_clicked(self) -> None:
        try:
            work_order_id, line_count = self.save_work_order_with_lines()
        except Exception as exc:
            message = str(exc) or exc.__class__.__name__
            QMessageBox.warning(self, "儲存失敗", message)
            self._set_status_message(f"儲存失敗：{message}")
            return

        work_number = normalize_line_edit_value(getattr(self.ui, "le_worknum", None)) or "-"
        success_message = f"已儲存 work_orders #{work_order_id}（工單 {work_number}，明細 {line_count} 筆）"
        QMessageBox.information(self, "儲存成功", success_message)
        self._set_status_message(success_message)

    def _apply_customer_contact_defaults(self, row: dict[str, str | int | None]) -> None:
        phone_widget = getattr(self.ui, "le_phone", None)
        address_widget = getattr(self.ui, "lle_address", None)
        if not isinstance(phone_widget, QLineEdit) or not isinstance(address_widget, QLineEdit):
            return

        next_phone = str(row.get("phone") or "")
        next_address = str(row.get("address") or "")

        current_phone = phone_widget.text().strip()
        current_address = address_widget.text().strip()
        can_fill_phone = not current_phone or current_phone == self._last_auto_filled_phone
        can_fill_address = not current_address or current_address == self._last_auto_filled_address

        if next_phone and can_fill_phone:
            phone_widget.setText(next_phone)
            self._last_auto_filled_phone = next_phone
        elif not next_phone and current_phone == self._last_auto_filled_phone:
            phone_widget.clear()
            self._last_auto_filled_phone = ""

        if next_address and can_fill_address:
            address_widget.setText(next_address)
            self._last_auto_filled_address = next_address
        elif not next_address and current_address == self._last_auto_filled_address:
            address_widget.clear()
            self._last_auto_filled_address = ""

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
        self._ensure_build_label(remark_group)
        self._position_build_label()

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

    def _ensure_build_label(self, remark_group: QWidget) -> None:
        if self.build_label is not None:
            return

        self.build_label = QLabel(BUILD_LABEL_TEXT, remark_group)
        self.build_label.setObjectName("lbl_buildVersion")
        self.build_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.build_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.build_label.setStyleSheet(
            "color: rgba(32, 33, 36, 0.55); "
            "background-color: rgba(245, 245, 245, 0.88); "
            "border: 1px solid rgba(201, 177, 234, 0.65); "
            "border-radius: 4px; "
            "padding: 1px 6px;"
        )
        self.build_label.adjustSize()
        self.build_label.raise_()

    def _position_build_label(self) -> None:
        if self.build_label is None:
            return

        label_margin_left = 14
        label_margin_bottom = 8
        x = label_margin_left
        y = max(24, self.ui.grp_remark.height() - self.build_label.sizeHint().height() - label_margin_bottom)
        self.build_label.move(x, y)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._position_build_label()

    def _ordered_focus_widgets(self, names: list[str]) -> list[QWidget]:
        widgets: list[QWidget] = []
        for name in names:
            widget = getattr(self.ui, name, None)
            if isinstance(widget, QWidget) and widget.focusPolicy() != Qt.FocusPolicy.NoFocus:
                widgets.append(widget)
        return widgets

    def _tab_target_widget(self, widget: QWidget) -> QWidget:
        if isinstance(widget, QComboBox):
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            line_edit = widget.lineEdit()
            if line_edit is not None:
                line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            # Editable QComboBox 會把焦點代理到內部 lineEdit。
            # Tab chain 必須綁在 combo 本體上，Qt 才會正確停在這個欄位，
            # 並在離開後接到下一個外部 widget，而不是把 customerName 略過。
            return widget
        return widget

    def _redirect_x_focus(self, row: int) -> bool:
        if self.table_tab_navigator is None:
            return False
        return self.table_tab_navigator.redirect_x_cell(row)

    def _sanitize_table_current_cell(self, row: int, column: int) -> None:
        if column != X_COLUMN_INDEX:
            return
        self._redirect_x_focus(row)

    def _sanitize_current_table_focus(self) -> bool:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return False
        if table.currentColumn() != X_COLUMN_INDEX:
            return False
        return self._redirect_x_focus(table.currentRow())

    def _configure_focus_chain(self) -> None:
        top_widgets = self._ordered_focus_widgets(self.TOP_TAB_ORDER)
        bottom_widgets = self._ordered_focus_widgets(self.BOTTOM_TAB_ORDER)
        table = getattr(self.ui, "tbl_lineItems", None)
        ordered_widgets = [self._tab_target_widget(widget) for widget in top_widgets]
        if isinstance(table, QWidget) and table.focusPolicy() != Qt.FocusPolicy.NoFocus:
            ordered_widgets.append(table)
        ordered_widgets.extend(self._tab_target_widget(widget) for widget in bottom_widgets)

        for first, second in zip(ordered_widgets, ordered_widgets[1:]):
            QWidget.setTabOrder(first, second)

        for widget in top_widgets:
            widget.installEventFilter(self)

        if table is not None:
            table.installEventFilter(self)
            table.currentCellChanged.connect(self._sanitize_table_current_cell)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
            if watched is getattr(self.ui, "le_endTime", None) and event.key() in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                forward = event.key() == Qt.Key.Key_Tab and not bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                if forward:
                    self.focus_first_table_cell()
                    return True

            if watched is getattr(self.ui, "tbl_lineItems", None) and event.key() in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                if self._sanitize_current_table_focus():
                    return True
                forward = event.key() == Qt.Key.Key_Tab and not bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                return self._focus_table_boundary_cell(forward=forward)

        return super().eventFilter(watched, event)

    def _first_focusable_table_cell(self) -> tuple[int, int] | None:
        if self.table_tab_navigator is None:
            return None
        return self.table_tab_navigator._find_next_editable_cell(0, -1, forward=True)

    def _last_focusable_table_cell(self) -> tuple[int, int] | None:
        if self.table_tab_navigator is None:
            return None
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return None
        return self.table_tab_navigator._find_next_editable_cell(table.rowCount() - 1, table.columnCount(), forward=False)

    def _focus_table_boundary_cell(self, *, forward: bool) -> bool:
        table = getattr(self.ui, "tbl_lineItems", None)
        navigator = self.table_tab_navigator
        if table is None or navigator is None:
            return False

        current_row = table.currentRow()
        current_column = table.currentColumn()
        has_current_cell = current_row >= 0 and current_column >= 0

        if has_current_cell and current_column == X_COLUMN_INDEX:
            return navigator.redirect_x_cell(current_row)

        if has_current_cell and navigator._is_focusable_cell(current_row, current_column):
            target_cell = navigator._find_next_editable_cell(current_row, current_column, forward=forward)
            if target_cell is not None:
                row, column = target_cell
                table.setCurrentCell(row, column)
                QTimer.singleShot(0, lambda: navigator._focus_cell(row, column))
                return True

            self.focus_after_table(forward=forward)
            return True

        boundary_cell = self._first_focusable_table_cell() if forward else self._last_focusable_table_cell()
        if boundary_cell is None:
            self.focus_after_table(forward=forward)
            return True

        row, column = boundary_cell
        table.setFocus(Qt.FocusReason.TabFocusReason if forward else Qt.FocusReason.BacktabFocusReason)
        table.setCurrentCell(row, column)
        QTimer.singleShot(0, lambda: navigator._focus_cell(row, column))
        return True

    def focus_first_table_cell(self) -> None:
        table = getattr(self.ui, "tbl_lineItems", None)
        first_cell = self._first_focusable_table_cell()
        if table is None or first_cell is None or self.table_tab_navigator is None:
            return

        row, column = first_cell
        table.setFocus(Qt.FocusReason.TabFocusReason)
        table.setCurrentCell(row, column)
        QTimer.singleShot(0, lambda: self.table_tab_navigator._focus_cell(row, column))

    def focus_last_top_field(self) -> None:
        top_widgets = self._ordered_focus_widgets(self.TOP_TAB_ORDER)
        if top_widgets:
            top_widgets[-1].setFocus(Qt.FocusReason.BacktabFocusReason)

    def focus_after_table(self, *, forward: bool) -> None:
        if not forward:
            self.focus_last_top_field()
            return

        bottom_widgets = self._ordered_focus_widgets(self.BOTTOM_TAB_ORDER)
        if bottom_widgets:
            bottom_widgets[0].setFocus(Qt.FocusReason.TabFocusReason)

    def _tune_line_items_table(self) -> None:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return

        table.clear()
        table.setColumnCount(len(TABLE_HEADERS))
        self.table_tab_navigator = TableCellTabNavigator(table, self)
        table.setItemDelegate(TableItemDelegate(self.table_tab_navigator, table))
        table.setHorizontalHeader(BandHeaderView(Qt.Orientation.Horizontal, table))
        table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self._apply_line_items_header_colors(table)
        table.setRowCount(DEFAULT_LINE_ITEM_ROW_COUNT)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.setShowGrid(True)
        table.setCornerButtonEnabled(False)
        table.setSelectionBehavior(table.SelectionBehavior.SelectItems)
        table.setSelectionMode(table.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
            item.setFlags(Qt.ItemFlag.NoItemFlags)
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

    def _make_line_edit(self, column: int, text: str) -> QLineEdit:
        line_edit = QLineEdit(text)
        line_edit.setFrame(False)
        line_edit.setMinimumHeight(28)
        line_edit.setMaximumHeight(28)
        line_edit.setTextMargins(6, 0, 6, 0)
        if column in NUMERIC_COLUMN_INDEXES:
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            line_edit.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        return line_edit

    def _make_widget_backing_item(self, column: int) -> QTableWidgetItem:
        item = self._make_table_item("", column)
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        return item

    def _register_table_cell_widget(self, widget: QWidget, row: int, column: int) -> QWidget:
        if self.table_tab_navigator is not None:
            self.table_tab_navigator.register_widget(widget, row, column)
        return widget

    def _populate_single_line_item_row(self, row_idx: int, row: list[str] | None = None) -> None:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return

        row_values = list(row) if row is not None else list(BLANK_LINE_ROW_TEMPLATE)
        if len(row_values) < len(TABLE_HEADERS):
            row_values.extend([""] * (len(TABLE_HEADERS) - len(row_values)))
        if len(row_values) > len(TABLE_HEADERS):
            row_values = row_values[: len(TABLE_HEADERS)]
        row_values[X_COLUMN_INDEX] = "x"

        for col_idx, value in enumerate(row_values):
            if col_idx in COMBO_COLUMN_OPTIONS:
                widget = self._make_combo_box(col_idx, value)
                self._connect_auto_append_signal(widget)
                table.setCellWidget(row_idx, col_idx, self._register_table_cell_widget(widget, row_idx, col_idx))
                table.setItem(row_idx, col_idx, self._make_widget_backing_item(col_idx))
            elif col_idx in TABLE_SKIP_FOCUS_COLUMN_INDEXES:
                table.setItem(row_idx, col_idx, self._make_table_item(value, col_idx))
            else:
                widget = self._make_line_edit(col_idx, value)
                self._connect_auto_append_signal(widget)
                table.setCellWidget(row_idx, col_idx, self._register_table_cell_widget(widget, row_idx, col_idx))
                table.setItem(row_idx, col_idx, self._make_widget_backing_item(col_idx))
        table.setRowHeight(row_idx, 36)

    def _connect_auto_append_signal(self, widget: QWidget) -> None:
        if isinstance(widget, QComboBox):
            widget.currentTextChanged.connect(self._handle_line_item_widget_changed)
            line_edit = widget.lineEdit()
            if line_edit is not None:
                line_edit.textChanged.connect(self._handle_line_item_widget_changed)
        elif isinstance(widget, QLineEdit):
            widget.textChanged.connect(self._handle_line_item_widget_changed)

    def _append_blank_line_item_row(self) -> int:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None:
            return -1

        row_idx = table.rowCount()
        table.insertRow(row_idx)
        self._populate_single_line_item_row(row_idx, list(BLANK_LINE_ROW_TEMPLATE))
        return row_idx

    def _ensure_trailing_blank_line(self) -> bool:
        table = getattr(self.ui, "tbl_lineItems", None)
        if table is None or table.rowCount() <= 0:
            return False

        last_row = table.rowCount() - 1
        if self._line_row_has_meaningful_data(last_row):
            self._append_blank_line_item_row()
            return True
        return False

    def _handle_line_item_widget_changed(self, _value: str) -> None:
        if self._suspend_auto_append_checks:
            return
        self._ensure_trailing_blank_line()

    def _initialize_blank_work_order(self) -> None:
        self.setWindowTitle("project.ui preview (generated)")

        self._last_auto_filled_phone = ""
        self._last_auto_filled_address = ""

        customer_combo = getattr(self.ui, "cb_customerName", None)
        if isinstance(customer_combo, QComboBox):
            customer_combo.setCurrentIndex(-1)
            customer_combo.clearEditText()

        for attr in (
            "le_worknum",
            "le_contactName",
            "le_phone",
            "le_caseName",
            "le_startTime",
            "le_endTime",
            "lle_address",
            "le_productionAmount",
            "le_taxAmount",
            "le_totalAmount",
        ):
            widget = getattr(self.ui, attr, None)
            if widget is not None:
                widget.clear()

        if hasattr(self.ui, "te_remark"):
            self.ui.te_remark.clear()

        table = getattr(self.ui, "tbl_lineItems", None)
        row_count = table.rowCount() if table is not None else 0
        self._populate_line_items_table_with_rows([list(BLANK_LINE_ROW_TEMPLATE) for _ in range(row_count)])

    def _populate_line_items_table_with_rows(self, rows: list[list[str]]) -> None:
        if not hasattr(self.ui, "tbl_lineItems"):
            return

        table = self.ui.tbl_lineItems
        desired_rows = max(DEFAULT_LINE_ITEM_ROW_COUNT, len(rows))
        if desired_rows <= 0:
            desired_rows = DEFAULT_LINE_ITEM_ROW_COUNT
        table.setRowCount(desired_rows)
        table.clearContents()
        self.table_tab_navigator = TableCellTabNavigator(table, self)
        self._suspend_auto_append_checks = True
        try:
            for row_idx in range(table.rowCount()):
                row = rows[row_idx] if row_idx < len(rows) else list(BLANK_LINE_ROW_TEMPLATE)
                self._populate_single_line_item_row(row_idx, row)
        finally:
            self._suspend_auto_append_checks = False
        self._ensure_trailing_blank_line()

    def _seed_demo_values(self) -> None:
        self._initialize_blank_work_order()

        customer_combo = getattr(self.ui, "cb_customerName", None)
        if isinstance(customer_combo, QComboBox):
            if self.clients:
                customer_combo.setCurrentIndex(0)
            else:
                customers = ["采月廣告有限公司", "萬榮國際", "KING", "就肆電競"]
                customer_combo.addItems(customers)
                customer_combo.setCurrentIndex(0)

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
            if widget is None:
                continue
            if attr in {"le_phone", "lle_address"} and widget.text().strip():
                continue
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
        self._populate_line_items_table_with_rows(sample_rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshot", type=Path, help="Save a screenshot to this path and exit.")
    parser.add_argument("--save-demo", action="store_true", help="Save the seeded header + line fields into work_orders/work_order_lines and print the inserted id.")
    parser.add_argument("--load-work-number", help="Load this work number after window init, print the loaded id/count, and exit.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    app = QApplication(sys.argv)
    apply_light_preview_theme(app)
    window = GeneratedUiPreviewWindow()
    window.show()

    if args.save_demo:
        def save_demo_and_quit() -> None:
            window._seed_demo_values()
            try:
                work_order_id, line_count = window.save_work_order_with_lines()
            except Exception as exc:
                print(f"SAVE_DEMO_ERROR: {exc}", file=sys.stderr)
                app.exit(1)
                return

            print(f"SAVE_DEMO_OK:{work_order_id}:{line_count}")
            app.exit(0)

        QTimer.singleShot(0, save_demo_and_quit)
    elif args.load_work_number:
        def load_and_quit() -> None:
            try:
                work_order_id, line_count = window.load_work_order_by_number(args.load_work_number)
            except Exception as exc:
                print(f"LOAD_WORK_ORDER_ERROR: {exc}", file=sys.stderr)
                app.exit(1)
                return

            header_values = {
                "work_number": normalize_line_edit_value(getattr(window.ui, "le_worknum", None)) or "",
                "case_name": normalize_line_edit_value(getattr(window.ui, "le_caseName", None)) or "",
                "customer_name": getattr(window.ui, "cb_customerName", None).currentText().strip() if getattr(window.ui, "cb_customerName", None) is not None else "",
                "phone": normalize_line_edit_value(getattr(window.ui, "le_phone", None)) or "",
                "contact_name": normalize_line_edit_value(getattr(window.ui, "le_contactName", None)) or "",
                "start_time": normalize_line_edit_value(getattr(window.ui, "le_startTime", None)) or "",
                "end_time": normalize_line_edit_value(getattr(window.ui, "le_endTime", None)) or "",
                "address": normalize_line_edit_value(getattr(window.ui, "lle_address", None)) or "",
                "remark": normalize_text_edit_value(getattr(window.ui, "te_remark", None)) or "",
            }
            table = getattr(window.ui, "tbl_lineItems", None)
            first_rows = []
            if table is not None:
                for row in range(min(3, table.rowCount())):
                    first_rows.append([window._table_cell_text(row, column) for column in range(table.columnCount())])
            print(f"LOAD_WORK_ORDER_OK:{work_order_id}:{line_count}:{header_values}:{first_rows}")
            app.exit(0)

        QTimer.singleShot(0, load_and_quit)
    elif args.screenshot:
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
