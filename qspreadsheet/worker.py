import sys
from typing import Callable

from qspreadsheet import qt


class WorkerSignals(qt.QObject):

    about_to_start = qt.Signal()
    result = qt.Signal(object)
    error = qt.Signal(tuple)  # Tuple[Type[BaseException], BaseException, TracebackType]
    finished = qt.Signal()
    progress = qt.Signal(int, str)


class Worker(qt.QRunnable):

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    def run(self) -> None:
        try:
            self.signals.about_to_start.emit()
            result = self.func(*self.args, **self.kwargs)
        except Exception:
            self.signals.error.emit(sys.exc_info())
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()