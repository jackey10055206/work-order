from __future__ import annotations

import sys
from dataclasses import dataclass

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateTimeEdit,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


@dataclass(frozen=True)
class DemoData:
    case_name: str = "南港展場春季活動主視覺"
    customer_name: str = "采月廣告有限公司"
    phone: str = "02-8647-8840"
    work_order_no: str = "26-03-28-01"
    contact_name: str = "王小姐"
    address: str = "台北市南港區經貿二路 186 號 4 樓"
    package_note: str = "珍珠棉保護 + 紙箱分件"
    transport_note: str = "3/31 上午送達，需先電話聯繫現場窗口"


class WorkOrderPrototypeWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.demo_data = DemoData()
        self.setWindowTitle("Work Order Prototype - PySide6")
        self.resize(1280, 720)
        self._build_ui()
        self._apply_styles()
        self._apply_demo_data()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        page_layout = QVBoxLayout(root)
        page_layout.setContentsMargins(20, 20, 20, 20)
        page_layout.setSpacing(16)

        page_layout.addWidget(self._create_header())
        page_layout.addWidget(self._create_basic_info_section())
        page_layout.addWidget(self._create_footer_hint())
        page_layout.addStretch(1)

    def _create_header(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("headerCard")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(18, 16, 18, 16)

        title_col = QVBoxLayout()
        title = QLabel("工單基本資料 Prototype")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)

        subtitle = QLabel("以 layout 重做原工單上方基本資料區，保留原本分組與輸入節奏。")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #5b6472;")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(QPushButton("預覽列印"))
        actions.addWidget(QPushButton("儲存草稿"))

        layout.addLayout(title_col, 1)
        layout.addLayout(actions)
        return frame

    def _create_basic_info_section(self) -> QGroupBox:
        group = QGroupBox("基本資料區")
        outer = QVBoxLayout(group)
        outer.setContentsMargins(16, 18, 16, 16)
        outer.setSpacing(14)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 4)

        grid.addWidget(self._create_order_overview_card(), 0, 0)
        grid.addWidget(self._create_contact_card(), 0, 1)
        grid.addWidget(self._create_time_card(), 0, 2)
        grid.addWidget(self._create_address_card(), 1, 0, 1, 2)
        grid.addWidget(self._create_logistics_card(), 1, 2)

        outer.addLayout(grid)
        return group

    def _create_order_overview_card(self) -> QFrame:
        frame, body = self._create_card("案件資訊")
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)

        self.case_name_edit = QLineEdit()
        self.case_name_edit.setPlaceholderText("請輸入案名")

        self.customer_combo = QComboBox()
        self.customer_combo.setEditable(True)
        self.customer_combo.addItems(["采月廣告有限公司", "萬榮國際", "KING", "就肆電競"])

        self.work_order_edit = QLineEdit()
        self.work_order_edit.setPlaceholderText("例如 26-03-28-01")

        layout.addRow("案名", self.case_name_edit)
        layout.addRow("客戶名稱", self.customer_combo)
        layout.addRow("工單編號", self.work_order_edit)
        body.addLayout(layout)
        return frame

    def _create_contact_card(self) -> QFrame:
        frame, body = self._create_card("聯絡資訊")
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("請輸入電話")

        self.contact_edit = QLineEdit()
        self.contact_edit.setPlaceholderText("請輸入聯絡人")

        layout.addRow("電話", self.phone_edit)
        layout.addRow("聯絡人", self.contact_edit)
        body.addLayout(layout)
        return frame

    def _create_time_card(self) -> QFrame:
        frame, body = self._create_card("進撤場時間")
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)

        self.work_time_edit = QDateTimeEdit()
        self.work_time_edit.setDisplayFormat("yyyy/MM/dd HH:mm")
        self.work_time_edit.setCalendarPopup(True)
        self.work_time_edit.setDateTime(QDateTime.fromString("2026/03/31 09:00", "yyyy/MM/dd HH:mm"))

        self.cleanup_time_edit = QDateTimeEdit()
        self.cleanup_time_edit.setDisplayFormat("yyyy/MM/dd HH:mm")
        self.cleanup_time_edit.setCalendarPopup(True)
        self.cleanup_time_edit.setDateTime(QDateTime.fromString("2026/03/31 18:00", "yyyy/MM/dd HH:mm"))

        layout.addRow("工作時間", self.work_time_edit)
        layout.addRow("清場時間", self.cleanup_time_edit)
        body.addLayout(layout)
        return frame

    def _create_address_card(self) -> QFrame:
        frame, body = self._create_card("工作地點")

        title_row = QHBoxLayout()
        title_label = QLabel("工作地址")
        hint_label = QLabel("保留原系統偏長地址輸入的使用感")
        hint_label.setStyleSheet("color: #5b6472;")
        title_row.addWidget(title_label)
        title_row.addStretch(1)
        title_row.addWidget(hint_label)

        self.address_edit = QTextEdit()
        self.address_edit.setPlaceholderText("請輸入施工 / 工作地址")
        self.address_edit.setMinimumHeight(110)
        self.address_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        body.addLayout(title_row)
        body.addWidget(self.address_edit)
        return frame

    def _create_logistics_card(self) -> QFrame:
        frame, body = self._create_card("包裝與運送")
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(12)

        self.package_combo = QComboBox()
        self.package_combo.addItems(["未指定", "紙箱", "珍珠棉", "木箱", "航空包裝"])

        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["未指定", "自取", "公司派送", "貨運寄送", "現場安裝"])

        form.addRow("包裝", self.package_combo)
        form.addRow("運送", self.transport_combo)

        self.package_note_edit = QLineEdit()
        self.package_note_edit.setPlaceholderText("包裝備註")
        self.transport_note_edit = QLineEdit()
        self.transport_note_edit.setPlaceholderText("運送備註")

        body.addLayout(form)
        body.addWidget(self.package_note_edit)
        body.addWidget(self.transport_note_edit)
        return frame

    def _create_footer_hint(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("footerHint")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)

        label = QLabel("Prototype 範圍只重做工單上方基本資料區；未串接資料庫，也不改動既有 PyQt5 視窗。")
        label.setWordWrap(True)
        layout.addWidget(label)
        return frame

    def _create_card(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame()
        frame.setProperty("card", True)

        wrapper = QVBoxLayout(frame)
        wrapper.setContentsMargins(16, 14, 16, 16)
        wrapper.setSpacing(12)

        title_bar = QLabel(title)
        title_bar.setObjectName("cardTitle")
        wrapper.addWidget(title_bar)

        body = QVBoxLayout()
        body.setSpacing(12)
        wrapper.addLayout(body)
        return frame, body

    def _apply_demo_data(self) -> None:
        self.case_name_edit.setText(self.demo_data.case_name)
        self.customer_combo.setCurrentText(self.demo_data.customer_name)
        self.phone_edit.setText(self.demo_data.phone)
        self.work_order_edit.setText(self.demo_data.work_order_no)
        self.contact_edit.setText(self.demo_data.contact_name)
        self.address_edit.setPlainText(self.demo_data.address)
        self.package_combo.setCurrentText("珍珠棉")
        self.transport_combo.setCurrentText("公司派送")
        self.package_note_edit.setText(self.demo_data.package_note)
        self.transport_note_edit.setText(self.demo_data.transport_note)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: #f3f5f8;
            }
            QGroupBox {
                border: 1px solid #d7deea;
                border-radius: 12px;
                margin-top: 10px;
                font-size: 15px;
                font-weight: 700;
                background: #ffffff;
            }
            QGroupBox::title {
                left: 14px;
                padding: 0 6px;
            }
            QFrame#headerCard, QFrame#footerHint, QFrame[card="true"] {
                background: #ffffff;
                border: 1px solid #d7deea;
                border-radius: 12px;
            }
            QLabel#cardTitle {
                font-size: 14px;
                font-weight: 700;
                color: #1f2937;
            }
            QLabel {
                color: #1f2937;
            }
            QLineEdit, QComboBox, QDateTimeEdit, QTextEdit {
                border: 1px solid #c6d0df;
                border-radius: 8px;
                padding: 8px 10px;
                background: #fbfcfe;
                min-height: 22px;
            }
            QPushButton {
                border: 1px solid #c8d3e1;
                border-radius: 8px;
                padding: 8px 14px;
                background: #ffffff;
            }
            QPushButton:hover {
                background: #f4f7fb;
            }
            """
        )


def main() -> int:
    app = QApplication(sys.argv)
    window = WorkOrderPrototypeWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
