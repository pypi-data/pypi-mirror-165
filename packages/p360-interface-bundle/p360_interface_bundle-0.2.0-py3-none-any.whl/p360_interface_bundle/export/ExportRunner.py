from typing import List
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class ExportRunner:
    def __init__(self, export_tasks: List[ExportTaskInterface]):
        self.__export_tasks = export_tasks

    def run(self):
        for export_task in self.__export_tasks:
            export_task.run()
