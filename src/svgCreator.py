# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:29:52 2015

@author: adreyer
"""

import matplotlib.pyplot
import operator

def createBarChart(data,top=None):
    pass

def createPieChart(data,top=None):
    print data.keys()
    print data.values()
    if top:
        l=data.keys()
        x=data.values()
#        x.sort(reverse=True)
#        x[0:top]
#        print x,"_",x[0:top]
#        a=[45,32,12]
#        a.sort()
#        print a
        sorted_x = sorted(data.items(), key=operator.itemgetter(1),reverse=True)
        print sorted_x
        [a,b]=map(list, zip(*sorted_x))
        print a
        print b
        print "HERE"
        l=a[0:top]
        l.append('others')
        x=b[0:top]
        print l
        x.append(sum(b[top:len(b)]))
        print x
        print l
    else:
        x=data.values()
        l=data.keys()
    matplotlib.pyplot.pie(x, explode=None, labels=l,
    #colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),
        autopct='%1.1f%%', pctdistance=0.6, shadow=False,
        labeldistance=1.1, startangle=None, radius=None,
        counterclock=True, wedgeprops=None, textprops=None)
    matplotlib.pyplot.show()