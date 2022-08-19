#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:35:20 2022

@author: Nishad Mandlik
"""

from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QApplication, QDesktopWidget
import sys


class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)
            return False
        return True


class WebEngineView(QWebEngineView):
    def __init__(self, url):
        QWebEngineView.__init__(self)
        self.setPage(WebEnginePage(self))
        self.setWindowTitle("PstrYve")
        self.showFullScreen()
        self.load(QUrl(url))
        self.show()


class WebApp():
    def __init__(self, url):
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        # Assignment is necessary. If widget is not assigned to a variable,
        # it gets destroyed once the function ends.
        self.wid = WebEngineView(url)

    def run(self):
        self.app.exec_()

    def end(self):
        self.app.quit()
