import logging
from datetime import datetime
from typing import Any, Dict, Mapping, Optional, Union

import numpy as np
import pandas as pd

from qspreadsheet import qt
from qspreadsheet import DF, MAX_FLOAT, MAX_INT
from qspreadsheet.custom_widgets import RichTextLineEdit

DateLike = Union[str, datetime, pd.Timestamp, qt.QDate]
logger = logging.getLogger(__name__)


class ColumnDelegate(qt.QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(ColumnDelegate, self).__init__(parent)

    def display_data(self, index: qt.QModelIndex, value: Any) -> str:
        del index  # not used
        if pd.isnull(value):
            return ".NA"
        return str(value)

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        del index  # not used
        return qt.Qt.AlignLeft | qt.Qt.AlignVCenter

    def background_brush(self, index: qt.QModelIndex) -> qt.QBrush:
        del index  # not used
        return None

    def foreground_brush(self, index: qt.QModelIndex) -> qt.QBrush:
        del index  # not used
        return None

    def font(self, index: qt.QModelIndex) -> qt.QFont:
        del index  # not used
        return None

    def null_value(self) -> Any:
        return None

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return None

    def to_nullable(self) -> "NullableDelegate":
        return NullableDelegate(self)

    def to_non_nullable(self) -> "ColumnDelegate":
        return self


class NullableDelegate(ColumnDelegate):
    def __init__(self, column_delegate: ColumnDelegate):
        super(NullableDelegate, self).__init__(column_delegate.parent())
        self._delegate = column_delegate
        self.checkbox: Optional[qt.QCheckBox] = None
        self._editor: Optional[qt.QWidget] = None

    def __repr__(self) -> str:
        managed_name = self._delegate.__class__.__name__
        return "{}[{}] at {}".format(
            self.__class__.__name__, managed_name, hex(id(self))
        )

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        nullable_editor = qt.QWidget(parent)
        nullable_editor.setAutoFillBackground(True)

        self.checkbox = qt.QCheckBox("")
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.on_checkboxStateChanged)

        editor = self._delegate.createEditor(parent, option, index)
        editor.setParent(nullable_editor)
        editor.setSizePolicy(
            qt.QSizePolicy.MinimumExpanding, qt.QSizePolicy.MinimumExpanding
        )
        editor.setFocus(qt.Qt.MouseFocusReason)
        self._editor = editor

        layout = qt.QHBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        nullable_editor.setLayout(layout)
        return nullable_editor

    def on_checkboxStateChanged(self, state: int):
        isnull = state == qt.Qt.Unchecked
        self._editor.setEnabled(not isnull)

    def setEditorData(self, editor: qt.QWidget, index: qt.QModelIndex):
        del editor  # not used
        self._delegate.setEditorData(self._editor, index)

    def setModelData(
        self, editor: qt.QWidget, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        del editor  # not used
        if self.checkbox.checkState() == qt.Qt.Checked:
            self._delegate.setModelData(self._editor, model, index)
        elif self.checkbox.checkState() == qt.Qt.Unchecked:
            model.setData(index, self._delegate.null_value())

    def display_data(self, index: qt.QModelIndex, value: Any) -> Any:
        return self._delegate.display_data(index, value)

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        return self._delegate.alignment(index)

    def default_value(self, index: qt.QModelIndex) -> Any:
        return self._delegate.default_value(index)

    def null_value(self) -> Any:
        return self._delegate.null_value()

    def to_nullable(self) -> "NullableDelegate":
        return self

    def to_non_nullable(self) -> ColumnDelegate:
        return self._delegate


# region MasterDelegate specific


class MasterDelegate(ColumnDelegate):
    def __init__(self, parent=None):
        super(MasterDelegate, self).__init__(parent=parent)
        self.delegates: Dict[int, ColumnDelegate] = {}

    def add_column_delegate(self, column_index: int, delegate: ColumnDelegate):
        delegate.setParent(self)
        self.delegates[column_index] = delegate

    def remove_column_delegate(self, column_index: int):
        delegate = self.delegates.pop(column_index, None)
        if delegate is not None:
            delegate.deleteLater()
            del delegate

    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            qt.QStyledItemDelegate.paint(self, painter, option, index)

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return qt.QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor: qt.QWidget, index: qt.QModelIndex):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            qt.QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(
        self, editor: qt.QWidget, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            qt.QStyledItemDelegate.setModelData(self, editor, model, index)

    def display_data(self, index: qt.QModelIndex, value: Any) -> str:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.display_data(index, value)
        else:
            return super().display_data(index, value)

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.alignment(index)
        return super().alignment(index)

    def background_brush(self, index: qt.QModelIndex) -> qt.QBrush:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.background_brush(index)
        return super().background_brush(index)

    def foreground_brush(self, index: qt.QModelIndex) -> qt.QBrush:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.foreground_brush(index)
        return super().foreground_brush(index)

    def font(self, index: qt.QModelIndex) -> qt.QFont:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.font(index)
        return super().font(index)

    def default_value(self, index: qt.QModelIndex) -> Any:
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.default_value(index)
        return super().default_value(index)

    @property
    def non_nullable_delegates(self):
        return {
            ndx: delegate
            for ndx, delegate in self.delegates.items()
            if not isinstance(delegate, NullableDelegate)
        }

    @property
    def nullable_delegates(self):
        return {
            ndx: delegate
            for ndx, delegate in self.delegates.items()
            if isinstance(delegate, NullableDelegate)
        }

    def to_nullable(self) -> "NullableDelegate":
        return self


# endregion MasterDelegate specific


# region Type delegates


class IntDelegate(ColumnDelegate):
    def __init__(
        self, parent=None, minimum: Optional[int] = None, maximum: Optional[int] = None
    ):
        super(IntDelegate, self).__init__(parent)
        self.minimum = minimum or -MAX_INT
        self.maximum = maximum or MAX_INT
        self._default = 0

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del index, option  # not used
        editor = qt.QSpinBox(parent)
        editor.setRange(self.minimum, self.maximum)
        editor.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        return editor

    def setEditorData(self, editor: qt.QSpinBox, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = (
            self.default_value(index) if pd.isnull(model_value) else int(model_value)
        )
        editor.setValue(value)

    def setModelData(
        self, editor: qt.QSpinBox, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        editor.interpretText()
        model.setData(index, editor.value())

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        del index  # not used
        return qt.Qt.AlignRight | qt.Qt.AlignVCenter

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self._default

    def null_value(self) -> Any:
        return pd.NA


class FloatDelegate(ColumnDelegate):
    def __init__(
        self,
        parent=None,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        edit_precision: int = 4,
        display_precision: int = 2,
    ):
        super(FloatDelegate, self).__init__(parent)
        self.minimum = minimum or -MAX_FLOAT
        self.maximum = maximum or MAX_FLOAT
        self.edit_precision = edit_precision
        self.display_precision = display_precision
        self._default = 0

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del index, option  # not used
        editor = qt.QDoubleSpinBox(parent)
        editor.setRange(self.minimum, self.maximum)
        editor.setDecimals(self.edit_precision)
        editor.setSingleStep(0.1)
        editor.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        return editor

    def setEditorData(self, editor: qt.QDoubleSpinBox, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = (
            self.default_value(index) if pd.isnull(model_value) else float(model_value)
        )
        editor.setValue(value)

    def setModelData(
        self,
        editor: qt.QDoubleSpinBox,
        model: qt.QAbstractItemModel,
        index: qt.QModelIndex,
    ):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value)

    def display_data(self, index: qt.QModelIndex, value: Any) -> str:
        if pd.isnull(value):
            return super().display_data(index, value)
        return "{0:.{1}f}".format(value, self.display_precision)

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        del index  # not used
        return qt.Qt.AlignRight | qt.Qt.AlignVCenter

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self._default

    def null_value(self) -> Any:
        return np.nan


class BoolDelegate(ColumnDelegate):
    def __init__(self, parent=None) -> None:
        super(BoolDelegate, self).__init__(parent)
        self.choices = [True, False]
        self._default = False

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del option  # not used
        editor = qt.QComboBox(parent)
        editor.addItems(list(map(str, self.choices)))
        editor.setEditable(True)
        editor.lineEdit().setReadOnly(True)
        editor.lineEdit().setAlignment(self.alignment(index))
        return editor

    def setEditorData(self, editor: qt.QComboBox, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = (
            self.default_value(index)
            if pd.isnull(model_value)
            else self.choices.index(model_value)
        )
        editor.setCurrentIndex(value)

    def setModelData(
        self, editor: qt.QComboBox, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        value = self.choices[editor.currentIndex()]
        model.setData(index, value)

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        del index  # not used
        return qt.Qt.AlignCenter

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self.choices.index(self._default)

    def null_value(self) -> Any:
        return pd.NA


class DateDelegate(ColumnDelegate):
    def __init__(
        self,
        parent=None,
        minimum: Optional[DateLike] = None,
        maximum: Optional[DateLike] = None,
        date_format="yyyy-MM-dd",
    ):
        super(DateDelegate, self).__init__(parent)
        self.minimum = as_qdate(minimum) if minimum else qt.QDate(1970, 1, 1)
        self.maximum = as_qdate(maximum) if maximum else qt.QDate(9999, 1, 1)
        self.date_format = date_format
        self._default = qt.QDate.currentDate()

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del index, option  # not used
        editor = qt.QDateEdit(parent)
        editor.setDateRange(self.minimum, self.maximum)
        editor.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        editor.setDisplayFormat(self.date_format)
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor: qt.QDateEdit, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = (
            self.default_value(index)
            if pd.isnull(model_value)
            else as_qdate(model_value)
        )
        editor.setDate(value)

    def setModelData(
        self, editor: qt.QDateEdit, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        model.setData(index, pd.to_datetime(editor.date().toPython()))

    def display_data(self, index: qt.QModelIndex, value: pd.Timestamp) -> Any:
        del index  # not used
        if pd.isnull(value):
            return ".NaT"
        result = as_qdate(value).toString(self.date_format)
        return result

    def alignment(self, index: qt.QModelIndex) -> qt.Qt.Alignment:
        del index  # not used
        return qt.Qt.AlignRight | qt.Qt.AlignVCenter

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self._default

    def null_value(self) -> Any:
        return pd.NaT


class StringDelegate(ColumnDelegate):
    def __init__(self, parent=None) -> None:
        super(StringDelegate, self).__init__(parent)
        self._default = ""

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del index, option  # not used
        editor = qt.QLineEdit(parent)
        return editor

    def setEditorData(self, editor: qt.QLineEdit, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = (
            self.default_value(index) if pd.isnull(model_value) else str(model_value)
        )
        editor.setText(value)

    def setModelData(
        self, editor: qt.QLineEdit, model: qt.QAbstractItemModel, index: qt.QModelIndex
    ):
        model.setData(index, editor.text())

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self._default


class RichTextDelegate(ColumnDelegate):
    def __init__(self, parent=None):
        super(RichTextDelegate, self).__init__(parent)
        self._default = ""

    def paint(self, painter, option, index: qt.QModelIndex):
        text = index.model().data(index, qt.Qt.DisplayRole)
        palette = qt.QApplication.palette()
        document = qt.QTextDocument()
        document.setDefaultFont(option.font)
        if option.state & qt.QStyle.State_Selected:
            document.setHtml(
                "<font color={}>{}</font>".format(
                    palette.highlightedText().color().name(), text
                )
            )
        else:
            document.setHtml(text)
        painter.save()
        color = (
            palette.highlight().color()
            if option.state & qt.QStyle.State_Selected
            else qt.QColor(index.model().data(index, qt.Qt.BackgroundColorRole))
        )
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index: qt.QModelIndex):
        text = index.model().data(index)
        document = qt.QTextDocument()
        document.setDefaultFont(option.font)
        document.setHtml(text)
        return qt.QSize(document.idealWidth() + 5, option.fontMetrics.height())

    def createEditor(
        self, parent: qt.QWidget, option: qt.QStyleOptionViewItem, index: qt.QModelIndex
    ) -> qt.QWidget:
        del index, option  # not used
        editor = RichTextLineEdit(parent)
        return editor

    def setEditorData(self, editor: RichTextLineEdit, index: qt.QModelIndex):
        model_value = index.model().data(index, qt.Qt.EditRole)
        value = self.default_value(index) if pd.isnull(model_value) else model_value
        editor.setHtml(value)

    def setModelData(
        self,
        editor: RichTextLineEdit,
        model: qt.QAbstractItemModel,
        index: qt.QModelIndex,
    ):
        model.setData(index, editor.toSimpleHtml())

    def to_nullable(self) -> "NullableDelegate":
        return self

    def default_value(self, index: qt.QModelIndex) -> Any:
        del index  # not used
        return self._default


# endregion Type delegates


def automap_delegates(
    df: DF, nullable: Union[bool, Mapping[Any, bool]] = True
) -> Dict[Any, ColumnDelegate]:
    dtypes = df.dtypes.astype(str)

    delegates = {}
    for columnname, dtype in dtypes.items():
        for key, delegate_class in default_delegates.items():
            if key in dtype:
                delegate = delegate_class()
                break
        else:
            delegate = StringDelegate()

        delegates[columnname] = delegate

    if isinstance(nullable, bool):
        if nullable:
            delegates = {
                column: delegate.to_nullable() for column, delegate in delegates.items()
            }
    elif isinstance(nullable, Mapping):
        for columnname, delegate in delegates.items():
            if nullable.get(columnname, False):
                delegates[columnname] = delegate.to_nullable()
    else:
        raise TypeError("Invalid type for `nullable`.")

    return delegates


def as_qdate(datelike: DateLike, format: Optional[str] = None) -> qt.QDate:
    """Converts date-like value to QDate

    Parameters
    ----------
    dt: {str, datetime, pd.Timestamp, QDate}: value to convert

    format: {str}: default=None. Format must be provided if dt is `str`.

    Returns
    -------
    `QDate`
    """
    if isinstance(datelike, str):
        datelike = datetime.strptime(datelike, format)
    return (
        datelike
        if isinstance(datelike, qt.QDate)
        else qt.QDate(datelike.year, datelike.month, datelike.day)
    )


default_delegates = dict(
    (
        ("object", StringDelegate),
        ("int", IntDelegate),
        ("float", FloatDelegate),
        ("datetime", DateDelegate),
        ("bool", BoolDelegate),
    )
)
