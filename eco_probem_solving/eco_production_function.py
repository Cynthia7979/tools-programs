import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

x = np.array([0,1,2,3,4,5,6,7])
tpy = np.array([0,500,1200,2100,2800,3000,3000,2800])
apy = np.array([0,500,600,700,700,600,500,400])
mpy = np.array([0,500,700,900,700,200,0,-200])



# 300 represents number of points to make between T.min and T.max
xnew = np.linspace(x.min(), x.max()+2, 300)

spl = make_interp_spline(x, tpy, k=3)  # type: BSpline
tpy_smooth = spl(xnew)
spl = make_interp_spline(x, apy, k=3)  # type: BSpline
apy_smooth = spl(xnew)
spl = make_interp_spline(x, mpy, k=3)  # type: BSpline
mpy_smooth = spl(xnew)

plt.figure()
plt.plot(x,tpy, 'r')
plt.plot(x,apy, 'g')
plt.plot(x,mpy, 'b')
plt.plot(xnew,tpy_smooth, 'r--', label='TP')
plt.plot(xnew,apy_smooth, 'g--', label='AP')
plt.plot(xnew,mpy_smooth, 'b--', label='MP')

plt.xlabel('Labor')
plt.ylabel('Output')
plt.legend()
plt.show()
