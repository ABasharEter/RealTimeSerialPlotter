# Serial Port Real-Time plotter and visualizer

A small library that will help you plot and visualize numeric data from serial port.
This can be vary helpful when you want to analyze analog data form your Arduino or Respray Pi.
Also you can save your data to a bzip compressed file and then load it and plot it later or do what ever you want to do with it.

## Installation:
Currently this project is under construction so just download the source files put them in your project.

## Usage:
1. Simplest way to plot data from serial port: 
```python
from RealTimePlotter import RealTimePlotter
from SerialBuffer import SerialBuffer
sb = SerialBuffer('COM3',1024)
p = RealTimePlotter()
sb.callbacks.append(p.plot)
sb.start()
p.show()
sb.loop()
```
2. To stop the running widget just close the window and hit Ctr-C on your terminal.
3.  If you want to save your data to a file (ex. my_data.bz2) send the SerialBuffer object your file name:
```python
from RealTimePlotter import RealTimePlotter
from SerialBuffer import SerialBuffer
sb = SerialBuffer('COM3',1024,'my_data.bz2')
p = RealTimePlotter()
sb.callbacks.append(p.plot)
sb.start()
p.show()
sb.loop()
```
4. To view your saved file:
```python
from HistoryPlotter import HistoryPlotter
h = HistoryPlotter('my_data.bz2')
h.loop()
```
## License
The MIT License (MIT)

Copyright (c) 2018 Ahmad Bashar Eter

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

