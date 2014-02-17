OCRToolkit
==========

Tools for working with Optical Character Recognition output

### Installation

    pip install git+git://github.com/opensecrets/OCRToolkit.git


### Example


#### Sample PDF Document

![Sample document](http://assets.opensecrets.org/github/sample_doc.png "Sample PDF: Periodic Financial Disclosure from the US House of Representatives")


```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans
import os
from ocrtoolkit import parser
```

```python
# Get the OCRed characters in a certain area
# of a form.  Useful for running through and 
# seeing if a set of forms are fairly consistant.
boundingBox = {'l':900, 't':400, 'r':1050, 'b':1000}
parser.getCharacters('2000777.xml', boundingBox)
```

```python
# Run through a directory, pulling out data from xml 
# documents matching the regular expression: 
#   Some Characters, an X, Something that looks like a date.
# What ABBYY calls a "line" or continuous string of text, is 
# separated by a pipe for matching purposes.  

regex = r"([^\n\|]+)\|(x)\|(\d\d\/\d\d\/\d\d)"


directory = '.'
xLocs = []
allData = []

for fname in os.listdir(directory ):
    (locs, data) = parser.parseXML(fname, regex)

    # I want the locations of the X, which 
    # should appear in position 1 in the locations 
    # array.  Locations correspond to parentheses in
    # the expression. The X is in the second group.
    xLocs += [l[1] for l in locs]
    allData += [[fname] + d for d in data]

# Now I'm going to try to find where most Xes
# occur by finding the densest parts of the histogram.
centroids = kmeans(np.array(xLocs), 3)[0]

# Plot the histogram and the centroids.
plt.hist(xLocs, facecolor='g', bins=100)

for l in centroids:
    axvline(x=l, color='r', zorder=0)

plt.title('Locations of X marks')
plt.axis([600,850, 0, 600])
plt.grid(False)
plt.show()

# The plot shows I should probably consider Xes between about
# 680 pixels from the left and 720 pixels from the left 
# to be in the first column, then 720 to 760 in the center column
# and more than 760 in the right column.

# Set Xes to something more meaningful.
for i, loc in enumerate(xLocs):
    if loc > 680 and loc <= 720:
        allData[i][2] = 'Purchase'
    elif loc > 720 and loc <= 760:
        allData[i][2] = 'Sale'
    elif loc > 760 and loc <= 800:
        allData[i][2] = 'Exchange'

# Print out the data from our example doc.
print [x for x in allData if x[0] == '2000777.xml']
```


![Histogram of X marks](http://assets.opensecrets.org/github/x_mark_hist.png "Histogram of X marks")




