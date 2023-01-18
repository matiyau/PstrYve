#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:35:20 2022.

@author: Nishad Mandlik
"""

from PySide6.QtCore import QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEnginePage, QWebEngineProfile, QWebEngineUrlRequestInterceptor)
from PySide6.QtWidgets import QApplication, QMainWindow
import sys


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """Interceptor for adding headers (if any) to GET request."""

    def interceptRequest(self, info):
        """Overload of virtual function for request interception."""
        info.setHttpHeader("", "")


class WebEnginePage(QWebEnginePage):
    """Widget for holding the web content."""

    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        """
        Overload of virtual function for navigating to he specified URL.

        Parameters
        ----------
        url : PySide6.QtCore.QUrl
            URL of the webpage.
        _type : PySide6.QtWebEngineCore.QWebEnginePage.NavigationType
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

        # Assignment is necessary. If profile is not assigned to a variable,
        # it gets destroyed once the function ends.
        self.profile = QWebEngineProfile()
        self.profile.setUrlRequestInterceptor(WebEngineUrlRequestInterceptor())

        self.setPage(QWebEnginePage(self.profile, self))
        self.load(QUrl(url))


class RespThread(QThread):
    """Thread for listening to response from server."""

    resp_recd = Signal()

    def __init__(self, handler_func):
        QThread.__init__(self)
        self.handler = handler_func

    def run(self):
        """Run the thread's task."""
        try:
            self.handler()
        except KeyboardInterrupt:
            print("Cancelled by user")

        self.resp_recd.emit()


class WebApp():
    """Qt App for displaying web pages."""

    def __init__(self, url, resp_handler_func):
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        self.resp_thread = RespThread(resp_handler_func)
        self.resp_thread.resp_recd.connect(self.app.quit)
        self.resp_thread.start()

        # Assignment is necessary. If object is not assigned to a variable,
        # it gets destroyed once the function ends.
        self.main_window = QMainWindow()
        self.web_view_widget = WebEngineView(url)

        self.main_window.setCentralWidget(self.web_view_widget)
        self.main_window.setWindowTitle("PstrYve")
        self.main_window.showFullScreen()

    def run(self):
        """
        Start the GUI Application.

        Returns
        -------
        None.

        """
        self.app.exec()

    def end(self):
        """
        End the GUI Application.

        Returns
        -------
        None.

        """
        self.app.closeAllWindows()
