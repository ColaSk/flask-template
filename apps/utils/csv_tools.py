import csv
import typing as t


class CSVService(object):
    """csv读写服务"""

    def __init__(self, path: str, mode: str = 'r+'):
        self.path = path
        self.mode = mode
        self._file = None
        self._writer = None
        self._reader = None
        self._dictreader = None

    @property
    def writer(self):
        if not self._writer:
            if not self._file:
                self._file = open(self.path, self.mode)
            self._writer = csv.writer(self._file)
        return self._writer

    @property
    def reader(self):
        if not self._reader:
            if not self._file:
                self._file = open(self.path, self.mode)
            self._reader = csv.reader(self._file)
        return self._reader

    @property
    def dictreader(self):
        if not self._dictreader:
            if not self._file:
                self._file = open(self.path, self.mode)
            self._dictreader = csv.DictReader(self._file)
        return self._dictreader

    def writerows(self, rows: t.Iterable[t.Iterable[t.Any]], processing_separator: bool = False):
        """写入多行数据"""
        if processing_separator:
            new_rows = []
            for row in rows:
                new_row = []
                for r in row:
                    if isinstance(r, str):
                        r = r.replace(',', '/')
                    new_row.append(r)
                new_rows.append(new_row)
            rows = new_rows
        self.writer.writerows(rows)

    def __del__(self):
        if self._file:
            self._file.close()
