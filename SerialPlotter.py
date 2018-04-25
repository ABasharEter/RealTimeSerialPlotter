from RealTimePlotter import RealTimePlotter
from SerialBuffer import SerialBuffer

if __name__ == '__main__':
    import sys
    sb = None
    if(len(sys.argv)<=1):
        sb = SerialBuffer('COM3',1024)
    else:
        sb = SerialBuffer('COM3',1024,sys.argv[1])
    p = RealTimePlotter()
    sb.callbacks.append(p.plot)
    sb.start()
    p.show()
    sb.loop()