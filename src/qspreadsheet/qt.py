"""Bulk imports from the PySide2 package, to manage in one place."""

import os
import PySide2

plugin_path = os.path.join(os.path.dirname(
    PySide2.__file__), 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


from PySide2.QtCore import (QAbstractItemModel, QAbstractTableModel, QDate,
                            QDateTime, QMargins, QModelIndex, QObject, QPoint,
                            QRegExp, QRunnable, QSettings, QSignalMapper,
                            QSize, QSortFilterProxyModel, Qt, QThreadPool,
                            Signal, QEvent)
from PySide2.QtGui import (QBrush, QCloseEvent, QColor, QContextMenuEvent,
                           QFont, QFontMetrics, QIcon, QKeySequence, QPixmap,
                           QResizeEvent, QShowEvent, QTextCharFormat,
                           QTextDocument, QStandardItemModel, QPainter)
from PySide2.QtWidgets import (QAction, QApplication, QBoxLayout, QCheckBox,
                               QComboBox, QDateEdit, QDateTimeEdit,
                               QDoubleSpinBox, QGridLayout, QHBoxLayout,
                               QHeaderView, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMainWindow, QMenu,
                               QMessageBox, QPushButton, QSizePolicy, QSpinBox,
                               QStyle, QStyledItemDelegate,
                               QStyleOptionViewItem, QTableView, QTextEdit,
                               QVBoxLayout, QLayout, QWidget, QWidgetAction)
