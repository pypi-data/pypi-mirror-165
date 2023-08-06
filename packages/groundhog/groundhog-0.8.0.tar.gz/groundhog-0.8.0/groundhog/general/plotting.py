#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Native Python packages
import datetime
import warnings
import traceback

# 3rd party packages
from jinja2 import Environment, BaseLoader
import plotly.graph_objs as go
from plotly.offline import plot, iplot
from plotly.colors import DEFAULT_PLOTLY_COLORS
from plotly import subplots
import numpy as np
import matplotlib.pyplot as plt

# Project imports

GROUNDHOG_PLOTTING_CONFIG = {
    'showLink': True,
    'plotlyServerURL': "https://github.com/snakesonabrain/groundhog",
    'linkText': 'Created by groundhog using Plotly!'
}

PLOTLY_GLOBAL_FONT = dict(family='Century Gothic', size=12, color='#5f5f5f')
C0 = '#1f77b4'; C1 = '#ff7f0e'; C2 = '#2ca02c'; C3 = '#d62728'; C4 = '#9467bd'; C5 = '#8c564b'; C6 = '#e377c2'; C7 = '#7f7f7f'; C8 = '#bcbd22'; C9 = '#17becf'
PLOTLY_COLORS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9]

PORTRAIT_TEMPLATE = """
<HTML>
    <head>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            @page { margin: 0 }
            body { margin: 0 }
            .sheet {
              margin: 0;
              overflow: hidden;
              position: relative;
              box-sizing: border-box;
              page-break-after: always;
            }

            body.A3           .sheet { width: 297mm; height: 419mm }
            body.A3.landscape .sheet { width: 420mm; height: 296mm }
            body.A4           .sheet { width: 210mm; height: 296mm }
            body.A4.landscape .sheet { width: 297mm; height: 209mm }
            body.A5           .sheet { width: 148mm; height: 209mm }
            body.A5.landscape .sheet { width: 210mm; height: 147mm }

            .sheet.padding-5mm { padding: 5mm}
            .sheet.padding-10mm { padding: 10mm }
            .sheet.padding-15mm { padding: 15mm }
            .sheet.padding-20mm { padding: 20mm }
            .sheet.padding-25mm { padding: 25mm }

            @media screen {
              body { background: #e0e0e0 }
              .sheet {
                background: white;
                box-shadow: 0 .5mm 2mm rgba(0,0,0,.3);
                margin: 5mm;
              }
            }
            @media print {
                       body.A3.landscape { width: 420mm }
              body.A3, body.A4.landscape { width: 297mm }
              body.A4, body.A5.landscape { width: 210mm }
              body.A5                    { width: 148mm }
            }
            table {
                border-spacing: 0;
                border-collapse: collapse;
                width: 100%;
            }
            table td{
                overflow: hidden;
                word-wrap: break-word;
                text-align: center;
            }
            table, th, td {
                border: 3px solid black;
            }
            th, td {
                border: 1px solid black;
                font-family: 'Century Gothic';
                font-size: 10px;
                padding: 3px;
            }
        </style>
    </head>
    <body class="A4 portrait">
        {% for fig in figures %}
        <section class="sheet" style="padding: 5mm;">
            <table class="table">
                <tbody>
                    <tr style="height: 920px">
                        <td colspan=4><div style="align-items: center">{{ fig.path }}</div></td>
                    </tr>
                    <tr>
                        <td style="width: 100px; border-bottom: 0px; padding: 3px">Drawn by</td>
                        <td style="width: 550px; padding: 3px; border-bottom: 0px; font-size: 14px; text-align: left; padding-left: 10px; padding-top: 10px" rowspan=2>
                            {{ fig.title }}<!-- Max chars = 90 --></td>
                        <td colspan=2 style="border-bottom: 0px; padding: 3px">Report no</td>
                    </tr>
                    <tr>
                        <td style="padding: 3px">{{ fig.drawnby }}</td>
                        <td style="padding: 3px" colspan=2>{{ fig.report }}<!-- Max chars = 15 --></td>
                    </tr>
                    <tr>
                        <td style="border-bottom: 0px; padding: 3px">Checked by</td>
                        <td style="width: 550px; padding: 3px; text-align: left; padding-left: 10px" rowspan=4>
                            {% if fig.subtitle1 %}
                                {{ fig.subtitle1 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle2 %}
                                <br>{{ fig.subtitle2 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle3 %}
                                <br>{{ fig.subtitle3 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle4 %}
                                <br>{{ fig.subtitle4 }}
                            {% endif %}
                        </td><!-- Max chars = 120 -->
                        <td style="border-bottom: 0px; padding: 3px">Figure No</td>
                        <td style="border-bottom: 0px; padding: 3px">Rev</td>
                    </tr>
                    <tr>
                        <td style="padding: 3px">{{ fig.checkedby }}</td>
                        <td style="padding: 3px">{{ fig.figno }}<!-- Max chars = 12 --></td>
                        <td style="padding: 3px">{{ fig.rev }}<!-- Max chars = 2 --></td>
                    </tr>
                    <tr>
                        <td rowspan=3><img src="https://en.wikipedia.org/wiki/Ghent_University#/media/File:Ghent_University_logo.svg" width="80px"></td>
                        <td colspan=2 style="border-bottom: 0px; padding: 3px">Date</td>
                    </tr>
                    <tr>
                        <td colspan=2 style="padding: 3px">{{ fig.date }}</td>
                    </tr>
                    <tr>
                        <td colspan=3 style="font-size: 15px">{{ fig.projecttitle }}</td><!-- Max chars = 95-->
                    </tr>

                </tbody>
            </table>
        </section>
        {% endfor %}

    </body>
</HTML>

"""

LANDSCAPE_TEMPLATE = """
<HTML>
    <head>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            @page { margin: 0 }
            body { margin: 0 }
            .sheet {
              margin: 0;
              overflow: hidden;
              position: relative;
              box-sizing: border-box;
              page-break-after: always;
            }

            body.A3           .sheet { width: 297mm; height: 419mm }
            body.A3.landscape .sheet { width: 420mm; height: 296mm }
            body.A4           .sheet { width: 210mm; height: 296mm }
            body.A4.landscape .sheet { width: 297mm; height: 209mm }
            body.A5           .sheet { width: 148mm; height: 209mm }
            body.A5.landscape .sheet { width: 210mm; height: 147mm }

            .sheet.padding-5mm { padding: 5mm}
            .sheet.padding-10mm { padding: 10mm }
            .sheet.padding-15mm { padding: 15mm }
            .sheet.padding-20mm { padding: 20mm }
            .sheet.padding-25mm { padding: 25mm }

            @media screen {
              body { background: #e0e0e0 }
              .sheet {
                background: white;
                box-shadow: 0 .5mm 2mm rgba(0,0,0,.3);
                margin: 5mm;
              }
            }
            @media print {
                       body.A3.landscape { width: 420mm }
              body.A3, body.A4.landscape { width: 297mm }
              body.A4, body.A5.landscape { width: 210mm }
              body.A5                    { width: 148mm }
            }
            table {
                border-spacing: 0;
                border-collapse: collapse;
                width: 100%;
            }
            table td{
                overflow: hidden;
                word-wrap: break-word;
                text-align: center;
            }
            table, th, td {
                border: 3px solid black;
            }
            th, td {
                border: 1px solid black;
                font-family: 'Century Gothic';
                font-size: 10px;
                padding: 3px;
            }
        </style>
    </head>
    <body class="A4 landscape">
        {% for fig in figures %}
        <section class="sheet" style="padding: 5mm;">
            <table class="table">
                <tbody>
                    <tr style="height: 500px">
                        <td colspan=4><div style="align-items: center">{{ fig.path }}</div></td>
                    </tr>
                    <tr>
                        <td style="width: 100px; border-bottom: 0px; padding: 3px">Drawn by</td>
                        <td style="width: 875px; padding: 3px; border-bottom: 0px; font-size: 14px; text-align: left; padding-left: 10px; padding-top: 10px" rowspan=2>
                            {{ fig.title }}<!-- Max chars = 90 --></td>
                        <td colspan=2 style="border-bottom: 0px; padding: 3px">Report no</td>
                    </tr>
                    <tr>
                        <td style="padding: 3px">{{ fig.drawnby }}</td>
                        <td style="padding: 3px" colspan=2>{{ fig.report }}<!-- Max chars = 15 --></td>
                    </tr>
                    <tr>
                        <td style="border-bottom: 0px; padding: 3px">Checked by</td>
                        <td style="width: 875px; padding: 3px; text-align: left; padding-left: 10px" rowspan=4>
                            {% if fig.subtitle1 %}
                                {{ fig.subtitle1 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle2 %}
                                <br>{{ fig.subtitle2 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle3 %}
                                <br>{{ fig.subtitle3 }}<!-- Max chars = 120 -->
                            {% endif %}
                            {% if fig.subtitle4 %}
                                <br>{{ fig.subtitle4 }}
                            {% endif %}
                        </td><!-- Max chars = 120 -->
                        <td style="border-bottom: 0px; padding: 3px">Figure No</td>
                        <td style="border-bottom: 0px; padding: 3px">Rev</td>
                    </tr>
                    <tr>
                        <td style="padding: 3px">{{ fig.checkedby }}</td>
                        <td style="padding: 3px">{{ fig.figno }}<!-- Max chars = 12 --></td>
                        <td style="padding: 3px">{{ fig.rev }}<!-- Max chars = 2 --></td>
                    </tr>
                    <tr>
                        <td rowspan=3><img src="https://en.wikipedia.org/wiki/Ghent_University#/media/File:Ghent_University_logo.svg" width="80px"></td>
                        <td colspan=2 style="border-bottom: 0px; padding: 3px">Date</td>
                    </tr>
                    <tr>
                        <td colspan=2 style="padding: 3px">{{ fig.date }}</td>
                    </tr>
                    <tr>
                        <td colspan=3 style="font-size: 15px">{{ fig.projecttitle }}</td><!-- Max chars = 95-->
                    </tr>

                </tbody>
            </table>
        </section>
        {% endfor %}

    </body>
</HTML>
"""

def generate_html(outpath, figures, titles, drawnby, report,
                           fignos, rev, projecttitle,
                           subtitle1s, subtitle2s=None, subtitle3s=None, subtitle4s=None, checkedby=None,
                           figure_date=datetime.date.today().strftime("%d/%m/%Y"),
                           filename='figures',
                           portraitformat=True,
                           print_message=True):
    """
    Returns HTML for a series of Plotly portrait figures.
    The figures are first coerced to the correct format (portrait: H=870 x W=702, landscape: H=600 x W=1050). Standardized font and colors are also set.

    :param outpath: Path where the output is written. Use absolute paths.
    :param figures: List of Plotly figures
    :param titles: List of titles for the figures (maximum 90 characters)
    :param drawnby: Initials of drawer (maximum 3 characters)
    :param report: Report number (maximum 15 characters)
    :param fignos: List with figure numbers (maximum 12 characters)
    :param rev: Revision of the figures (maximum 2 characters)
    :param date: Date of drawing in %d/%m/%Y format
    :param projecttitle: Title of the project (maximum 95 characters)
    :param subtitle1s: List with first subtitles (maximum 120 characters)
    :param subtitle2s: List with second subtitles (maximum 120 characters) - default is None
    :param subtitle3s: List with third subtitles (maximum 120 characters) - default is None
    :param subtitle4s: List with fourth subtitles (maximum 120 characters) - default is None
    :param checkedby: Initials of the checker (maximum 3 characters)
    :param filename: Filename for the output, 'figures' by default
    :param portraitformat: Boolean determining whether the figure is portrait or landscape format
    :param print_message: Defines whether a message is returned to the user
    :return: Writes a file with HTML code to the specified output path
    """

    # 0. Validation of string lengths
    if len(drawnby) > 3:
        raise ValueError("Initials cannot be longer than 3 characters")
    if checkedby is not None:
        if len(checkedby) > 3:
            raise ValueError("Initials cannot be longer than 3 characters")
    if len(figure_date) > 10:
        raise ValueError("Dates cannot exceed 10 characters")
    if len(report) > 15:
        raise ValueError("Report number cannot exceed 15 characters")
    if len(rev) > 2:
        raise ValueError("Revision number cannot exceed 2 characters")
    if len(projecttitle) > 95:
        raise ValueError("Project title cannot exceed 95 characters")
    for title in titles:
        if len(title) > 90:
            raise ValueError("Figure titles cannot exceed 90 characters")
    for figno in fignos:
        if len(figno) > 12:
            raise ValueError("Figure titles cannot exceed 12 characters")
    for subtitle in subtitle1s:
        if len(subtitle) > 120:
            raise ValueError("Figure subtitles cannot exceed 120 characters")
    if subtitle2s is not None:
        for subtitle in subtitle2s:
            if len(subtitle) > 120:
                raise ValueError("Figure subtitles cannot exceed 120 characters")
    if subtitle3s is not None:
        for subtitle in subtitle3s:
            if len(subtitle) > 120:
                raise ValueError("Figure subtitles cannot exceed 120 characters")
    if subtitle4s is not None:
        for subtitle in subtitle4s:
            if len(subtitle) > 120:
                raise ValueError("Figure subtitles cannot exceed 120 characters")
    if len(titles) == len(fignos) == len(figures) == len(subtitle1s):
        pass
    else:
        raise ValueError('Lists with figures, figure titles, figure numbers, ... all need to be the same length')
    if subtitle2s is not None:
        if len(subtitle1s) != len(subtitle2s):
            raise ValueError("Lists with subtitles need to be the same length")
    if subtitle3s is not None:
        if len(subtitle1s) != len(subtitle3s):
            raise ValueError("Lists with subtitles need to be the same length")
    if subtitle4s is not None:
        if len(subtitle1s) != len(subtitle4s):
            raise ValueError("Lists with subtitles need to be the same length")

    if portraitformat:
        template = PORTRAIT_TEMPLATE
        figure_height=870
        figure_width=702
    else:
        template = LANDSCAPE_TEMPLATE
        figure_height = 600
        figure_width = 1050
    try:
        # 1. Coerce the figure to correct format, set font and colors
        figure_list = []
        for i, fig in enumerate(figures):

            fig['layout'].update(
                height=figure_height,
                width=figure_width,
                font=PLOTLY_GLOBAL_FONT,
                colorway=PLOTLY_COLORS
            )
            div = plot(fig, auto_open=False, output_type='div', show_link=False, include_plotlyjs=False)
            figure = {
                'path': div,
                'title': titles[i],
                'drawnby': drawnby,
                'report': report,
                'subtitle1': subtitle1s[i],
                'checkedby': checkedby,
                'figno': fignos[i],
                'rev': rev,
                'date': figure_date,
                'projecttitle': projecttitle,
            }
            if subtitle2s is not None:
                figure['subtitle2'] = subtitle2s[i]
            if subtitle3s is not None:
                figure['subtitle3'] = subtitle3s[i]
            if subtitle4s is not None:
                figure['subtitle4'] = subtitle4s[i]
            figure_list.append(figure)

        # 2. Render the template
        rtemplate = Environment(loader=BaseLoader).from_string(template)
        html_figures = rtemplate.render(
            figures=figure_list)

        # 3. Write the output
        with open("%s/%s.html" % (outpath, filename), "w+") as renderedhtmlfile:
            renderedhtmlfile.write(html_figures)

        if print_message:
            print("Figures successfully generated. Open the file %s/%s.html to see the output." % (
                outpath, filename))
    except:
        raise


def plot_with_log(x=[[],], z=[[],], names=[[],], showlegends=None, hide_all_legends=False,
                  modes=None, markerformats=None,
                  soildata=None, fillcolordict={'SAND': 'yellow', 'CLAY': 'brown', 'SILT': 'green', 'ROCK': 'grey'},
                  depth_from_key="Depth from [m]", depth_to_key="Depth to [m]",
                  colors=None, logwidth=0.05,
                  xtitles=[], ztitle=None, xranges=None, zrange=None, ztick=None, dticks=None,
                  layout=dict(),
                  showfig=True):
    """
    Plots a given number of traces in a plot with a soil mini-log on the left hand side.
    The traces are given as a list of lists, the traces are grouped per plotting panel.
    For example x=[[np.linspace(0, 1, 100), np.logspace(0,2,100)], [np.linspace(1, 3, 100), ]] leads to the first two
    traces plotted in the first panel and one trace in the second panel. The same goes for the z arrays, trace names, ...

    :param x: List of lists of x-arrays for the traces
    :param z: List of lists of z-arrays for the traces
    :param names: List of lists of names for the traces (used in legend)
    :param showlegends: Array of booleans determining whether or not to show the trace in the legend. Showing/hiding legends can be specified per trace.
    :param hide_all_legends: Boolean indicating whether all legends need to be hidden (default=False).
    :param modes: List of display modes for the traces (select from 'lines', 'markers' or 'lines+markers'
    :param markerformats: List of formats for the markers (see Plotly docs for more info)
    :param soildata: Pandas dataframe with keys 'Soil type': Array with soil type for each layer, 'Depth from [m]': Array with start depth for each layer, 'Depth to [m]': Array with bottom depth for each layer
    :param fillcolordict: Dictionary with fill colours (default yellow for 'SAND', brown from 'CLAY' and grey for 'ROCK')
    :param depth_from_key: Key for the column with start depths of each layer
    :param depth_to_key: Key for the column with end depths of each layer
    :param colors: List of colours to be used for plotting (default = default Plotly colours)
    :param logwidth: Width of the soil width as a ratio of the total plot with (default = 0.05)
    :param xtitles: Array with X-axis titles for the panels
    :param ztitle: Depth axis title (Depth axis is shared between all panels)
    :param xranges: List with ranges to be used for X-axes
    :param zrange: Range to be used for Y-axis
    :param ztick: Tick interval to be used for the Y-axis
    :param dticks: List of tick intervals to be used for the X-axes
    :param layout: Dictionary with the layout settings
    :param showfig: Boolean determining whether the figure needs to be shown
    :return: Plotly figure object which can be further modified
    """

    no_panels = x.__len__()

    panel_widths = list(map(lambda _x: (1 - logwidth) / no_panels, x))

    panel_widths = list(np.append(logwidth, panel_widths))

    _fig = subplots.make_subplots(rows=1, cols=no_panels + 1, column_widths=panel_widths, shared_yaxes=True,
                                  print_grid=False)

    _showlegends = []
    _modes = []
    _markerformats = []
    _colors = []
    for i, _x in enumerate(x):
        _showlegends_panel = []
        _modes_panel = []
        _markerformats_panel = []
        _colors_panel = []
        for j, _trace_x in enumerate(_x):
            _showlegends_panel.append(not(hide_all_legends))
            _modes_panel.append('lines')
            _markerformats_panel.append(dict(size=5))
            _colors_panel.append(DEFAULT_PLOTLY_COLORS[j])
        _showlegends.append(_showlegends_panel)
        _modes.append(_modes_panel)
        _markerformats.append(_markerformats_panel)
        _colors.append(_colors_panel)

    if showlegends is None:
        showlegends = _showlegends
    if modes is None:
        modes = _modes
    if markerformats is None:
        markerformats = _markerformats
    if colors is None:
        colors = _colors

    _traces = []

    log_dummy_trace = go.Scatter(x=[0, 1], y=[np.nan, np.nan], showlegend=False)
    _fig.append_trace(log_dummy_trace, 1, 1)

    for i, _x in enumerate(x):
        for j, _trace_x in enumerate(_x):
            try:
                _trace = go.Scatter(
                    x=x[i][j],
                    y=z[i][j],
                    mode=modes[i][j],
                    name=names[i][j],
                    showlegend=showlegends[i][j],
                    marker=markerformats[i][j],
                    line=dict(color=colors[i][j]))
                _fig.append_trace(_trace, 1, i + 2)
            except Exception as err:
                warnings.warn(
                    "Error during traces creation for trace %s - %s" % (names[i][j], str(traceback.format_exc())))

    _layers = []
    for i, row in soildata.iterrows():
        _fillcolor = fillcolordict[row['Soil type']]
        _y0 = row[depth_from_key]
        _y1 = row[depth_to_key]
        _layers.append(
            dict(type='rect', xref='x1', yref='y', x0=0, y0=_y0, x1=1, y1=_y1, fillcolor=_fillcolor, opacity=1))

    if zrange is None:
        _fig['layout']['yaxis1'].update(title=ztitle, autorange='reversed')
    else:
        _fig['layout']['yaxis1'].update(title=ztitle, range=zrange)

    _fig['layout'].update(layout)
    _fig['layout'].update(shapes=_layers)

    if ztick is not None:
        _fig['layout']['yaxis1'].update(dtick=ztick)

    _fig['layout']['xaxis1'].update(
        anchor='y', title=None, side='top', tickvals=[])
    for i, _x in enumerate(x):
        _fig['layout']['xaxis%i' % (i + 2)].update(
            anchor='y', title=xtitles[i], side='top')
        if dticks is not None:
            _fig['layout']['xaxis%i' % (i + 2)].update(dtick=dticks[i])
        if xranges is not None:
            _fig['layout']['xaxis%i' % (i + 2)].update(range=xranges[i])

    if showfig:
        iplot(_fig, filename='logplot', config=GROUNDHOG_PLOTTING_CONFIG)
    return _fig

class LogPlot(object):
    """
    Class for planneled plots with a minilog on the side.
    """

    def __init__(self, soilprofile, no_panels=1, logwidth=0.05,
                 fillcolordict={"Sand": 'yellow', "Clay": 'brown', 'Rock': 'grey'},
                 soiltypelegend=True,
                 **kwargs):
        """
        Initializes a figure with a minilog on the side.
        :param soilprofile: Soilprofile used for the minilog
        :param no_panels: Number of panels
        :param logwidth: Width of the minilog as a ratio to the total width of the figure (default=0.05)
        :param fillcolordict: Dictionary with fill colors for each of the soil types. Every unique ``Soil type`` needs to have a corresponding color. Default: ``{"Sand": 'yellow', "Clay": 'brown', 'Rock': 'grey'}``
        :param soiltypelegend: Boolean determining whether legend entries need to be shown for the soil types in the log
        :param kwargs: Optional keyword arguments for the make_subplots method
        """

        # Determine the panel widths
        panel_widths = list(map(lambda _x: (1 - logwidth) / no_panels, range(0, no_panels)))

        panel_widths = list(np.append(logwidth, panel_widths))

        # Set up the figure
        self.fig = subplots.make_subplots(
            rows=1, cols=no_panels+1, column_widths=panel_widths, shared_yaxes=True,
            print_grid=False, **kwargs)
        self.fig['layout']['yaxis1'].update(range=(soilprofile.max_depth, soilprofile.min_depth))

        # Create rectangles for the log plot
        _layers = []
        for i, row in soilprofile.iterrows():
            try:
                _fillcolor = fillcolordict[row['Soil type']]
            except:
                _fillcolor = DEFAULT_PLOTLY_COLORS[i % 10]
            _y0 = row['Depth from [m]']
            _y1 = row['Depth to [m]']
            _layers.append(
                dict(type='rect', xref='x1', yref='y', x0=0, y0=_y0, x1=1, y1=_y1, fillcolor=_fillcolor, opacity=1))

        for _soiltype in soilprofile['Soil type'].unique():
            try:
                _fillcolor = fillcolordict[_soiltype]
            except:
                soiltypelegend = False

            try:
                if soiltypelegend:
                    _trace = go.Bar(
                        x=[-10, -10],
                        y=[row['Depth to [m]'], row['Depth to [m]']],
                        name=_soiltype,
                        marker=dict(color=_fillcolor))
                    self.fig.append_trace(_trace, 1, 1)
            except:
                pass

        self.fig['layout'].update(shapes=_layers)
        self.fig['layout']['xaxis1'].update(
            anchor='y', title=None, side='top', tickvals=[], range=(0, 1))
        self.fig['layout']['yaxis1'].update(title='Depth [m]')

        for i in range(0, no_panels):
            _dummy_data = go.Scatter(
                x=[0, 100],
                y=[np.nan, np.nan],
                mode='lines',
                name='Dummy',
                showlegend=False,
                line=dict(color='black'))
            self.fig.append_trace(_dummy_data, 1, i + 2)
            self.fig['layout']['xaxis%i' % (i + 2)].update(
                anchor='y', title='X-axis %i' % (i+1), side='top')

    def add_trace(self, x, z, name, panel_no, resetaxisrange=True, **kwargs):
        """
        Adds a trace to the plot. By default, lines are added but optional keyword arguments can be added for go.Scatter as ``**kwargs``
        :param x: Array with the x-values
        :param z: Array with the z-values
        :param name: Name for the trace (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param panel_no: Panel to plot the trace on (1-indexed)
        :param resetaxisrange: Boolean determining whether the axis range needs to be reset to fit this trace
        :param kwargs: Optional keyword arguments for the ``go.Scatter`` constructor
        :return: Adds the trace to the specified panel
        """
        try:
            mode = kwargs['mode']
            kwargs.pop('mode')
        except:
            mode = 'lines'
        _data = go.Scatter(
            x=x,
            y=z,
            mode=mode,
            name=name,
            **kwargs)
        self.fig.append_trace(_data, 1, panel_no + 1)

        if resetaxisrange:
            self.fig['layout']['xaxis%i' % (panel_no + 1)].update(
                range=(np.array(x).min(), np.array(x).max()))

    def set_xaxis(self, title, panel_no, **kwargs):
        """
        Changes the X-axis title of a panel
        :param title: Title to be set (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param panel_no: Panel number (1-indexed)
        :param kwargs: Additional keyword arguments for the axis layout update function, e.g. ``range=(0, 100)``
        :return: Adjusts the X-axis of the specified panel
        """
        self.fig['layout']['xaxis%i' % (panel_no + 1)].update(
            title=title, **kwargs)

    def set_zaxis(self, title, **kwargs):
        """
        Changes the Z-axis
        :param title: Title to be set (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param kwargs: Additional keyword arguments for the axis layout update function, e.g. ``range=(0, 100)``
        :return: Adjusts the Z-axis
        """
        self.fig['layout']['yaxis1'].update(
            title=title, **kwargs)

    def set_size(self, width, height):
        """
        Adjust the size of the plot
        :param width: Width of the plot in pixels
        :param height: Height of the plot in pixels
        :return: Adjust the height and width as specified
        """
        self.fig['layout'].update(height=height, width=width)

    def show(self):
        self.fig.show(config=GROUNDHOG_PLOTTING_CONFIG)


class LogPlotMatplotlib(object):
    """
    Class for planneled plots with a minilog on the side, using the Matplotlib plotting backend
    """

    def __init__(self, soilprofile, no_panels=1, logwidth=0.05,
                 fillcolordict={"Sand": 'yellow', "Clay": 'brown', 'Rock': 'grey'},
                 soiltypelegend=True, figheight=6, plot_layer_transitions=True, showgrid=True,
                 **kwargs):
        """
        Initializes a figure with a minilog on the side.
        :param soilprofile: Soilprofile used for the minilog
        :param no_panels: Number of panels
        :param logwidth: Width of the minilog as a percentage of the total width (default=0.05)
        :param fillcolordict: Dictionary with fill colors for each of the soil types. Every unique ``Soil type`` needs to have a corresponding color. Default: ``{"Sand": 'yellow', "Clay": 'brown', 'Rock': 'grey'}``
        :param soiltypelegend: Boolean determining whether legend entries need to be shown for the soil types in the log
        :param figheight: Figure height in inches (default=6in)
        :param plot_layer_transitions: Boolean determining whether layer transitions need to be plotted or not
        :param showgrid: Boolean determining whether a grid is shown on the plot panels or not (default=True)
        :param kwargs: Optional keyword arguments for the make_subplots method
        """
        self.soilprofile = soilprofile
        self.no_panels = no_panels
        # Determine the panel widths
        panel_widths = list(map(lambda _x: (1 - logwidth) / no_panels, range(0, no_panels)))

        panel_widths = list(np.append(logwidth, panel_widths))

        # Set up the figure
        self.fig, self.axes = plt.subplots(1, no_panels + 1, figsize=(4 * no_panels, figheight), sharex=False, sharey=True,
                        constrained_layout=False, gridspec_kw={'width_ratios': panel_widths})
        
        self.axes[0].set_ylim([soilprofile.max_depth, soilprofile.min_depth])

        # Create rectangles for the log plot
        _layers = []
        for i, row in soilprofile.iterrows():
            try:
                _fillcolor = fillcolordict[row['Soil type']]
            except:
                _fillcolor = DEFAULT_PLOTLY_COLORS[i % 10]
            _y0 = row['Depth from [m]']
            _y1 = row['Depth to [m]']
            self.axes[0].fill(
                [0.0,0.0,1.0,1.0],[_y0, _y1, _y1, _y0], fill=True, color=_fillcolor,
                label='_nolegend_', edgecolor="black")
            
        _legend_entries = []
        for _soiltype in soilprofile['Soil type'].unique():
            try:
                _fillcolor = fillcolordict[_soiltype]
            except:
                soiltypelegend = False

            try:
                if soiltypelegend:
                    _legend_entry, = self.axes[0].fill(
                        [-11.0,-11.0,-10.0,-10.0],[_y0, _y1, _y1, _y0], fill=True, color=_fillcolor,
                        label=_soiltype, edgecolor="black")
                    _legend_entries.append(_legend_entry)
            except:
                pass

        self._legend_entries = _legend_entries

        self.axes[0].set_xlim([0, 1])
        self.axes[0].get_xaxis().set_ticks([])
        self.axes[0].set_ylabel('Depth below mudline [m]',size=15)
        for i in range(0, no_panels):
            _dummy_data = self.axes[i+1].plot([0, 100], [np.nan, np.nan], label='_nolegend_')
            self.axes[i+1].tick_params(labelbottom=False,labeltop=True)
            self.axes[i+1].set_xlabel('X-axis %i' % (i + 1), size=15)
            self.axes[i+1].xaxis.set_label_position('top') 
            self.axes[i+1].set_xlim([0, 1])
            self.axes[i+1].set_ylim([soilprofile.max_depth, soilprofile.min_depth])

        self.plot_layer_transitions = plot_layer_transitions

        if showgrid:
            for i in range(0, no_panels):
                self.axes[i+1].grid()
        else:
            pass

    def add_trace(self, x, z, name, panel_no, resetaxisrange=False, line=True, showlegend=False, **kwargs):
        """
        Adds a trace to the plot. By default, lines are added but optional keyword arguments can be added for plt.plot as ``**kwargs``
        :param x: Array with the x-values
        :param z: Array with the z-values
        :param name: Label for the trace (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param panel_no: Panel to plot the trace on (1-indexed)
        :param resetaxisrange: Boolean determining whether the axis range needs to be reset to fit this trace
        :param line: Boolean determining whether the data needs to be shown as a line or as individual markers
        :param showlegend: Boolean determining whether the trace name needs to be added to the legend entries
        :param kwargs: Optional keyword arguments for the ``go.Scatter`` constructor
        :return: Adds the trace to the specified panel
        """
        if line:
            self.axes[panel_no].plot(x, z,label=name, **kwargs)
        else:
            self.axes[panel_no].scatter(x, z,label=name, **kwargs)

        if resetaxisrange:
            self.axes[panel_no].set_xlim([x[~np.isnan(x)].min(), x[~np.isnan(x)].max()])
        
        if showlegend:
            self._legend_entries.append(name)

    def plot_parameter(self, parameter, panel_no, name, **kwargs):
        """
        Plot the trace of a certain parameter in the ``SoilProfile`` object associated with the logplot
        on the specified panel
        """
        z, x = self.soilprofile.soilparameter_series(parameter)
        self.add_trace(x=x, z=z, name=name, panel_no=panel_no, **kwargs)

    def set_xaxis_title(self, title, panel_no, size=15, **kwargs):
        """
        Changes the X-axis title of a panel
        :param title: Title to be set (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param panel_no: Panel number (1-indexed)
        :param kwargs: Additional keyword arguments for the axis layout update function, e.g. ``range=(0, 100)``
        :return: Adjusts the X-axis of the specified panel
        """
        self.axes[panel_no].set_xlabel(title, size=size)

    def set_xaxis_range(self, min_value, max_value, panel_no, **kwargs):
        """
        Changes the X-axis range of a panel
        :param min_value: Minimum value of the plot panel range
        :param max_value: Maximum value of the plot panel range
        :param panel_no: Panel number (1-indexed)
        :param kwargs: Additional keyword arguments for the ``set_xlim`` method
        :return: Adjusts the X-axis range of the specified panel
        """
        self.axes[panel_no].set_xlim([min_value, max_value])

    def set_zaxis_title(self, title, size=15, **kwargs):
        """
        Changes the Z-axis
        :param title: Title to be set (LaTeX allowed, e.g. ``r'$ \alpha $'``)
        :param kwargs: Additional keyword arguments for the ``set_label`` method
        :return: Adjusts the Z-axis title
        """
        self.axes[0].set_ylabel(title, size=size)

    def set_zaxis_range(self, min_depth, max_depth, **kwargs):
        """
        Changes the Z-axis
        :param min_depth: Minimum depth of the plot
        :param max_depth: Maximum depth of the plot
        :param kwargs: Additional keyword arguments for the ``set_ylim`` method
        :return: Adjusts the Z-axis range
        """
        self.axes[0].set_ylim([max_depth, min_depth])

    def set_size(self, width, height):
        """
        Adjust the size of the plot
        :param width: Width of the plot in inches
        :param height: Height of the plot in inches
        :return: Adjust the height and width as specified
        """
        plt.gcf().set_size_inches(width, height)

    def show(self, showlegend=True):
        if self.plot_layer_transitions:
            for i in range(0, self.no_panels):
                for _y in self.soilprofile.layer_transitions():
                    self.axes[i+1].plot(
                        self.axes[i+1].get_xlim(),
                        (_y, _y),
                        color='grey', ls="--"
                    )
        else:
            pass

        if showlegend:
            plt.legend(handles=self._legend_entries, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        plt.show()

    def save_fig(self, path, dpi=250, bbox_inches='tight',pad_inches=1):
        """
        Exports the figure to png format

        :param path: Path of the figure (filename ends in .png)
        :param dpi: Output resolution
        :param bbox_inches: Setting for the bounding box
        :param pad_inches: Inches for padding
        """
        plt.savefig(path, dpi=dpi,bbox_inches=bbox_inches, pad_inches=pad_inches)

    def select_additional_layers(self, no_additional_layers, panel_no=1, precision=2):
        """
        Allows for the selection of additional layer transitions for the ``SoilProfile`` object.
        The number of additional transition is controlled by the ``no_additional_layers`` argument.
        Click on the desired layer transition location in the specified panel (default ``panel_no=1``)
        The depth of the layer transition is rounded according to the ``precision`` argument. Default=2
        for cm accuracy."""
        ax = self.axes[panel_no]
        xy = plt.ginput(no_additional_layers)

        x = [p[0] for p in xy]
        y = [round(p[1], precision) for p in xy]
        for _y in y:
            for i in range(self.axes.__len__() - 1):
                line = self.axes[i+1].plot(
                    self.axes[i+1].get_xlim(),
                    (_y, _y), color='grey', ls="--")
            self.soilprofile.insert_layer_transition(_y)
        ax.figure.canvas.draw()
        
    def select_constant(self, panel_no, parametername, units, nan_tolerance=0.1):
        """
        Selects a constant value in each layer. Click the desired value in each layer, working from the top down.
        If a nan value needs to be set in a layer, click sufficiently close to the minimum of the x axis.
        The ``nan_tolerance`` argument determines which values are interpreted as nan.
        The parameter is added to the ``SoilProfile`` object with the ``'parametername [units]'`` key.
        """
        ax = self.axes[panel_no]
        xy = plt.ginput(self.soilprofile.__len__())

        x = [p[0] for p in xy]
        y = [p[1] for p in xy]
        
        for i, _x in enumerate(x):
            if _x < nan_tolerance:
                x[i] = np.nan

        self.soilprofile["%s [%s]" % (parametername, units)] = x
        self.plot_parameter(
            parameter="%s [%s]" % (parametername, units),
            panel_no=panel_no,
            name=parametername)
        ax.figure.canvas.draw()

    def select_linear(self, panel_no, parametername, units, nan_tolerance=0.1):
        """
        Selects a linear variation in each layer. Click the desired value at each layer boundary.
        Note that a value needs to be selected at the top and bottom of each layer (2 x no layers clicks).
        If a nan value needs to be set in a layer, click sufficiently close to the minimum of the x axis.
        The ``nan_tolerance`` argument determines which values are interpreted as nan.
        The parameter is added to the ``SoilProfile`` object with the ``'parametername [units]'`` key.
        """
        ax = self.axes[panel_no]
        xy = plt.ginput(2 * self.soilprofile.__len__())

        x = [p[0] for p in xy]
        y = [p[1] for p in xy]
        
        for i, _x in enumerate(x):
            if _x < nan_tolerance:
                x[i] = np.nan
                
        self.soilprofile["%s from [%s]" % (parametername, units)] = x[::2]
        self.soilprofile["%s to [%s]" % (parametername, units)] = x[1::2]
        self.plot_parameter(
            parameter="%s [%s]" % (parametername, units),
            panel_no=panel_no,
            name=parametername)
        ax.figure.canvas.draw()