import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QPushButton
)

# Matplotlib embebido en Qt
from components import RightPanel, UniformLeftPanel, NormalLeftPanel, ExponentialLeftPanel, Tab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TP2 - Generación de variables aleatorias")
        self.resize(800, 600)

        # Datos de ejemplo
        self.df = pd.DataFrame({
            "X": np.arange(0, 10),
            "Y1": np.random.randint(0, 50, 10),
            "Y2": np.random.randint(50, 100, 10),
        })

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)
        
        btn = QPushButton("Uniforme")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(UniformLeftPanel, RightPanel([])))

        btn = QPushButton("Exponencial")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(ExponentialLeftPanel, RightPanel([])))

        btn = QPushButton("Normal")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(NormalLeftPanel, RightPanel([])))

        self.setLayout(pagelayout)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)
    
    def update_plot(self, col):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.df["X"], self.df[col], marker="o")
        ax.set_title(f"Columna seleccionada: {col}")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
