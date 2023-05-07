#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import platform
import sys

from qspreadsheet import qt


class RichTextLineEdit(qt.QTextEdit):
    (
        Bold,
        Italic,
        Underline,
        StrikeOut,
        Monospaced,
        Sans,
        Serif,
        NoSuperOrSubscript,
        Subscript,
        Superscript,
    ) = range(10)

    def __init__(self, parent=None):
        super(RichTextLineEdit, self).__init__(parent)

        self.monofamily = "courier"
        self.sansfamily = "helvetica"
        self.seriffamily = "times"
        self.setLineWrapMode(qt.QTextEdit.NoWrap)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
        fm = qt.QFontMetrics(self.font())
        h = int(fm.height() * (1.4 if platform.system() == "Windows" else 1.2))
        self.setMinimumHeight(h)
        self.setMaximumHeight(int(h * 1.2))
        self.setToolTip(
            "Press <b>Ctrl+M</b> for the text effects "
            "menu and <b>Ctrl+K</b> for the color menu"
        )

    def toggleItalic(self):
        self.setFontItalic(not self.fontItalic())

    def toggleUnderline(self):
        self.setFontUnderline(not self.fontUnderline())

    def toggleBold(self):
        self.setFontWeight(
            qt.QFont.Normal if self.fontWeight() > qt.QFont.Normal else qt.QFont.Bold
        )

    def sizeHint(self):
        return qt.QSize(self.document().idealWidth() + 5, self.maximumHeight())

    def minimumSizeHint(self):
        fm = qt.QFontMetrics(self.font())
        return qt.QSize(fm.width("WWWW"), self.minimumHeight())

    def contextMenuEvent(self, event):
        self.textEffectMenu()

    def keyPressEvent(self, event):
        if event.modifiers() & qt.Qt.ControlModifier:
            handled = False
            if event.key() == qt.Qt.Key_B:
                self.toggleBold()
                handled = True
            elif event.key() == qt.Qt.Key_I:
                self.toggleItalic()
                handled = True
            elif event.key() == qt.Qt.Key_K:
                self.colorMenu()
                handled = True
            elif event.key() == qt.Qt.Key_M:
                self.textEffectMenu()
                handled = True
            elif event.key() == qt.Qt.Key_U:
                self.toggleUnderline()
                handled = True
            if handled:
                event.accept()
                return
        if event.key() in (qt.Qt.Key_Enter, qt.Qt.Key_Return):
            self.returnPressed.emit()
            event.accept()
        else:
            qt.QTextEdit.keyPressEvent(self, event)

    def colorMenu(self):
        pixmap = qt.QPixmap(22, 22)
        menu = qt.QMenu("Colour")
        for text, color in (
            ("&Black", qt.Qt.black),
            ("B&lue", qt.Qt.blue),
            ("Dark Bl&ue", qt.Qt.darkBlue),
            ("&Cyan", qt.Qt.cyan),
            ("Dar&k Cyan", qt.Qt.darkCyan),
            ("&Green", qt.Qt.green),
            ("Dark Gr&een", qt.Qt.darkGreen),
            ("M&agenta", qt.Qt.magenta),
            ("Dark Mage&nta", qt.Qt.darkMagenta),
            ("&Red", qt.Qt.red),
            ("&Dark Red", qt.Qt.darkRed),
        ):
            color = qt.QColor(color)
            pixmap.fill(color)
            action = menu.addAction(qt.QIcon(pixmap), text, self.setColor)
            action.setData(color)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(self.cursorRect().center()))

    def setColor(self):
        action = self.sender()
        if action is not None and isinstance(action, qt.QAction):
            color = qt.QColor(action.data())
            if color.isValid():
                self.setTextColor(color)

    def textEffectMenu(self):
        format = self.currentCharFormat()
        menu = qt.QMenu("Text Effect")
        for text, shortcut, data, checked in (
            (
                "&Bold",
                "Ctrl+B",
                RichTextLineEdit.Bold,
                self.fontWeight() > qt.QFont.Normal,
            ),
            ("&Italic", "Ctrl+I", RichTextLineEdit.Italic, self.fontItalic()),
            ("Strike &out", None, RichTextLineEdit.StrikeOut, format.fontStrikeOut()),
            ("&Underline", "Ctrl+U", RichTextLineEdit.Underline, self.fontUnderline()),
            (
                "&Monospaced",
                None,
                RichTextLineEdit.Monospaced,
                format.fontFamily() == self.monofamily,
            ),
            (
                "&Serifed",
                None,
                RichTextLineEdit.Serif,
                format.fontFamily() == self.seriffamily,
            ),
            (
                "S&ans Serif",
                None,
                RichTextLineEdit.Sans,
                format.fontFamily() == self.sansfamily,
            ),
            (
                "&No super or subscript",
                None,
                RichTextLineEdit.NoSuperOrSubscript,
                format.verticalAlignment() == qt.QTextCharFormat.AlignNormal,
            ),
            (
                "Su&perscript",
                None,
                RichTextLineEdit.Superscript,
                format.verticalAlignment() == qt.QTextCharFormat.AlignSuperScript,
            ),
            (
                "Subs&cript",
                None,
                RichTextLineEdit.Subscript,
                format.verticalAlignment() == qt.QTextCharFormat.AlignSubScript,
            ),
        ):
            action = menu.addAction(text, self.setTextEffect)
            if shortcut is not None:
                action.setShortcut(qt.QKeySequence(shortcut))
            action.setData(data)
            action.setCheckable(True)
            action.setChecked(checked)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(self.cursorRect().center()))

    def setTextEffect(self):
        action = self.sender()
        if action is not None and isinstance(action, qt.QAction):
            what = int(action.data())
            if what == RichTextLineEdit.Bold:
                self.toggleBold()
                return
            if what == RichTextLineEdit.Italic:
                self.toggleItalic()
                return
            if what == RichTextLineEdit.Underline:
                self.toggleUnderline()
                return
            format = self.currentCharFormat()
            if what == RichTextLineEdit.Monospaced:
                format.setFontFamily(self.monofamily)
            elif what == RichTextLineEdit.Serif:
                format.setFontFamily(self.seriffamily)
            elif what == RichTextLineEdit.Sans:
                format.setFontFamily(self.sansfamily)
            if what == RichTextLineEdit.StrikeOut:
                format.setFontStrikeOut(not format.fontStrikeOut())
            if what == RichTextLineEdit.NoSuperOrSubscript:
                format.setVerticalAlignment(qt.QTextCharFormat.AlignNormal)
            elif what == RichTextLineEdit.Superscript:
                format.setVerticalAlignment(qt.QTextCharFormat.AlignSuperScript)
            elif what == RichTextLineEdit.Subscript:
                format.setVerticalAlignment(qt.QTextCharFormat.AlignSubScript)
            self.mergeCurrentCharFormat(format)

    def toSimpleHtml(self):
        html = ""
        black = qt.QColor(qt.Qt.black)
        block = self.document().begin()
        while block.isValid():
            iterator = block.begin()
            while iterator != block.end():
                fragment = iterator.fragment()
                if fragment.isValid():
                    format = fragment.charFormat()
                    family = format.fontFamily()
                    color = format.foreground().color()
                    text = qt.QRegExp.escape(fragment.text())
                    if format.verticalAlignment() == qt.QTextCharFormat.AlignSubScript:
                        text = "<sub>{}</sub>".format(text)
                    elif format.verticalAlignment() == qt.QTextCharFormat.AlignSuperScript:
                        text = "<sup>{}</sup>".format(text)
                    if format.fontUnderline():
                        text = "<u>{}</u>".format(text)
                    if format.fontItalic():
                        text = "<i>{}</i>".format(text)
                    if format.fontWeight() > qt.QFont.Normal:
                        text = "<b>{}</b>".format(text)
                    if format.fontStrikeOut():
                        text = "<s>{}</s>".format(text)
                    if color != black or family:
                        attribs = ""
                        if color != black:
                            attribs += ' color="{}"'.format(color.name())
                        if family:
                            attribs += ' face="{}"'.format(family)
                        text = "<font{}>{}</font>".format(attribs, text)
                    html += text
                iterator += 1
            block = block.next()
        return html


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    lineedit = RichTextLineEdit()
    lineedit.show()
    lineedit.setWindowTitle("RichTextEdit")
    app.exec_()
    print(lineedit.toHtml())
    print(lineedit.toPlainText())
    print(lineedit.toSimpleHtml())
