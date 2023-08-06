import matplotlib.pyplot as plt
import json
import time
from dispositor import space as spaceClass

path = 'data1.json'
segment_count = len(spaceClass.septenerSegmentData())
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
langs = list(range(segment_count))
f = open(path, "r")
data = json.loads(f.read())
f.close()
ax.bar(langs, data)
plt.show()



