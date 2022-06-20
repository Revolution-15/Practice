# importing matplotlib module 
from matplotlib import pyplot as plt
  
# x-axis values
x = [0, 3, 6, 9, 12]
  
# Y-axis values
y = [0, 4.64, 1.57, 1.91, 1.13]
  
plt.xlim(1,15)
plt.ylim(1,15)
# Function to plot
plt.bar(x,y)
  
# function to show the plot
plt.show()