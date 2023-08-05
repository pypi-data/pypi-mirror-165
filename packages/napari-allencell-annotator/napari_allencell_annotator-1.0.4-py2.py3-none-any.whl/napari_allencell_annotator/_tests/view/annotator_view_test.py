from unittest import mock
from unittest.mock import MagicMock, create_autospec, ANY

from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
    QListWidget,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QVBoxLayout,
    QListWidgetItem,
    QWidget,
    QHBoxLayout,
    QLabel,
    QMessageBox,
)


class TestAnnotatorView:
    def setup_method(self):
        with mock.patch.object(AnnotatorView, "__init__", lambda x: None):
            self._view = AnnotatorView()
            self._view._mode = AnnotatorViewMode.ADD

    def test_mode(self):
        assert self._view.mode == AnnotatorViewMode.ADD

    def test_set_mode(self):
        expected = AnnotatorViewMode.VIEW
        self._view._display_mode = MagicMock()
        self._view.set_mode(expected)
        assert self._view._mode == self._view.mode == expected
        self._view._display_mode.assert_called_once_with()

    def test_set_num_images(self):
        self._view.set_num_images(4)
        assert self._view.num_images == 4

    def test_set_curr_index(self):
        self._view.num_images = 4
        self._view.progress_bar = MagicMock()
        self._view.progress_bar.setText = MagicMock()
        self._view.set_curr_index(2)
        self._view.progress_bar.setText.assert_called_once_with("3 of 4 Images")
        assert self._view.curr_index == 2

    def test_reset_annotations(self):
        with mock.patch.object(QListWidget, "__init__", lambda x: None):

            self._view.annot_list = QListWidget()

            self._view.annot_list.setMaximumHeight = MagicMock()
            self._view.annot_list.clear = MagicMock()
            self._view.annotation_item_widgets = ["item"]
            self._view.annots_order = ["item"]
            self._view.default_vals = ["item"]
            self._view._reset_annotations()

            self._view.annot_list.clear.assert_called_once_with()
            assert self._view.annotation_item_widgets == []
            assert self._view.annots_order == []
            assert self._view.default_vals == []

    def test_render_default_values(self):
        self._view.default_vals = []
        self._view.render_values = MagicMock()
        self._view.render_default_values()
        self._view.render_values.assert_called_once_with([])

    def test_render_values_line_input(self):
        q_line_edit = create_autospec(QLineEdit)
        self._view.annotation_item_widgets = [q_line_edit]
        self._view.default_vals = ["default"]
        self._view.render_values(["hello"])
        q_line_edit.setText.assert_called_once_with("hello")

    def test_render_values_line_no_input(self):
        q_line_edit = create_autospec(QLineEdit)
        self._view.annotation_item_widgets = [q_line_edit]
        self._view.default_vals = ["default"]
        self._view.render_values([""])
        q_line_edit.setText.assert_called_once_with("default")

    def test_render_values_line_none_input(self):
        q_line_edit = create_autospec(QLineEdit)
        self._view.annotation_item_widgets = [q_line_edit]
        self._view.default_vals = ["default"]
        self._view.render_values([None])
        q_line_edit.setText.assert_called_once_with("default")

    def test_render_values_spin(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        self._view.annotation_item_widgets = [q_spin]
        self._view.default_vals = [8]
        self._view.render_values(["0"])
        q_spin.setValue.assert_called_once_with(0)

    def test_render_values_spin_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        self._view.annotation_item_widgets = [q_spin]
        self._view.default_vals = ["8"]
        self._view.render_values([""])
        q_spin.setValue.assert_called_once_with(8)

    def test_render_values_check(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        self._view.annotation_item_widgets = [q_check]
        self._view.default_vals = [True]
        self._view.render_values(["False"])
        q_check.setChecked.assert_called_once_with(False)

    def test_render_values_check_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        self._view.annotation_item_widgets = [q_check]
        self._view.default_vals = [True]
        self._view.render_values([""])
        q_check.setChecked.assert_called_once_with(True)

    def test_render_values_combo(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_combo]
        self._view.default_vals = ["option1"]
        self._view.render_values(["option2"])
        q_combo.setCurrentText.assert_called_once_with("option2")

    def test_render_values_combo_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_combo]
        self._view.default_vals = ["option1"]
        self._view.render_values([""])
        q_combo.setCurrentText.assert_called_once_with("option1")

    def test_render_values_mult_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        self._view.default_vals = ["default", "0", True, "option1"]
        self._view.render_values(["", "", "", ""])
        q_line_edit.setText.assert_called_once_with("default")
        q_spin.setValue.assert_called_once_with(0)
        q_check.setChecked.assert_called_once_with(True)
        q_combo.setCurrentText.assert_called_once_with("option1")

    def test_render_values_mult_some_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        self._view.default_vals = ["default", "0", True, "option1"]
        self._view.render_values(["", "5", "", "option2"])
        q_line_edit.setText.assert_called_once_with("default")
        q_spin.setValue.assert_called_once_with(5)
        q_check.setChecked.assert_called_once_with(True)
        q_combo.setCurrentText.assert_called_once_with("option2")

    def test_render_values_mult_some_none_some_empty(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        self._view.default_vals = ["default", "0", True, "option1"]
        self._view.render_values([None, "", "False", ""])
        q_line_edit.setText.assert_called_once_with("default")
        q_spin.setValue.assert_called_once_with(0)
        q_check.setChecked.assert_called_once_with(False)
        q_combo.setCurrentText.assert_called_once_with("option1")

    def test_get_curr_annots(self):
        q_line_edit = create_autospec(QLineEdit)
        q_line_edit.text = MagicMock(return_value="text")
        q_spin = create_autospec(QSpinBox)
        q_spin.value = MagicMock(return_value=5)
        q_check = create_autospec(QCheckBox)
        q_check.isChecked = MagicMock(return_value=True)
        q_combo = create_autospec(QComboBox)
        q_combo.currentText = MagicMock(return_value="text2")
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        assert self._view.get_curr_annots() == ["text", 5, True, "text2"]

    def test_toggle_annots_editable_true(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        self._view.toggle_annots_editable(True)
        q_line_edit.setEnabled.assert_called_once_with(True)
        q_spin.setEnabled.assert_called_once_with(True)
        q_check.setEnabled.assert_called_once_with(True)
        q_combo.setEnabled.assert_called_once_with(True)

    def test_toggle_annots_editable_false(self):
        q_line_edit = create_autospec(QLineEdit)
        q_spin = create_autospec(QSpinBox)
        q_check = create_autospec(QCheckBox)
        q_combo = create_autospec(QComboBox)
        self._view.annotation_item_widgets = [q_line_edit, q_spin, q_check, q_combo]
        self._view.toggle_annots_editable(False)
        q_line_edit.setEnabled.assert_called_once_with(False)
        q_spin.setEnabled.assert_called_once_with(False)
        q_check.setEnabled.assert_called_once_with(False)
        q_combo.setEnabled.assert_called_once_with(False)

    def test_display_mode_add_mode(self):
        self._view._mode = AnnotatorViewMode.ADD
        self._view.add_widget = MagicMock()
        self._view._reset_annotations = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(QListWidgetItem)
        widget = create_autospec(QLineEdit)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.add_widget.show.assert_called_once_with()
        self._view._reset_annotations.assert_called_once_with()
        self._view.layout.addWidget.assert_called_once_with(self._view.add_widget)

    def test_display_mode_view_mode(self):
        self._view._mode = AnnotatorViewMode.VIEW
        self._view.save_json_btn = MagicMock()
        self._view.view_widget = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(QListWidgetItem)
        widget = create_autospec(QLineEdit)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.view_widget.show.assert_called_once_with()
        self._view.save_json_btn.setEnabled.assert_called_once_with(True)
        self._view.layout.addWidget.assert_called_once_with(self._view.view_widget)

    def test_display_mode_annotate_mode(self):
        self._view._mode = AnnotatorViewMode.ANNOTATE
        self._view.prev_btn = MagicMock()
        self._view.annot_widget = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(QListWidgetItem)
        widget = create_autospec(QLineEdit)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.annot_widget.show.assert_called_once_with()
        self._view.prev_btn.setEnabled.assert_called_once_with(False)
        self._view.layout.addWidget.assert_called_once_with(self._view.annot_widget)

    def test_render_annotations(self):
        dct = {"name": [], "name2": [], "name3": []}
        self._view._create_annot = MagicMock()

        self._view.annot_list = create_autospec(QListWidget)
        self._view.annot_list.item(0).sizeHint().height = MagicMock(return_value=10)
        self._view.render_annotations(dct)
        self._view._create_annot.assert_has_calls(
            [mock.call("name", []), mock.call("name2", []), mock.call("name3", [])]
        )
        self._view.annot_list.setMaximumHeight.assert_called_once_with(30)

    def test_render_annotations_one_item(self):
        dct = {"name": []}
        self._view._create_annot = MagicMock()

        self._view.annot_list = create_autospec(QListWidget)
        self._view.annot_list.item(0).sizeHint().height = MagicMock(return_value=10)
        self._view.render_annotations(dct)
        self._view._create_annot.assert_has_calls([mock.call("name", [])])
        self._view.annot_list.setMaximumHeight.assert_called_once_with(10)

    def test_create_annot_string(self):
        with mock.patch.object(QWidget, "__init__", lambda x: None):
            with mock.patch.object(QHBoxLayout, "__init__", lambda x: None):
                with mock.patch.object(QLabel, "__init__", lambda x, y: None):
                    with mock.patch.object(QLineEdit, "__init__", lambda x, y: None):
                        with mock.patch.object(QListWidget, "__init__", lambda y: None):
                            with mock.patch.object(QListWidget, "__init__", lambda y: None):
                                with mock.patch.object(QListWidgetItem, "__init__", lambda x, y: None):
                                    QLineEdit.setEnabled = MagicMock()
                                    self._view.annots_order = []
                                    self._view.default_vals = []
                                    self._view.annotation_item_widgets = []
                                    QHBoxLayout.setContentsMargins = MagicMock()
                                    QHBoxLayout.setSpacing = MagicMock()
                                    QWidget.setLayout = MagicMock()
                                    QWidget.minimumSizeHint = MagicMock()
                                    QListWidgetItem.setSizeHint = MagicMock()
                                    self._view.annot_list = QListWidget()
                                    self._view.annot_list.setItemWidget = MagicMock()
                                    QHBoxLayout.addWidget = MagicMock()

                                    QHBoxLayout.setSizeConstraint = MagicMock()
                                    self._view._create_annot("name", {"type": "string", "default": ""})

                                    assert self._view.annots_order == ["name"]
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QLabel("name")))
                                    line_edit = QLineEdit("")
                                    assert QHBoxLayout().addWidget.has_call(mock.call(line_edit))
                                    assert self._view.default_vals == [""]
                                    assert len(self._view.annotation_item_widgets) == 1
                                    assert type(self._view.annotation_item_widgets[0]) == type(QLineEdit(""))
                                    QLineEdit("").setEnabled.assert_called_once_with(True)
                                    QHBoxLayout().setContentsMargins.assert_called_once_with(2, 12, 8, 12)
                                    QHBoxLayout().setSpacing.assert_called_once_with(2)
                                    QWidget().setLayout.assert_called_once_with(ANY)
                                    assert isinstance(QWidget().setLayout.call_args_list[0][0][0], QHBoxLayout)

                                    QListWidgetItem(self._view.annot_list).setSizeHint.assert_called_once_with(
                                        QWidget().minimumSizeHint()
                                    )

                                    self._view.annot_list.setItemWidget.assert_called_once_with(ANY, ANY)
                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][0], QListWidgetItem
                                    )

                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][1], QWidget
                                    )

    def test_create_annot_number(self):
        with mock.patch.object(QWidget, "__init__", lambda x: None):
            with mock.patch.object(QHBoxLayout, "__init__", lambda x: None):
                with mock.patch.object(QLabel, "__init__", lambda x, y: None):
                    with mock.patch.object(QSpinBox, "__init__", lambda y: None):
                        with mock.patch.object(QListWidget, "__init__", lambda y: None):
                            with mock.patch.object(QListWidget, "__init__", lambda y: None):
                                with mock.patch.object(QListWidgetItem, "__init__", lambda x, y: None):
                                    QSpinBox.setEnabled = MagicMock()
                                    QSpinBox.setValue = MagicMock()
                                    self._view.annots_order = []
                                    self._view.default_vals = []
                                    self._view.annotation_item_widgets = []
                                    QHBoxLayout.setContentsMargins = MagicMock()
                                    QHBoxLayout.setSpacing = MagicMock()
                                    QWidget.setLayout = MagicMock()
                                    QWidget.minimumSizeHint = MagicMock()
                                    QListWidgetItem.setSizeHint = MagicMock()
                                    self._view.annot_list = QListWidget()
                                    self._view.annot_list.setItemWidget = MagicMock()
                                    QHBoxLayout.addWidget = MagicMock()

                                    QHBoxLayout.setSizeConstraint = MagicMock()
                                    self._view._create_annot("name", {"type": "number", "default": 2})

                                    assert self._view.annots_order == ["name"]
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QLabel("name")))
                                    QSpinBox().setValue.assert_called_once_with(2)
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QSpinBox()))
                                    assert self._view.default_vals == [2]
                                    assert len(self._view.annotation_item_widgets) == 1
                                    assert type(self._view.annotation_item_widgets[0]) == type(QSpinBox())
                                    QSpinBox().setEnabled.assert_called_once_with(True)
                                    QHBoxLayout().setContentsMargins.assert_called_once_with(2, 12, 8, 12)
                                    QHBoxLayout().setSpacing.assert_called_once_with(2)
                                    QWidget().setLayout.assert_called_once_with(ANY)
                                    assert isinstance(QWidget().setLayout.call_args_list[0][0][0], QHBoxLayout)

                                    QListWidgetItem(self._view.annot_list).setSizeHint.assert_called_once_with(
                                        QWidget().minimumSizeHint()
                                    )

                                    self._view.annot_list.setItemWidget.assert_called_once_with(ANY, ANY)
                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][0], QListWidgetItem
                                    )

                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][1], QWidget
                                    )

    def test_create_annot_bool_true(self):
        with mock.patch.object(QWidget, "__init__", lambda x: None):
            with mock.patch.object(QHBoxLayout, "__init__", lambda x: None):
                with mock.patch.object(QLabel, "__init__", lambda x, y: None):
                    with mock.patch.object(QCheckBox, "__init__", lambda y: None):
                        with mock.patch.object(QListWidget, "__init__", lambda y: None):
                            with mock.patch.object(QListWidget, "__init__", lambda y: None):
                                with mock.patch.object(QListWidgetItem, "__init__", lambda x, y: None):
                                    QCheckBox.setEnabled = MagicMock()
                                    QCheckBox.setChecked = MagicMock()
                                    self._view.annots_order = []
                                    self._view.default_vals = []
                                    self._view.annotation_item_widgets = []
                                    QHBoxLayout.setContentsMargins = MagicMock()
                                    QHBoxLayout.setSpacing = MagicMock()
                                    QWidget.setLayout = MagicMock()
                                    QWidget.minimumSizeHint = MagicMock()
                                    QListWidgetItem.setSizeHint = MagicMock()
                                    self._view.annot_list = QListWidget()
                                    self._view.annot_list.setItemWidget = MagicMock()
                                    QHBoxLayout.addWidget = MagicMock()

                                    QHBoxLayout.setSizeConstraint = MagicMock()
                                    self._view._create_annot("name", {"type": "bool", "default": True})

                                    assert self._view.annots_order == ["name"]
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QLabel("name")))
                                    QCheckBox().setChecked.assert_called_once_with(True)
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QCheckBox()))
                                    assert self._view.default_vals == [True]
                                    assert len(self._view.annotation_item_widgets) == 1
                                    assert type(self._view.annotation_item_widgets[0]) == type(QCheckBox())
                                    QCheckBox().setEnabled.assert_called_once_with(True)
                                    QHBoxLayout().setContentsMargins.assert_called_once_with(2, 12, 8, 12)
                                    QHBoxLayout().setSpacing.assert_called_once_with(2)
                                    QWidget().setLayout.assert_called_once_with(ANY)
                                    assert isinstance(QWidget().setLayout.call_args_list[0][0][0], QHBoxLayout)

                                    QListWidgetItem(self._view.annot_list).setSizeHint.assert_called_once_with(
                                        QWidget().minimumSizeHint()
                                    )

                                    self._view.annot_list.setItemWidget.assert_called_once_with(ANY, ANY)
                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][0], QListWidgetItem
                                    )

                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][1], QWidget
                                    )

    def test_create_annot_bool_false(self):
        with mock.patch.object(QWidget, "__init__", lambda x: None):
            with mock.patch.object(QHBoxLayout, "__init__", lambda x: None):
                with mock.patch.object(QLabel, "__init__", lambda x, y: None):
                    with mock.patch.object(QCheckBox, "__init__", lambda y: None):
                        with mock.patch.object(QListWidget, "__init__", lambda y: None):
                            with mock.patch.object(QListWidget, "__init__", lambda y: None):
                                with mock.patch.object(QListWidgetItem, "__init__", lambda x, y: None):
                                    QCheckBox.setEnabled = MagicMock()
                                    QCheckBox.setChecked = MagicMock()
                                    self._view.annots_order = []
                                    self._view.default_vals = []
                                    self._view.annotation_item_widgets = []
                                    QHBoxLayout.setContentsMargins = MagicMock()
                                    QHBoxLayout.setSpacing = MagicMock()
                                    QWidget.setLayout = MagicMock()
                                    QWidget.minimumSizeHint = MagicMock()
                                    QListWidgetItem.setSizeHint = MagicMock()
                                    self._view.annot_list = QListWidget()
                                    self._view.annot_list.setItemWidget = MagicMock()
                                    QHBoxLayout.addWidget = MagicMock()

                                    QHBoxLayout.setSizeConstraint = MagicMock()
                                    self._view._create_annot("name", {"type": "bool", "default": False})

                                    assert self._view.annots_order == ["name"]
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QLabel("name")))
                                    QCheckBox().setChecked.assert_not_called()
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QCheckBox()))
                                    assert self._view.default_vals == [False]
                                    assert len(self._view.annotation_item_widgets) == 1
                                    assert type(self._view.annotation_item_widgets[0]) == type(QCheckBox())
                                    QCheckBox().setEnabled.assert_called_once_with(True)
                                    QHBoxLayout().setContentsMargins.assert_called_once_with(2, 12, 8, 12)
                                    QHBoxLayout().setSpacing.assert_called_once_with(2)
                                    QWidget().setLayout.assert_called_once_with(ANY)
                                    assert isinstance(QWidget().setLayout.call_args_list[0][0][0], QHBoxLayout)

                                    QListWidgetItem(self._view.annot_list).setSizeHint.assert_called_once_with(
                                        QWidget().minimumSizeHint()
                                    )

                                    self._view.annot_list.setItemWidget.assert_called_once_with(ANY, ANY)
                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][0], QListWidgetItem
                                    )

                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][1], QWidget
                                    )

    def test_create_annot_list(self):
        with mock.patch.object(QWidget, "__init__", lambda x: None):
            with mock.patch.object(QHBoxLayout, "__init__", lambda x: None):
                with mock.patch.object(QLabel, "__init__", lambda x, y: None):
                    with mock.patch.object(QComboBox, "__init__", lambda y: None):
                        with mock.patch.object(QListWidget, "__init__", lambda y: None):
                            with mock.patch.object(QListWidget, "__init__", lambda y: None):
                                with mock.patch.object(QListWidgetItem, "__init__", lambda x, y: None):
                                    QComboBox.setEnabled = MagicMock()
                                    QComboBox.addItem = MagicMock()
                                    QComboBox.setCurrentText = MagicMock()
                                    self._view.annots_order = []
                                    self._view.default_vals = []
                                    self._view.annotation_item_widgets = []
                                    QHBoxLayout.setContentsMargins = MagicMock()
                                    QHBoxLayout.setSpacing = MagicMock()
                                    QWidget.setLayout = MagicMock()
                                    QWidget.minimumSizeHint = MagicMock()
                                    QListWidgetItem.setSizeHint = MagicMock()
                                    self._view.annot_list = QListWidget()
                                    self._view.annot_list.setItemWidget = MagicMock()
                                    QHBoxLayout.addWidget = MagicMock()
                                    QHBoxLayout.setSizeConstraint = MagicMock()
                                    self._view._create_annot(
                                        "name", {"type": "list", "default": "", "options": ["op1", "op2", "op3"]}
                                    )

                                    assert self._view.annots_order == ["name"]
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QLabel("name")))
                                    QComboBox().setCurrentText.assert_called_once_with("")
                                    QComboBox().addItem.assert_has_calls(
                                        [mock.call("op1"), mock.call("op2"), mock.call("op3")]
                                    )
                                    assert QHBoxLayout().addWidget.has_call(mock.call(QComboBox()))
                                    assert self._view.default_vals == [""]
                                    assert len(self._view.annotation_item_widgets) == 1
                                    assert type(self._view.annotation_item_widgets[0]) == type(QComboBox())
                                    QComboBox().setEnabled.assert_called_once_with(True)
                                    QHBoxLayout().setContentsMargins.assert_called_once_with(2, 12, 8, 12)
                                    QHBoxLayout().setSpacing.assert_called_once_with(2)
                                    QWidget().setLayout.assert_called_once_with(ANY)
                                    assert isinstance(QWidget().setLayout.call_args_list[0][0][0], QHBoxLayout)

                                    QListWidgetItem(self._view.annot_list).setSizeHint.assert_called_once_with(
                                        QWidget().minimumSizeHint()
                                    )

                                    self._view.annot_list.setItemWidget.assert_called_once_with(ANY, ANY)
                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][0], QListWidgetItem
                                    )

                                    assert isinstance(
                                        self._view.annot_list.setItemWidget.call_args_list[0][0][1], QWidget
                                    )

    def test_popup_yes(self):
        with mock.patch.object(QMessageBox, "__init__", lambda x: None):
            QMessageBox.setText = MagicMock()
            QMessageBox.setStandardButtons = MagicMock()
            QMessageBox.exec = MagicMock(return_value=QMessageBox.Yes)

            assert self._view.popup("text")
            QMessageBox.setText.assert_called_once_with("text")
            QMessageBox.setStandardButtons.assert_called_once_with(QMessageBox.No | QMessageBox.Yes)
            QMessageBox.exec.assert_called_once_with()

    def test_popup_no(self):
        with mock.patch.object(QMessageBox, "__init__", lambda x: None):
            QMessageBox.setText = MagicMock()
            QMessageBox.setStandardButtons = MagicMock()
            QMessageBox.exec = MagicMock(return_value=QMessageBox.No)

            assert not self._view.popup("text")
            QMessageBox.setText.assert_called_once_with("text")
            QMessageBox.setStandardButtons.assert_called_once_with(QMessageBox.No | QMessageBox.Yes)
            QMessageBox.exec.assert_called_once_with()
