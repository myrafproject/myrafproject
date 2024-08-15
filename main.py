from myraflib import Fits

f = Fits.sample()

f.div(3.1415, output="asd", override=True)
Fits.high_precision = True
f.div(3.1415, output="asd_h", override=True)
