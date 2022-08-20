#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:35:20 2022.

@author: Nishad Mandlik
"""

from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QApplication
import sys


class WebEnginePage(QWebEnginePage):
    """Widget for holding the web content."""

    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        """
        Overload of virtual function for navigating to he specified URL.

        Parameters
        ----------
        url : PySide2.QtCore.QUrl
            URL of the webpage.
        _type : PySide2.QtWebEngineWidgets.QWebEnginePage.NavigationType
            Type of navigation (link clicked, form submitted, reload, etc.).
        isMainFrame : bool
            Specifies whether the request corresponds to the main frame or a
            child frame.

        Returns
        -------
        bool
            True if navigation is successful and URL is loaded,
            False otherwise.

        """
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)
            return False
        return True


class WebEngineView(QWebEngineView):
    """Widget for displaying the web page."""

    def __init__(self, url):
        QWebEngineView.__init__(self)
        self.setPage(WebEnginePage(self))
        self.setWindowTitle("PstrYve")
        self.showFullScreen()
        self.load(QUrl(url))
        self.show()


class WebApp():
    """Qt App for displaying web pages."""

    def __init__(self, url):
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        # Assignment is necessary. If widget is not assigned to a variable,
        # it gets destroyed once the function ends.
        self.wid = WebEngineView(url)

    def run(self):
        """
        Start the GUI Application.

        Returns
        -------
        None.

        """
        self.app.exec_()

    def end(self):
        """
        End the GUI Application.

        Returns
        -------
        None.

        """
        self.app.quit()
