import serial
import numpy as np
from matplotlib import pyplot as plt
import time
from threading import Thread,Event,Lock


class RealTimePlotter:
    def __init__(self):
        plt.ion()
        self.fig, (self.time_axis,self.freq_axis) = plt.subplots(2)
        self.fig.suptitle('live updated data', fontsize='14', fontweight='bold')
        self.time_axis.set_title('time data', fontsize='14', fontweight='bold')
        self.time_axis.set_xlabel('time, seconds', fontsize='11', fontstyle='italic')
        self.time_axis.set_ylabel('amplitude, V', fontsize='11', fontstyle='italic')
        self.freq_axis.set_title('frequency data', fontsize='14', fontweight='bold')
        self.freq_axis.set_xlabel('frequency, Hz', fontsize='11', fontstyle='italic')
        self.freq_axis.set_ylabel('amplitude, log', fontsize='11', fontstyle='italic')
        self.fig.subplots_adjust(hspace=0.5)
    def show(self):
        try:
            x = [0]
            self.time_line, = self.time_axis.plot(x, x)
            self.freq_line, = self.freq_axis.plot(x, x)
            self.fig.canvas.draw()
            self.fig.show()
            plt.show(block=False)
        except KeyboardInterrupt:
            self.fig.close('all')

    def plot(self,buffer,stats):
        try:
            buffer = buffer/1024*5-2.5+0.7/2
            fft = np.log(np.abs(np.fft.rfft(buffer))+1e-8)
            t = np.linspace(0,stats['elapsed_time'],buffer.shape[0])
            f = np.linspace(0,stats['fs'],fft.shape[0])
            #self.time_axis.clear()
            #self.freq_axis.clear()
            self.time_line.set_xdata(t)
            self.time_line.set_ydata(buffer)
            
            self.freq_line.set_xdata(f)
            self.freq_line.set_ydata(fft)

            self.time_axis.relim() 
            self.time_axis.autoscale_view(True,True,True) 
            self.freq_axis.relim() 
            self.freq_axis.autoscale_view(True,True,True) 
            #self.time_axis.plot(t,buffer)
            #self.freq_axis.plot(f,fft)
            self.fig.canvas.draw()
            plt.pause(0.001)
        except Exception as e:
            print(e)