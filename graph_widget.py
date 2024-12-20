import pyqtgraph as pg
import numpy as np

class Plot_Widget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.p = self.plot()
        self.p.setData([1,2,3,4,5],[1,4,2,6,1])
