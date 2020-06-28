import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

x = np.array([0,400,1200,2100,2700,3000])
tc = np.array([1000,3000,5000,7000,9000,11000])



# 300 represents number of points to make between T.min and T.max
xnew = np.linspace(x.min(), x.max(), 300)

spl = make_interp_spline(x, tc, k=3)  # type: BSpline
tc_smooth = spl(xnew)

plt.figure()
# plt.plot(x,tc)
plt.plot(xnew,tc_smooth, label='TC')

plt.xlabel('Quantity')
plt.ylabel('Total Cost')
plt.legend()
plt.show()
