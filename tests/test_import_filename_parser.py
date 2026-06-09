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


def test_import_only_accepts_jpg_suffixes():
    _install_qt_stubs()
    import preview_generated_ui as app

    assert app.IMPORT_IMAGE_SUFFIXES == {".jpg"}


def test_paper_stand_quantity_sets_line_quantity_and_keeps_accessory():
    _install_qt_stubs()
    import preview_generated_ui as app

    parser = object.__new__(app.GeneratedUiPreviewWindow)
    parser.combo_column_options = {
        5: ["PVC", "PP"],
        6: ["亮面", "霧面"],
        7: ["合成板", "黑色合成板", "發泡板", "瓦楞板"],
        8: ["2mm", "5mm", "10mm", "30mm"],
        9: ["紙腳架"],
    }

    line = parser._parse_import_file(Path("問券牌-21X30-PVC+H+紙腳架X3.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["production_item"] == "問券牌"
    assert finalized["size_text"] == "21X30"
    assert finalized["material"] == "PVC"
    assert finalized["board_type"] == "合成板"
    assert finalized["extra_materials"] == ["紙腳架"]
    assert finalized["extra_material_quantities"] == {"紙腳架": 3}
    assert finalized["quantity"] == 3
    table_row = parser._build_table_row_from_import_line(finalized)
    assert table_row[4] == "3"
    assert table_row[10] == "3"
    assert finalized["needs_review"] is False


def test_multi_dash_production_item_uses_rightmost_size_segment():
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

    line = parser._parse_import_file(Path("入口上方logo-輸出表板-180x40-PVC+H.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["production_item"] == "入口上方logo-輸出表板"
    assert finalized["size_text"] == "180x40"
    assert finalized["material"] == "PVC"
    assert finalized["board_type"] == "合成板"
    assert finalized["needs_review"] is False


def test_short_extra_material_aliases_map_to_database_names():
    _install_qt_stubs()
    import preview_generated_ui as app

    parser = object.__new__(app.GeneratedUiPreviewWindow)
    parser.combo_column_options = {
        5: ["PVC", "PP"],
        6: ["亮面", "霧面"],
        7: ["合成板", "黑色合成板", "發泡板", "瓦楞板"],
        8: ["2mm", "5mm", "10mm", "30mm"],
        9: ["150直鐵腳架", "機台切型"],
    }

    line = parser._parse_import_file(Path("入場須知-63X151-PVC+H+150直+機切.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["extra_materials"] == ["150直鐵腳架", "機台切型"]
    assert finalized["needs_review"] is False


def test_processing_hint_with_quantity_affects_quantities_but_is_not_recorded():
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

    line = parser._parse_import_file(Path("中島上紅圈-4X216-PVC+黑色H+前留1.5CMX4.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["quantity"] == 4
    assert finalized["extra_materials"] == []
    assert finalized["unresolved_tokens"] == []
    assert finalized["needs_review"] is False


def test_banner_item_can_leave_material_blank_for_user():
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

    line = parser._parse_import_file(Path("A-42X110-掛旗+上下鋁桿43.jpg"), {"customer_name": ""})
    finalized = parser._finalize_import_line_resolution(line, {"customer_name": ""})

    assert finalized["production_item"] == "掛旗"
    assert finalized["size_text"] == "42X110"
    assert finalized["material"] == ""
    assert finalized["unresolved_tokens"] == []
    assert finalized["needs_review"] is False


def test_banner_lines_with_same_spec_are_summarized():
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

    lines = [
        parser._finalize_import_line_resolution(parser._parse_import_file(Path("A-42X110-掛旗+上下鋁桿43.jpg"), {"customer_name": ""}), {"customer_name": ""}),
        parser._finalize_import_line_resolution(parser._parse_import_file(Path("B-42X110-掛旗+上下鋁桿43.jpg"), {"customer_name": ""}), {"customer_name": ""}),
        parser._finalize_import_line_resolution(parser._parse_import_file(Path("logo掛旗x2_w38xh95cm-上方鋁桿40下方切型.jpg"), {"customer_name": ""}), {"customer_name": ""}),
    ]
    grouped = parser._summarize_import_lines(lines)

    assert [(line["production_item"], line["size_text"], line["quantity"]) for line in grouped] == [
        ("掛旗", "42X110", 2),
        ("logo掛旗", "38X95cm", 2),
    ]


def test_numbered_layout_suffix_on_board_token_is_ignored_and_grouped():
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

    lines = [
        parser._finalize_import_line_resolution(parser._parse_import_file(Path("60th_入口兩側主視覺-252x252-pvc+h-1.jpg"), {"customer_name": ""}), {"customer_name": ""}),
        parser._finalize_import_line_resolution(parser._parse_import_file(Path("60th_入口兩側主視覺-252x252-pvc+h-2.jpg"), {"customer_name": ""}), {"customer_name": ""}),
    ]
    grouped = parser._summarize_import_lines(lines)

    assert len(grouped) == 1
    assert grouped[0]["production_item"] == "60th_入口兩側主視覺"
    assert grouped[0]["size_text"] == "252x252"
    assert grouped[0]["material"] == "PVC"
    assert grouped[0]["board_type"] == "合成板"
    assert grouped[0]["quantity"] == 2
    assert grouped[0]["needs_review"] is False


def test_import_completion_message_lists_review_rows_and_reasons():
    _install_qt_stubs()
    import preview_generated_ui as app

    parser = object.__new__(app.GeneratedUiPreviewWindow)
    message = parser._format_import_completion_message([
        {"source_file": "ok.jpg", "needs_review": False},
        {
            "source_file": "超人力霸王迪迦_w47x52cm.jpg",
            "needs_review": True,
            "review_reason": ["材質未判定"],
        },
    ])

    assert "已導入 2 筆明細；其中 1 筆需要你再看一下" in message
    assert "第 2 行：超人力霸王迪迦_w47x52cm.jpg — 材質未判定" in message
