import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,Slider
from RealTimePlotter import RealTimePlotter
import io
import bz2
import pickle

class HistoryPlotter:
    def __init__(self,saved_filename):
        self.plotter = RealTimePlotter()
        self.plotter.fig.suptitle('History data', fontsize='14', fontweight='bold')
        self.plotter.fig.subplots_adjust(bottom=0.23,hspace=0.5)
        self.index = 0
        self.saved_filename = saved_filename
        self.data = []
        self.prev_axis = plt.axes([0.395, 0.03, 0.1, 0.06])
        self.next_axis = plt.axes([0.505, 0.03, 0.1, 0.06])
        self.btn_next = Button(self.next_axis, 'Next')
        self.btn_next.on_clicked(self.next)
        self.btn_prev = Button(self.prev_axis, 'Previous')
        self.btn_prev.on_clicked(self.prev)
        self.slider_axis = plt.axes([0.25, 0.11, 0.5, 0.03])
        self.read_data()
        self.slider = Slider(self.slider_axis, 'chunk',0,len(self.data)-1, valinit=0,valfmt='%10.0f')
        self.slider.on_changed(self.update)

    def read_data(self):
        with bz2.BZ2File(self.saved_filename,'r') as f:
            self.data = pickle.load(f)
            print('Number of chunks',len(self.data) )
        

    def loop(self):
        try:
            self.plotter.show()
            self.plotter.plot(self.data[self.index]['buffer'],self.data[self.index]['stats'])
            plt.show(block=True)
        except KeyboardInterrupt:
            print("Stopping...")

    def update(self,val):
        self.index=int(val)
        self.plotter.plot(self.data[self.index]['buffer'],self.data[self.index]['stats'])

    def next(self,event):
        if(self.index < len(self.data)-1):
            self.index +=1
            self.plotter.plot(self.data[self.index]['buffer'],self.data[self.index]['stats'])
            self.slider.set_val(self.index)

    def prev(self,event):
        if(self.index >0):
            self.index -=1
            self.plotter.plot(self.data[self.index]['buffer'],self.data[self.index]['stats'])
            self.slider.set_val(self.index)

if __name__ == '__main__':
    import sys
    if(len(sys.argv)<=1):
        print("Usage: python HistoryPlotter [HistoryFileName.bz2]")
    else:
        h = HistoryPlotter(sys.argv[1])
        h.loop()
