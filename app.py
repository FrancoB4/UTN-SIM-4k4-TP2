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
        self.resize(1200, 900)

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)
        
        btn = QPushButton("Uniforme")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(UniformLeftPanel, None))

        btn = QPushButton("Exponencial")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(ExponentialLeftPanel, None))

        btn = QPushButton("Normal")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Tab(NormalLeftPanel, None))

        self.setLayout(pagelayout)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
