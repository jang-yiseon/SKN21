import matplotlib.pyplot as plt
import numpy as np

plt.style.use("dark_background")

fig = plt.figure(figsize=(15,7), facecolor='gray') #facecolor: figure의 배경색
axes1 = fig.add_subplot(1,2,1)
axes2 = fig.add_subplot(1,2,2)

axes1.plot([1,2,3,4,5], [10,20,30,40,50], label='line1')
axes1.plot([1,2,3,4,5], [50,40,30,20,10], label='line2')
axes2.scatter(np.random.randint(100, size=50), np.random.randint(100, 200, size=50), color='r')

fig.suptitle('Example of Plot', size=25, color='blue') #size: 폰트크기, color: 글자색
axes1.set_title("PLOT 1", size=20)
axes2.set_title("Plot 2", size=20)

axes1.set_xlabel("X축", size=15)
axes1.set_ylabel("Y축", size=15)
axes2.set_xlabel("가격1", size=15)
axes2.set_ylabel('가격2', size=15)

axes1.legend()
axes1.grid(True)
plt.show()