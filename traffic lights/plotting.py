# importing matplotlib module 
from matplotlib import pyplot as plt
  
# x-axis values
x = [0, 3, 6, 9, 12]
  
# Y-axis values
y = [0, 9.45, 12.89, 9.81, 11.27]
  
plt.xlim(1,15)
plt.ylim(1,15)
# Function to plot
plt.bar(x,y)
  
# function to show the plot
plt.show()