import matplotlib
import pandas as pd

from visualization import PandasModel
matplotlib.use('Qt5Agg')


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QComboBox, QLineEdit, QPushButton, QApplication, QLabel, QStackedLayout
)

from PyQt5.QtGui import QKeySequence

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from generators import *


class CopyableTableView(QTableView):
    def keyPressEvent(self, e):
        if e.matches(QKeySequence.Copy):  # type: ignore
            self.copySelectionToClipboard()
        else:
            super().keyPressEvent(e)

    def copySelectionToClipboard(self):
        selection = self.selectionModel()
        if not selection.hasSelection():  # type: ignore
            return

        indexes = selection.selectedIndexes()  # type: ignore
        if not indexes:
            return

        indexes = sorted(indexes, key=lambda x: (x.row(), x.column()))

        rows = []
        current_row = indexes[0].row()
        row_data = []

        for idx in indexes:
            if idx.row() != current_row:
                rows.append('\t'.join(row_data))
                row_data = []
                current_row = idx.row()
            row_data.append(idx.data())
        rows.append('\t'.join(row_data))

        clipboard_text = '\n'.join(rows)

        QApplication.clipboard().setText(clipboard_text.replace('.', ','))  # type: ignore


class HistogramWidget(FigureCanvasQTAgg):
    def __init__(self, x, intervals, label: str, width: int = 5, height: int = 4, dpi: int = 100, parent=None):
        self.x = x
        self.intervals = intervals
        self.label = label
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.add_subplot(111)
        super().__init__(fig)
        
    def update_histogram(self, x=None, intervals: int | None = None):
        if x is not None:
            self.x = x
            
        if intervals is not None:
            self.intervals = intervals
        
        ax = self.figure.get_axes()[0]
        ax.clear()

        self.counts, self.bin_edges, patches = ax.hist(
            self.x, bins=self.intervals, alpha=0.7
        )

        labels = [f"[{self.bin_edges[i]:.2f}, {self.bin_edges[i+1]:.2f})" for i in range(len(self.bin_edges)-1)]

        for patch, label in zip(patches, labels): #type: ignore
            patch.set_label(label)

        ax.legend(fontsize=8, title="Intervalos")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Histograma de distribución de frecuencia")

        self.draw()
        return self.counts, self.bin_edges


class RightPanel(QWidget):
    def __init__(self, x, update_dist_table, left_panel, label: str = '', parent=None):
        super().__init__(parent)
        
        self.update_dist_table = update_dist_table
        self.left_panel = left_panel
        
        self.x = x
        self.label = label
        
        self.setWindowTitle('Panel Derecho')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(['5', '10', '15', '20', '25'])
        
        self.histogram = HistogramWidget(self.x, 5, self.label, width=7, height=5)
        
        self.combo.currentTextChanged.connect(self.update_plot)
        
        layout.addWidget(self.combo)
        layout.addWidget(self.histogram)

        self.setLayout(layout)
        
    def update_plot(self, intervals: str):
        counts, bin_edges = self.histogram.update_histogram(intervals=int(intervals))
        self.update_dist_table(counts, bin_edges)
        
    def update_plot_data(self, x):
        self.x = x
        return self.histogram.update_histogram(x=self.x)


class LeftPanel(QWidget):
    def __init__(self, update_plot, parent=None):
        super().__init__(parent)
        
        self.update_plot = update_plot
        
        self.setWindowTitle('Configuración de la variable')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        
        self._add_configuration(layout)

        self.error_label = QLabel('', self)
        self.error_label.setStyleSheet('color: red;')
        layout.addWidget(self.error_label)
        
        self.generate_button = QPushButton('Generar variable aleatoria', self)
        self.generate_button.clicked.connect(self.on_generate)
        layout.addWidget(self.generate_button)

        btn = QPushButton('Valores')
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.table = CopyableTableView()
        self.stacklayout.addWidget(self.table)
        
        btn = QPushButton('Distribución de frecuencias')
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.dist_table = CopyableTableView()
        self.stacklayout.addWidget(self.dist_table)
        
        #self.table = CopyableTableView()
        #layout.addWidget(self.table)
        layout.addLayout(button_layout)
        layout.addLayout(self.stacklayout)

        self.setLayout(layout)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)
    
    def _add_configuration(self, layout: QVBoxLayout):
        raise NotImplementedError('This method should be implemented in subclasses.')
    
    def _check_inputs(self):
        if not self.n_input.text().replace('-', '').isdigit():
            self.error_label.setText('Error: El tamaño de la muestra debe ser un número.')
            return False
        
        if not int(self.n_input.text()) > 0:
            self.error_label.setText('Error: El tamaño de la muestra debe ser mayor que 0.')
            return False
        
        if not int(self.n_input.text()) <= 1_000_000:
            self.error_label.setText('Error: El tamaño de la muestra debe ser menor que 1.000.000.')
            return False
        
        return True
    
    def _get_data(self):
        raise NotImplementedError('This method should be implemented in subclasses.')

    def on_generate(self):
        self.data = self._get_data()
        self.table.setModel(PandasModel(pd.DataFrame(self.data, columns=['Valores'])))
        self.table.resizeColumnsToContents()
        counts, bin_edges = self.update_plot(self.data)
        self.update_dist_table(counts, bin_edges)
        
    def update_dist_table(self, counts, bin_edges):
        counts, bin_edges = self.update_plot(self.data)
        min_edges = [0] * len(counts)
        max_edges = [0] * len(counts)
        frecuencia_acumulada = [0] * len(counts)
        for i in range(len(bin_edges)-1):
            min_edges[i] = round(bin_edges[i], 4)
            max_edges[i] = round(bin_edges[i+1], 4)
            if i == 0:
                frecuencia_acumulada[i] = round(counts[i])
            else:
                frecuencia_acumulada[i] = frecuencia_acumulada[i-1] + round(counts[i])
        self.dist_table.setModel(PandasModel(pd.DataFrame({
            'Limite inferior': min_edges, 
            'Limite superior': max_edges, 
            'Frecuencia observada': counts,
            #'Frecuencia acumulada': frecuencia_acumulada
            })))


class UniformLeftPanel(LeftPanel):
    def _add_configuration(self, layout: QVBoxLayout):
        self.n_input = QLineEdit(self)
        self.n_input.setPlaceholderText('Tamaño de la muestra (n)')
        layout.addWidget(self.n_input)
        
        self.min = QLineEdit(self)
        self.min.setPlaceholderText('Mínimo valor de la muestra')
        layout.addWidget(self.min)
        
        self.max = QLineEdit(self)
        self.max.setPlaceholderText('Máximo valor de la muestra')
        layout.addWidget(self.max)
    
    def _check_inputs(self):
        if not super()._check_inputs():
            return False
        
        if not self.min.text().replace('.', '', 1).replace('-', '').isdigit() or not self.max.text().replace('.', '', 1).replace('-', '').isdigit():
            self.error_label.setText('Error: Los valores mínimo y máximo deben ser números.')
            return False
        
        min_val = float(self.min.text())
        max_val = float(self.max.text())
        
        if min_val >= max_val:
            self.error_label.setText('Error: El valor mínimo debe ser menor que el valor máximo.')
            return False
        
        self.error_label.setText('')
        return True
    
    def _get_data(self):  # type: ignore
        if not self._check_inputs():
            return []
            
        n = int(self.n_input.text())    
        min_val = float(self.min.text())
        max_val = float(self.max.text())

        return generate_random_variable_distribution(n, uniform_distribution_generator, ndigits=4, min=min_val, max=max_val)


class ExponentialLeftPanel(LeftPanel):     
    def _add_configuration(self, layout: QVBoxLayout):
        self.n_input = QLineEdit(self)
        self.n_input.setPlaceholderText('Tamaño de la muestra (n)')
        layout.addWidget(self.n_input)
        
        self.lamb = QLineEdit(self)
        self.lamb.setPlaceholderText('Lambda para la muestra')
        layout.addWidget(self.lamb)
        
    def _check_inputs(self):
        if not super()._check_inputs():
            return False
        
        if not self.lamb.text().replace('.', '', 1).replace('-', '').isdigit():
            self.error_label.setText('Error: Lambda debe ser un número.')
            return False
        
        lamb_val = float(self.lamb.text())
        
        if lamb_val <= 0:
            self.error_label.setText('Error: Lambda debe ser mayor que 0.')
            return False
        
        self.error_label.setText('')
        return True
    
    def _get_data(self):  # type: ignore
        if not self._check_inputs():
            return []
        
        n = int(self.n_input.text())
        lamb = float(self.lamb.text())
        return generate_random_variable_distribution(n, negative_exponential_distribution_generator, ndigits=4, lamb=lamb)


class NormalLeftPanel(LeftPanel):
    def _add_configuration(self, layout: QVBoxLayout):
        self.n_input = QLineEdit(self)
        self.n_input.setPlaceholderText('Tamaño de la muestra (n)')
        layout.addWidget(self.n_input)
        
        self.mu = QLineEdit(self)
        self.mu.setPlaceholderText('Media (μ)')
        layout.addWidget(self.mu)

        self.sigma = QLineEdit(self)
        self.sigma.setPlaceholderText('Desviación estándar (σ)')
        layout.addWidget(self.sigma)
        
    def _check_inputs(self):
        if not super()._check_inputs():
            return False
        
        if not self.mu.text().replace('.', '', 1).replace('-', '').isdigit() or not self.sigma.text().replace('.', '', 1).replace('-', '').isdigit():
            self.error_label.setText('Error: La media y la desviación estándar deben ser números.')
            return False
        
        sigma_val = float(self.sigma.text())
        
        if sigma_val <= 0:
            self.error_label.setText('Error: La desviación estándar debe ser mayor que 0.')
            return False
        
        self.error_label.setText('')
        return True
    
    def _get_data(self):  # type: ignore
        if not self._check_inputs():
            return []
        
        n = int(self.n_input.text())
        mu = float(self.mu.text())
        sigma = float(self.sigma.text())
        return generate_random_variable_distribution(n, normal_distribution_generator_box_muller, ndigits=4, mu=mu, sigma=sigma)

class Tab(QWidget):
    def __init__(self, left_panel, update_plot, parent=None):
        super().__init__(parent)

        self.left_panel = left_panel(self.update_plot_data)
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.left_panel)
        
        self.right_panel = RightPanel([], self.update_dist_table, left_panel=self.left_panel)
        
        layout.addWidget(self.right_panel)

        self.setLayout(layout)
        
    def update_plot_data(self, data):
        return self.right_panel.update_plot_data(data)
    
    def update_dist_table(self, counts, bin_edges):
        self.left_panel.update_dist_table(counts, bin_edges)
