from __future__ import annotations

import sys
import types
from pathlib import Path


class _Dummy:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return _Dummy()

    def __getattr__(self, name):
        return _Dummy()

    def __or__(self, other):
        return self

    def __ror__(self, other):
        return self

    def __bool__(self):
        return False


class _StandardButton:
    Yes = _Dummy()
    No = _Dummy()
    Cancel = _Dummy()


class _QMessageBox(_Dummy):
    StandardButton = _StandardButton


class _DummyModule(types.ModuleType):
    def __getattr__(self, name):
        value = type(name, (_Dummy,), {})
        setattr(self, name, value)
        return value


def _install_qt_stubs() -> None:
    sys.modules.setdefault("PySide6", _DummyModule("PySide6"))
    sys.modules.setdefault("PySide6.QtCore", _DummyModule("PySide6.QtCore"))
    sys.modules.setdefault("PySide6.QtGui", _DummyModule("PySide6.QtGui"))
    qt_widgets = _DummyModule("PySide6.QtWidgets")
    qt_widgets.QMessageBox = _QMessageBox
    sys.modules.setdefault("PySide6.QtWidgets", qt_widgets)
    ui_module = types.ModuleType("ui_project_generated")
    ui_module.Ui_MainWindow = type("Ui_MainWindow", (_Dummy,), {})
    sys.modules.setdefault("ui_project_generated", ui_module)


def test_inline_wh_material_without_board_keeps_30mm_in_production_item():
    _install_qt_stubs()
    import preview_generated_ui as app

    parser = object.__new__(app.GeneratedUiPreviewWindow)
    parser.combo_column_options = {
        5: ["PVC", "PP"],
        6: ["亮面", "霧面"],
        7: ["合成板", "黑色合成板", "發泡板", "瓦楞板"],
        8: ["2mm", "5mm", "10mm", "30mm"],
        9: [],
    }

    line = parser._parse_import_file(Path("30MM AC檯面PVC_w99_h50cm.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["production_item"] == "30MM AC檯面"
    assert finalized["size_text"] == "99X50cm"
    assert finalized["material"] == "PVC"
    assert finalized["board_type"] == ""
    assert finalized["board_thickness"] == ""
    assert finalized["needs_review"] is False


def test_thickness_token_only_applies_when_board_token_exists():
    _install_qt_stubs()
    import preview_generated_ui as app

    parser = object.__new__(app.GeneratedUiPreviewWindow)
    parser.combo_column_options = {9: []}

    without_board = parser._resolve_import_spec_tokens(["30MM"], {"customer_name": ""})
    assert without_board["board_type"] == ""
    assert without_board["board_thickness"] == ""
    assert without_board["unresolved_tokens"] == ["30MM"]

    with_board = parser._resolve_import_spec_tokens(["H", "5MM"], {"customer_name": ""})
    assert with_board["board_type"] == "合成板"
    assert with_board["board_thickness"] == "5MM"
    assert with_board["unresolved_tokens"] == []
