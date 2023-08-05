from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from qtpy import QtWidgets as QtW
from qtpy.QtCore import Qt, QTimer
from ._base import QBaseTable, _QTableViewEnhanced, DataFrameModel

if TYPE_CHECKING:
    import pandas as pd


def _get_standard_icon(x):
    return QtW.QApplication.style().standardIcon(x)


class QPlayButton(QtW.QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._RUN = _get_standard_icon(QtW.QStyle.StandardPixmap.SP_MediaPlay)
        self._PAUSE = _get_standard_icon(QtW.QStyle.StandardPixmap.SP_MediaPause)
        self.clicked.connect(self.switchRunning)
        self.setRunning(True)

    def running(self):
        return self._running

    def setRunning(self, val: bool):
        self._running = val
        if val:
            self.setIcon(self._PAUSE)
        else:
            self.setIcon(self._RUN)

    def switchRunning(self, *_):
        self.setRunning(not self.running())


# TODO: don't initialize filter and only accept function filter.
class QTableDisplay(QBaseTable):
    def __init__(
        self,
        parent: QtW.QWidget | None = None,
        loader: Callable[[], pd.DataFrame] = None,
        interval_ms: int = 1000,
    ):
        import pandas as pd

        super().__init__(parent, pd.DataFrame([]))
        if loader is None:
            self._loader = lambda: pd.DataFrame([])
        else:
            self._loader = lambda: pd.DataFrame(loader())
        self._refreshing = False
        self._qtimer = QTimer()
        self._qtimer.setSingleShot(True)
        self._qtimer.setInterval(interval_ms)
        self._qtimer.setTimerType(Qt.TimerType.PreciseTimer)
        self._qtimer.timeout.connect(self.refreshCallback)

        self._interval_spinbox.valueChanged.connect(self._qtimer.setInterval)
        self._interval_spinbox.setValue(self._qtimer.interval())

        if self._play_button.running():
            self._qtimer.start()

    def copy(self, link: bool = True) -> QTableDisplay:
        copy = self.__class__(self.parent(), self.loader(), self._qtimer.interval())
        if link:
            copy._qtable_view.setModel(self._qtable_view.model())
            copy._qtable_view.setSelectionModel(self._qtable_view.selectionModel())
        return copy

    if TYPE_CHECKING:

        def model(self) -> DataFrameModel:
            ...

    def refreshCallback(self):
        """Run refresh if needed."""
        if self._play_button.running() and not self._refreshing:
            self.refresh()

    def loader(self) -> Callable:
        """Return the loader function."""
        return self._loader

    def setLoader(self, loader: Callable) -> None:
        """Set the loader function and refresh."""
        if not callable(loader):
            raise TypeError("loader must be callable")
        self._loader = loader
        self.refresh()

    def getDataFrame(self) -> pd.DataFrame:
        return self._data_raw

    def setDataFrame(self, data: pd.DataFrame) -> None:
        self._data_raw = data
        self.model().df = data
        self._qtable_view.viewport().update()
        return

    def createModel(self):
        model = DataFrameModel(self)
        self._qtable_view.setModel(model)
        return None

    @property
    def _qtable_view(self) -> _QTableViewEnhanced:
        return self._qtable_view_

    def createQTableView(self):
        self._qtable_view_ = _QTableViewEnhanced(self)

        _header = QtW.QWidget()
        _header_layout = QtW.QHBoxLayout()
        _header_layout.setContentsMargins(2, 2, 2, 2)
        _header_layout.addWidget(QtW.QLabel("Interval (ms):"))

        self._interval_spinbox = QtW.QSpinBox()
        self._interval_spinbox.setMinimum(10)
        self._interval_spinbox.setMaximum(10000)
        _header_layout.addWidget(self._interval_spinbox)

        self._play_button = QPlayButton()

        @self._play_button.clicked.connect
        def _clicked(*_):
            if self._qtimer.isActive():
                self._qtimer.stop()
            else:
                self._qtimer.start()

        _header_layout.addWidget(self._play_button)
        _header.setLayout(_header_layout)

        _main_layout = QtW.QVBoxLayout()
        _main_layout.setContentsMargins(0, 0, 0, 0)
        _main_layout.addWidget(_header)
        _main_layout.addWidget(self._qtable_view_)
        wdt = QtW.QWidget()
        wdt.setLayout(_main_layout)
        self.addWidget(wdt)

    def refresh(self) -> None:
        self._refreshing = True
        if self.isVisible():
            try:
                self._data_raw = self._loader()
            except Exception as e:
                return
            self.model().df = self._data_raw

        self._refreshing = False
        if self._play_button.running():
            self._qtimer.start()
        else:
            self._qtimer.stop()
        return super().refreshTable()
