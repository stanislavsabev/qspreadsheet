import logging
from typing import Iterable, List, Optional

from qspreadsheet import qt
from qspreadsheet import resources_rc

logger = logging.getLogger(__name__)


class HeaderWidget(qt.QWidget):

    def __init__(self, labelText='', margins: Optional[qt.QMargins] = None, parent=None):
        super(HeaderWidget, self).__init__(parent)
        self._text = str(labelText)
        self.is_filtered = False

        self.label = qt.QLabel('') 
        self.button = qt.QPushButton('')
        self.margins = margins or qt.QMargins(2, 2, 2, 2)
        self._setup_label()
        self._setup_button()

        layout = qt.QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, 1, qt.Qt.AlignVCenter)
        layout.addWidget(self.button, 0, 1, 1, 1)
        layout.setSpacing(1)
        layout.setContentsMargins(qt.QMargins(2, 1, 2, 1))
        self.setLayout(layout)

    def text(self) -> str:
        return self._text
    
    @property
    def short_text(self) -> str:
        fm = qt.QFontMetrics(self.label.font())
        return fm.elidedText(
            self._text, qt.Qt.ElideRight, self.label.width())

    def _setup_label(self):
        self.label.setStyleSheet('''
            color: white;
            font: bold 12px ; ''')  # 'Consolas'
        self.label.setWordWrap(True)
        self.label.setText(self.short_text)

    def _setup_button(self):
        self.button.setObjectName(self._text)
        self.button.setFixedSize(qt.QSize(25, 20))
        self.button.setIcon(qt.QIcon(":/down-arrow-thin"))
        self.button.setIconSize(qt.QSize(12, 12))        

    def sizeHint(self) -> qt.QSize:
        fm = qt.QFontMetrics(self.label.font())
        width = max(fm.width(self.label.text()), 2) / 2 + self.width()
        return qt.QSize(width, self.height())

    def resizeEvent(self, event: qt.QResizeEvent):
        fm = qt.QFontMetrics(self.label.font())
        elided_text = fm.elidedText(
            self._text, qt.Qt.ElideRight, self.label.width())
        self.label.setText(elided_text)

    def set_filtered(self, filtered: bool):
        if filtered == self.is_filtered:
            return
        self.is_filtered = filtered
        icon_name = ":/down-arrow-orange" if filtered else ":/down-arrow-thin"
        self.button.setIcon(qt.QIcon(icon_name))
        self.button.setIconSize(qt.QSize(12, 12))


class HeaderView(qt.QHeaderView):

    def __init__(self, columns: Iterable[str], parent=None):
        super(HeaderView, self).__init__(qt.Qt.Horizontal, parent)

        self.header_widgets: List[HeaderWidget] = []
        self.filter_btn_mapper = qt.QSignalMapper(self)

        for name in columns:
            name = str(name)
            header_widget = HeaderWidget(labelText=name, parent=self)
            self.filter_btn_mapper.setMapping(header_widget.button, name)
            header_widget.button.clicked.connect(self.filter_btn_mapper.map)
            self.header_widgets.append(header_widget)

        self.sectionResized.connect(self.on_section_resized)
        self.sectionMoved.connect(self.on_section_moved)
        self.setStyleSheet('''
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #5dade2, stop: 0.5 #3498db,
                                                  stop: 0.6 #3498db, stop:1 #21618c);
                color: white;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 4px;
                padding-right: 4px;
                border: 1px solid #21618c; }''')

    def showEvent(self, e: qt.QShowEvent):
        for i, header in enumerate(self.header_widgets):
            header.setParent(self)
            self._set_item_geometry(header, i)
            header.show()
        super().showEvent(e)

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:
        
        return super().eventFilter(object, event)

    def sizeHint(self) -> qt.QSize:
        # insert space for our filter row
        super_sz_h = super().sizeHint()
        return qt.QSize(super_sz_h.width(), super_sz_h.height() + 10)

    def on_section_resized(self, i):
        logger.debug("\nstart =======")
        for ndx in range(i, len(self.header_widgets)):
            logical = self.logicalIndex(ndx)
            self._set_item_geometry(self.header_widgets[logical], logical)
        logger.debug("\nend =======\n")

    def _set_item_geometry(self, item: HeaderWidget, logical: int):
        x = self.sectionViewportPosition(logical) + item.margins.left()
        y = item.margins.top()
        w = self.sectionSize(logical) - item.margins.left() - item.margins.right() - 1
        h = self.height() + item.margins.top() + item.margins.bottom() - 1
        logger.debug("logical: %s", logical)
        logger.debug("\nx=%s  y=%s\nw=%s  h=%s", x, y, w, h)
        item.setGeometry(x, y, w, h)

    def on_section_moved(self, logical, oldVisualIndex, newVisualIndex):
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            self._set_item_geometry(self.header_widgets[i], logical)

    def fix_item_positions(self):
        for i, header in enumerate(self.header_widgets):
            self._set_item_geometry(header, i)

    def set_item_margin(self, index: int, margins: qt.QMargins):
        self.header_widgets[index].margins = margins