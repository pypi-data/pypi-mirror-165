from abc import ABC, abstractmethod


class ExportTaskInterface(ABC):
    @abstractmethod
    def run(self):
        pass
