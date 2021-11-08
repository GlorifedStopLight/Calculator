import matplotlib.pyplot as plt


plt.plot([0, 10], [0, 10])
plt.xlabel("X Label")
plt.ylabel("Y Label")

ax = plt.gca()

ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])

plt.grid(True)
plt.show()