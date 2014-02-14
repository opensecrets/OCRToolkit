import re
from lxml import etree
import os

schema = '{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}'

PAGE = schema + 'page'
BLOCK = schema + 'block'
LINE = schema + 'line'
CHAR = schema + 'charParams'


def inside(bb, a):

    if bb['l'] < a['l'] and bb['t'] < a['t'] and bb['r'] > a['r'] and bb['b'] > a['b']:
        return True
    else:
        return False


def getCharacters(fname, bb):
    charsInside = ''

    f = open(fname, 'r')
    root = etree.XML(f.read())

    for p in root.iter(PAGE):
        for c in p.iter(CHAR):
            # Convert attributes to integers
            a = {k: int(v) for k, v in c.attrib.items()}

            if inside(bb, a):
                charsInside += c.text
        charsInside += '\n'
    return charsInside


def parseXML(fname, regex, minLineLen=200, lineSeparator='|'):
    regExC = re.compile(regex,  re.IGNORECASE)

    f = open(fname, 'r')
    root = etree.XML(f.read())
    matches = []
    lefts = []
    locs  = []
    line = ''

    for p in root.iter(PAGE):
        for b in p.iter(BLOCK):

            lastLeft = -1
            for l in b.iter(LINE):
                for c in l.iter(CHAR):
                    left = int(c.attrib['l'])

                    if left + minLineLen < lastLeft:
                        match = regExC.match(line)
                        if match is not None:
                            matches.append(list(match.groups()))
                            # Array of leftmost locations for each match
                            leftMosts = [lefts[match.start(i+1)] for i, m in enumerate(match.groups())]
                            locs.append(leftMosts)

                        lefts = []
                        line = ''

                    lastLeft = left

                    lefts.append(left)
                    line += c.text

                lefts.append(-1)
                line += lineSeparator

    return (locs, matches)


