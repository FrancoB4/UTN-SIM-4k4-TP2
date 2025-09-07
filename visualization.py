import pandas as pd
from PyQt5.QtCore import Qt, QAbstractTableModel


class PandasModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._df = df

    def rowCount(self, parent=None):
        return len(self._df)

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole): # type: ignore
        if role == Qt.DisplayRole: # type: ignore
            return str(self._df.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole): # type: ignore
        if role == Qt.DisplayRole: # type: ignore
            if orientation == Qt.Horizontal: # type: ignore
                return str(self._df.columns[section])
            if orientation == Qt.Vertical: # type: ignore
                return str(self._df.index[section])
        return None
