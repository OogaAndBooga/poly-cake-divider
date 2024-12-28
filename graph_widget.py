import pyqtgraph as pg
import numpy as np

class Plot_Widget(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        # p = self.plot(symbol = 'p','o')
        p1 = self.plot()
        p2 = self.plot()
        p3 = self.plot()

        self.plot1 = p1
        self.plot2 = p2
        self.plot3 = p3

        self.linear_region = pg.LinearRegionItem([0,1])

        scene = self.scene()
        scene.sigMouseClicked.connect(self.clicke)

        plotitem = self.getPlotItem()
        plotdataitem = p1

        self.line = pg.InfiniteLine(0)
        self.addItem(self.line)

        # plotitem.scene().connect(self.clicke)
        #emits signal only if plot is clicked
        # plotdataitem.sigClicked.connect(self.clicke)

        # what does this do?
        # lr.setZValue(-10)

        # self.addItem(self.linear_region)
    def set_btindex(self, btindex):
        # self.linear_region.setRegion([self.btindex, self.btindex])
        self.line.setValue(btindex)

    def clicke(self, event):
        print(event)
        print(event.pos())
        print(event.scenePos())

    #do not override this
    # def mousePressEvent(self, ev):
    #     self.clicke(ev)
