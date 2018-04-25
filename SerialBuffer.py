import serial
import numpy as np
from matplotlib import pyplot as plt
import time
from threading import Thread,Event,Lock
import io
import bz2
import pickle

class SerialBuffer:
    @staticmethod
    def worker(buffer):
        buffer.stats[buffer.write_buffer_index]['start_time'] = time.perf_counter()
        while(buffer.started):
            try:
                x = buffer.formater(buffer.serial_port.readline().decode())
                buffer.buffers[buffer.write_buffer_index][buffer.write_buffer_pos] = x
                buffer.write_buffer_pos+=1
            except Exception as e:
                print(e)
                pass
            if buffer.write_buffer_pos == buffer.buffers[buffer.write_buffer_index].shape[0]:
                buffer.stats[buffer.write_buffer_index]['elapsed_time'] = (time.perf_counter() 
                                                                - buffer.stats[buffer.write_buffer_index]['start_time'])
                buffer.stats[buffer.write_buffer_index]['fs'] = (buffer.buffers[buffer.write_buffer_index].shape[0]
                                                        /buffer.stats[buffer.write_buffer_index]['elapsed_time'])
                buffer.write_buffer_pos = 0

                with buffer.lock:
                    buffer.last_ready_buffer_index = buffer.write_buffer_index
                    buffer.onReady.set()
                    
                buffer.write_buffer_index = (buffer.write_buffer_index+1)%(len(buffer.buffers))
                buffer.stats[buffer.write_buffer_index]['start_time'] = time.perf_counter()
    
    def __init__(self,port_name,buffer_size,filename=None,port_baudrate=115200,buffers_count=2):
        self.buffers = [np.zeros((buffer_size)) for i in range(buffers_count)]
        self.last_ready_buffer_index = -1
        self.stats = [{} for i in range(buffers_count)]
        self.serial_port = serial.Serial()
        self.serial_port.port = port_name
        self.serial_port.baudrate = port_baudrate
        self.lock = Lock()
        self.onReady = Event()
        self.thread = None
        self.started = False
        self.callbacks = []
        self.save_filename = filename
        self.formater = self.default_formater
        self.all_data = []
        self.write_buffer_index = 0
        self.write_buffer_pos = 0
        
    def default_formater(self,data):
        return np.float(data.strip())

    def start(self):
        if(self.thread is not None):
            raise Exception('The buffering thread already started!')
        self.thread = Thread(target = SerialBuffer.worker, args = [self])
        self.thread.daemon = True
        self.serial_port.open()
        if(self.save_filename is not None):
            self.all_data = []
            def save_callback(buffer,stats):
                self.all_data.append({'buffer':buffer,'stats':stats})
            self.callbacks.append(save_callback)

        self.started = True
        self.thread.start()

    def stop(self):
        if(self.thread is None):
            raise Exception('The buffering thread already stopped!')
        self.started = False
        self.serial_port.close()
        self.thread.join()
        if(self.save_filename is not None):
            with bz2.BZ2File(self.save_filename,'w') as f:
                pickle.dump(self.all_data,f)
        self.thread = None

    def loop(self):
        try:
            while self.thread is not None and self.thread.isAlive:
                while(not self.onReady.is_set()):
                    plt.pause(0.1)
                    #self.onReady.wait(10)
                buffer_idx = 0
                with self.lock:
                    buffer_idx = self.last_ready_buffer_index
                    self.onReady.clear()
                for calback in self.callbacks:
                    calback(self.buffers[buffer_idx],self.stats[buffer_idx])
        except KeyboardInterrupt:
            print("Stopping...")
            self.stop()


        


    