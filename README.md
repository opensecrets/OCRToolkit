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




### Well-Known Text Conversion

Parse as normal, returning all coordinates.  This will return a bounding box for the each line with a match.  (Regex ```.*``` will return the whole document.)

```python
(locs, data) = parser.parseXML('someXML.xom', regex, allCoords=True)
pprint([parser.toWellKnownText(x) for x in locs])
```

Output [WKT](http://en.wikipedia.org/wiki/Well-known_text):
```
['POLYGON ((106 78, 106 1518, 156 1518, 156 78))',
 'POLYGON ((215 1611, 215 1979, 241 1979, 241 1611))',
 'POLYGON ((270 1630, 270 2062, 312 2062, 312 1630))',
 'POLYGON ((249 77, 249 1215, 308 1215, 308 77))',
 'POLYGON ((391 122, 391 173, 411 173, 411 122))',
 'POLYGON ((412 230, 412 1066, 443 1066, 443 230))',
 'POLYGON ((435 1568, 435 2029, 465 2029, 465 1568))',
 'POLYGON ((470 1568, 470 1731, 496 1731, 496 1568))',
 .
 .
 .
 
```



