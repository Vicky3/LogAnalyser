# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:29:52 2015

Tools for creating svgs from data in dictionaries.

@author: adreyer
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import operator
import StringIO

def createBarChart(data,top=None):
    """
    Creates a bar chart.

    Parameters
    ----------
    data : dict
        keys are names of bars, values are heights of bars
    top : int, optional
        a maximum number of bars, if less than in data the smallest bars are
        melted together

    Returns
    -------
    StringIO
        svg image
    """
    #top too big?
    if top>=len(data.values()):
        top=None
    #top given
    if top:
        top-=1#number of bars from data
        #sort dictionary in lists to melt the smallest bars together
        sorted_x = sorted(data.items(), key=operator.itemgetter(1),
                          reverse=True)
        [a,b]=map(list, zip(*sorted_x))
        l=a[0:top]
        l.append('others')
        x=b[0:top]
        #sum up the values of melted bars
        x.append(sum(b[top:len(b)]))
    #no top given - use full data
    else:
        x=data.values()
        l=data.keys()

    #Convert values
    l=[s.decode('ISO-8859-1') for s in l]
    #build svg
    xpos=range(len(x))#pos of left bottom edge of bars
    xlpos=[n+0.4 for n in xpos]#pos of labels
    a=plot.subplot()
    a.bar(xpos, x)
    a.set_xticks(xlpos)
    a.set_xticklabels(l)
    a.set_ylabel("# of appearance")

    #write svg to StringIO
    f=StringIO.StringIO()
    plot.savefig(f, format="svg")
    return f

def createPieChart(data,top=None):
    """
    Creates a pie chart.

    Parameters
    ----------
    data : dict
        keys are names of wedges, values are size of bars
    top : int, optional
        a maximum number of wedges, if less than in data the smallest wedges
        are melted together

    Returns
    -------
    StringIO
        svg image
    """
    #top too big?
    if top>=len(data.values()):
        top=None
    #top given
    if top:
        top-=1#number of bars from data
        #sort dictionary in lists to melt the smallest wedges together
        sorted_x = sorted(data.items(), key=operator.itemgetter(1),
                          reverse=True)
        [a,b]=map(list, zip(*sorted_x))
        l=a[0:top]
        l.append('others')
        x=b[0:top]
        #sum up the values of melted wedges
        x.append(sum(b[top:len(b)]))
    #no top given - use full data
    else:
        x=data.values()
        l=data.keys()

    #Convert values
    l=[s.decode('ISO-8859-1') for s in l]
    #build svg
    plot.pie(x, explode=None, labels=l, colors=('b', 'g', 'r', 'c', 'm', 'y', 'w'), shadow=True,startangle=90,
             counterclock=False)

    #TODO patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
    #http://stackoverflow.com/questions/14279344/how-can-i-add-textures-to-my-bars-and-wedges

    plot.axis('equal')#make the pie round
    #write svg to StringIO
    f=StringIO.StringIO()
    plot.savefig(f, format="svg")
    return f
    #print f.getvalue()