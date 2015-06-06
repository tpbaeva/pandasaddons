import os
import uuid
from types import MethodType

import numpy as np
import pandas as pd

from bokeh.resources import CDN
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import autoload_static
from bokeh.models import HoverTool


COLORS = ["#1f77b4", "#ff7f0e", "#ffbb78", "#2ca02c", "#98df8a", "#d62728", 
          "#ff9896", "#9467bd", "#c5b0d5", "#8c564b", "#c49c94", "#e377c2", 
          "#f7b6d2", "#7f7f7f", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"]
          
TOOLS = ['pan', 'wheel_zoom', 'box_zoom', 'resize', 'reset', 'previewsave', 'box_select', 'hover']


def plot_df(df, 
            tools=TOOLS, 
            title='', 
            x_axis_type='datetime', 
            line_width=2, 
            background_fill= '#eeeff0',
            alpha=0.7,
            style='o-',
            plot_width=600,
            plot_height=400,
            xlabel='',
            ylabel=''):
    """Creates a bokeh plot of dataframe, one line per column"""    
    
    plot = figure(x_axis_type=x_axis_type, 
                  tools=','.join(tools), 
                  title=title,
                  background_fill=background_fill,
                  plot_width=plot_width,
                  plot_height=plot_height)
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel
    
    info = df.index
    if isinstance(df.index, pd.tseries.index.DatetimeIndex):
        info = [d.strftime('%d/%m/%Y %H:%M:%S') for d in info]
        
    for idx, ts in enumerate(df):
        source = ColumnDataSource(
            data=dict(x=df.index,
                      y=df[ts].values,
                      info=info,
                     )
        )
        
        color = COLORS[idx%len(COLORS)]
        plot.line(df.index, df[ts].values, 
                  line_color=color, 
                  line_width=line_width, 
                  alpha=alpha, 
                  legend=ts,
                  source=source)
        if style == 'o-':
            plot.circle(df.index, df[ts].values, color=color, fill_color=None, size=10, legend=ts, source=source)
        
        if 'hover' in tools:
            hover = plot.select(dict(type=HoverTool))
            hover.tooltips = [(xlabel, "@info"),
                              (ylabel, "$y"),
                             ]    
    return plot


def setcol(x):
    """Sets color for a given value"""
    
    if np.isnan(x):
        return '#e2e2e2'
    elif x<0:
        return '#cc7878'
    else:
        return '#a5bab7'


def heatmap_df(df, 
            tools=TOOLS, 
            title='', 
            alpha=0.7,
            plot_width=900,
            plot_height=400,
            xlabel='',
            ylabel='',
            x_axis_location='above'):
    """Creates a bokeh plot of dataframe as a heatmap"""
    
    # pre-condition as columns and index need to be list of string
    x = list(map(str, df.index))
    y = list(df.columns)    
    
    # set color for every cell
    ys = []
    xs = []
    for xi in x:
        for yi in y:
            ys.append(yi)
            xs.append(xi)
    value = df.values.ravel()
    color = [setcol(v) for v in value]
    
    source = ColumnDataSource(
        data=dict(x=xs,
                  y=ys,
                  color=color,
                  value=value,
                  )
    )
    
    plot = figure(title=title, 
                  tools=tools,
                  x_range=x, 
                  y_range=list(reversed(y)),
                  plot_width=plot_width, 
                  plot_height=plot_height, 
                  x_axis_location=x_axis_location)
           
    plot.rect('x', 'y', 0.95, 0.95, source=source, color='color', line_color=None)
    
    plot.grid.grid_line_color = None
    plot.axis.axis_line_color = None
    plot.axis.major_tick_line_color = None
    plot.axis.major_label_standoff = 0
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel

    if 'hover' in tools:
        hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [(xlabel, "$x"),
                          (ylabel, "$y"),
                          ('value', '@value'),
                         ]    
    return plot  
    
     
def iplot(self, 
          plottype='linear',
          jspath=None,
          title='',
          browser='chrome',
          tools=TOOLS,
          x_axis_type='datetime',
          line_width=2,
          background_fill= '#eeeff0',
          alpha=0.7,
          plot_width=900,
          plot_height=400,
          xlabel='',
          ylabel='',
          style='o-'):
    """Writes javascript in given location, embeds it in a html saved in same location, and opens it in a browser
    
    Example
    -------
    >>> import pandas as pd
    >>> import pandasaddons
    >>> rdf = pd.RandomDataFrame(index_type='datetime')
    >>> rdf.iplot()
    >>> rdf = pd.RandomDataFrame(index_type='linear')-0.5
    >>> rdf.iplot(plottype='heatmap', xlabel='x', ylabel='y')
    
    """
    
    if plottype.lower() == 'heatmap':
        plot = heatmap_df(self, 
                          tools=tools, 
                          title=title, 
                          alpha=alpha,
                          plot_width=plot_width,
                          plot_height=plot_height,
                          xlabel=xlabel,
                          ylabel=ylabel,
                          x_axis_location='above')
    else:
        plot = plot_df(self, 
                       tools=tools, 
                       title=title, 
                       x_axis_type=x_axis_type, 
                       line_width=line_width, 
                       background_fill=background_fill,
                       alpha=alpha,
                       style=style,
                       plot_width=plot_width,
                       plot_height=plot_height,
                       xlabel=xlabel,
                       ylabel=ylabel)
    
    filename = str(uuid.uuid4())
    this_jspath = jspath if jspath else os.environ['TMP']
    jsfilename = os.path.join(this_jspath, filename+'.js')
    htmlfilename = os.path.join(this_jspath, filename+'.html' )
    js, tag = autoload_static(plot, CDN, script_path=jsfilename)
    
    with open(jsfilename, 'w') as f:
        f.write(js)
        
    html = '<html><div>'+tag+'</div></html>'
    with open(htmlfilename, 'w') as f:
        f.write(html)
    os.system('start {browser}.exe "{htmlfilename}"'.format(**locals()))
    
pd.DataFrame.iplot = MethodType(iplot, None, pd.DataFrame)