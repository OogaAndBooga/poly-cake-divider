import pyqtgraph as pg
import numpy as np

class Plot_Widget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        p = self.plot(symbol = 'p')
        p.setData([1,2,3,4,5],[1,4,2,6,1])
        lr = pg.LinearRegionItem([0,1])

        scene = self.scene()
        scene.sigMouseClicked.connect(self.clicke)

        plotitem = self.getPlotItem()
        plotdataitem = p

        # plotitem.scene().connect(self.clicke)
        #emits signal only if plot is clicked
        # plotdataitem.sigClicked.connect(self.clicke)

        # what does this do?
        # lr.setZValue(-10)
        self.addItem(lr)
        self.p = p

    def clicke(self, event):
        print(event)
        print(event.pos())
        print(event.scenePos())
    #do not override this
    # def mousePressEvent(self, ev):
    #     self.clicke(ev)
