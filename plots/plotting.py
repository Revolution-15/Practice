# importing matplotlib module 
from matplotlib import pyplot as plt
import numpy as np
  
# x-axis values
x = [0, 3, 6, 9, 12]
  
# Y-axis values
y = [0, 12.02, 11.68, 11.50, 10.41]
z = [0, 1.581, 0.65, 0.573, 0.465]
  
X_axis = np.arange(0,15,3)
# Function to plot

ax = plt.axes()
ax.set_facecolor("#eafff5")
ax.set_xlabel('spawning time of vehicles (sec)', color='c')
ax.set_ylabel('Delay (sec)', color='c')

font2 = {'family':'serif','color':'darkred','size':15}
plt.title("Average waiting time", fontdict = font2)
plt.bar(X_axis-0.2, y, 0.4, label = 'Traffic Lights')
plt.bar(X_axis+0.2, z, 0.4, label = 'Ours')
plt.xticks(list(range(0,13)))
plt.yticks(list(range(0,13)))
# function to show the plot
plt.legend(loc='upper left')
plt.show()