# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:29:52 2015

Tools for creating svgs from data in dictionaries.

@author: adreyer
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
        topSorted = sorted_x[:top]
        topSorted.append(('other', sum(n for _, n in sorted_x[top:])))
    #no top given - use full data
    else:
        topSorted = data.items()

    #sort by keys (e.g. alphabetically)
    sorted_x = sorted(topSorted, key=operator.itemgetter(0),
                          reverse=False)
    l,x= map(list, zip(*sorted_x))

    #Convert values
    l=[s.decode('ISO-8859-1') for s in l]

    #build svg
    xpos=range(len(x))#pos of left bottom edge of bars
    xlpos=[n+0.4 for n in xpos]#pos of labels
    a=plt.subplot()
    a.bar(xpos, x)
    a.set_xticks(xlpos)
    a.set_xticklabels(l)
    a.set_ylabel("# of appearance")

    #write svg to StringIO
    f=StringIO.StringIO()
    plt.savefig(f, format="svg")
    plt.close()
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
    #sort dictionary in lists to melt the smallest wedges together
    sorted_x = sorted(data.items(), key=operator.itemgetter(1),
                      reverse=True)
    a,b= map(list, zip(*sorted_x))

    #top given
    if top:
        top-=1#number of bars from data
        l=a[0:top]
        l.append('others')
        x=b[0:top]
        #sum up the values of melted wedges
        x.append(sum(b[top:len(b)]))
    #no top given - use full data
    else:
        l=a
        x=b

    #Convert values
    l=[s.decode('ISO-8859-1') for s in l]

    #build svg
    wedges = plt.pie(x, explode=None, colors=('b','g','r','c','m','y','w'),
                     shadow=True, startangle=90, counterclock=False)[0]
    #differentiate between wedges
    if len(wedges)>7:
        hatch=["/","\\","x","o","O",".","*"]
        for i in range(7,len(wedges)):
            wedges[i].set_hatch(hatch[i-7])
        plt.draw()#needed for update

    #legend
    leg = plt.legend(l,loc='upper center', bbox_to_anchor=(0.5, 0.0))

    plt.axis('equal')#make the pie round

    #write svg to StringIO
    f=StringIO.StringIO()
    plt.savefig(f,format="svg",bbox_extra_artists=(leg,),bbox_inches='tight')
    plt.close()
    return f