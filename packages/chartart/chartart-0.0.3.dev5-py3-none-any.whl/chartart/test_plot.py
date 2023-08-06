# TODO: Once the package structure is corrected, the next three lines should not be required.
import os
import sys
sys.path.append(os.getcwd())

import pytest
from pandas.core.groupby.generic import GroupBy
from chartart.plot import Figure
from .conftest import *
import json
import numpy as np


def print_json(text: dict) -> str:
    return json.dumps(text, indent=4, sort_keys=True)


def test_init():
    plt_title: str = 'Test Title'
    plt_x_label: str = 'X axis'
    plt_y_label: str = 'Y axis'
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    assert fig.title == plt_title
    assert fig.x_axis_label == plt_x_label
    assert fig.y_axis_label == plt_y_label

    fig = Figure(chart_id='pytest')
    assert fig.title == ''
    assert fig.x_axis_label == 'x'
    assert fig.y_axis_label == 'y'

    fig = Figure(chart_id='pytest', title=plt_title)
    assert fig.title == plt_title
    assert fig.x_axis_label == 'x'
    assert fig.y_axis_label == 'y'

    fig = Figure(chart_id='pytest', x_axis_label=plt_x_label)
    assert fig.title == ''
    assert fig.x_axis_label == plt_x_label
    assert fig.y_axis_label == 'y'

    fig = Figure(chart_id='pytest', y_axis_label=plt_y_label)
    assert fig.title == ''
    assert fig.x_axis_label == 'x'
    assert fig.y_axis_label == plt_y_label


def test_set_title():
    plt_title: str = 'Test Title'
    fig = Figure(chart_id='pytest')
    fig.set_title(plt_title)
    assert fig.title == plt_title


def test_set_x_label():
    plt_x_label: str = 'X axis'
    fig = Figure(chart_id='pytest')
    fig.set_x_label(plt_x_label)
    assert fig.x_axis_label == plt_x_label


def test_set_y_label():
    plt_y_label: str = 'Y axis'
    fig = Figure(chart_id='pytest')
    fig.set_y_label(plt_y_label)
    assert fig.y_axis_label == plt_y_label


def test_line():
    # Numeric
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_data, y_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.line(np.array(x_data), np.array(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.line(pd.Series(x_data), pd.Series(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Datetime
    x_data_dt_numeric: list = [ts.timestamp() * 1e6 for ts in x_data_dt]
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'datetime',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data_dt_numeric,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_data_dt, y_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.line(np.array(x_data_dt), np.array(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.line(pd.Series(x_data_dt), pd.Series(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Line properties
    line_style: str = '.-'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': line_style,
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_data, y_data, ls=line_style)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    line_width: int = 4
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': '-',
            'line_width': line_width,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(np.array(x_data), np.array(y_data), lw=line_width)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    line_colour: str = 'green'
    line_colour_hex: str = '#15b01a'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': line_colour_hex,
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(pd.Series(x_data), pd.Series(y_data), c=line_colour)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    line_label: str = 'price'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': line_colour_hex,
            'line_style': '-',
            'line_width': 1.0,
            'name': line_label
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(pd.Series(x_data), pd.Series(y_data),
             c=line_colour, labels=line_label)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    line_colour: str = 'rose'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_data, y_data, c=line_colour)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Data frame numeric
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': x_col,
        'y_axis_label': y_col,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': data_df[x_col].tolist(),
            'y_data': data_df[y_col].tolist(),
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_col, y_col, data_df)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    with pytest.raises(ValueError):
        fig.line(x_col, y_col)

    fig = Figure(chart_id='pytest')
    with pytest.raises(ValueError):
        fig.line(x_col_dt, y_col, data_df)

    # Data frame datetime
    ts: pd.Timestamp
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': '',
        'x_axis_type': 'datetime',
        'y_axis_type': 'numeric',
        'x_axis_label': x_col_dt,
        'y_axis_label': y_col,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': [ts.timestamp() * 1e6 for ts in data_df_dt[x_col_dt]],
            'y_data': data_df_dt[y_col].tolist(),
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_col_dt, y_col, data_df_dt)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Multiple lines
    plt_title: str = 'Multi-line chart'
    plt_x_label: str = 'Size'
    plt_y_label: str = 'Rent (in $)'
    green_hex: str = '#15b01a'
    red_hex: str = '#e50000'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': plt_title,
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'line',
                'x_data': x_data,
                'y_data': y_data,
                'colour': green_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': 'line_1'
            },
            {
                'type': 'line',
                'x_data': x_data,
                'y_data': y_data,
                'colour': red_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': 'line_2'
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.line(x_data, y_data, c='green')
    fig.line(x_data, y_data, c='red')
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    item_a_hex: str = '#006ba4'
    item_b_hex: str = '#ff800e'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': plt_title,
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[0], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[0], y_col].tolist(),
                'colour': item_a_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': 'a'
            },
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[1], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[1], y_col].tolist(),
                'colour': item_b_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': 'b'
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.line(x_col, y_col, c=c_col, data=data_df)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    item_a_label: str = 'Item A'
    item_b_label: str = 'Item B'
    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': plt_title,
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[0], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[0], y_col].tolist(),
                'colour': item_a_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': item_a_label
            },
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[1], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[1], y_col].tolist(),
                'colour': item_b_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': item_b_label
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.line(x_col, y_col, c=c_col, data=data_df,
             labels=[item_a_label, item_b_label])
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    correct_out: dict = {
        'category': 'cartesian',
        'type': 'line',
        'title': plt_title,
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[0], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[0], y_col].tolist(),
                'colour': item_a_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': items[0]
            },
            {
                'type': 'line',
                'x_data': data_df.loc[data_df[c_col] == items[1], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[1], y_col].tolist(),
                'colour': item_b_hex,
                'line_style': '-',
                'line_width': 1.0,
                'name': items[1]
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.line(x_col, y_col, c=c_col, data=data_df)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)


def test_hline():
    # Numeric
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'line',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [{
            'y_axis': {
                'start': 44,
                'end': 44,
                'text': 44
            }
        }],
        'indicators': [],
        'data': [{
            'type': 'line',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'line_style': '-',
            'line_width': 1.0,
            'name': 'line_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.line(x_data, y_data)
    fig.hline(44)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)


def test_scatter():
    # Numeric
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_data, y_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.scatter(np.array(x_data), np.array(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.scatter(pd.Series(x_data), pd.Series(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Datetime
    x_data_dt_numeric: list = [ts.timestamp() * 1e6 for ts in x_data_dt]
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'datetime',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data_dt_numeric,
            'y_data': y_data,
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_data_dt, y_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.scatter(np.array(x_data_dt), np.array(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.scatter(pd.Series(x_data_dt), pd.Series(y_data))
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Point properties
    points_marker: str = '*'
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'size': 1.0,
            'marker': points_marker,
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_data, y_data, marker=points_marker)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    points_alpha: float = 0.9
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': points_alpha,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(np.array(x_data), np.array(y_data), alpha=points_alpha)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    points_colour: str = 'green'
    points_colour_hex: str = '#15b01a'
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': points_colour_hex,
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(pd.Series(x_data), pd.Series(y_data), c=points_colour)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    points_label: str = 'rent'
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': points_colour_hex,
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': points_label
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(pd.Series(x_data), pd.Series(y_data),
                c=points_colour, labels=points_label)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    point_colour: str = 'crimson'
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_data, y_data, c=point_colour)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Data frame numeric
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': x_col,
        'y_axis_label': y_col,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': data_df[x_col].tolist(),
            'y_data': data_df[y_col].tolist(),
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_col, y_col, data_df)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    with pytest.raises(ValueError):
        fig.scatter(x_col, y_col)

    fig = Figure(chart_id='pytest')
    with pytest.raises(ValueError):
        fig.scatter(x_col_dt, y_col, data_df)

    # Data frame datetime
    ts: pd.Timestamp
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'scatter',
        'x_axis_type': 'datetime',
        'y_axis_type': 'numeric',
        'x_axis_label': x_col_dt,
        'y_axis_label': y_col,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'scatter',
            'x_data': [ts.timestamp() * 1e6 for ts in data_df_dt[x_col_dt]],
            'y_data': data_df_dt[y_col].tolist(),
            'colour': '#000000',
            'size': 1.0,
            'marker': 'o',
            'alpha': 1.0,
            'name': 'point_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.scatter(x_col_dt, y_col, data_df_dt)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    # Multiple data
    plt_title: str = 'Multi-data chart'
    plt_x_label: str = 'Size'
    plt_y_label: str = 'Rent (in $)'
    green_hex: str = '#15b01a'
    red_hex: str = '#e50000'
    correct_out: dict = {
        'category': 'cartesian',
        'title': plt_title,
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'scatter',
                'x_data': x_data,
                'y_data': y_data,
                'colour': green_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': 'point_1'
            },
            {
                'type': 'scatter',
                'x_data': x_data,
                'y_data': y_data,
                'colour': red_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': 'point_2'
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.scatter(x_data, y_data, c='green')
    fig.scatter(x_data, y_data, c='red')
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    item_a_hex: str = '#006ba4'
    item_b_hex: str = '#ff800e'
    correct_out: dict = {
        'category': 'cartesian',
        'title': plt_title,
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'scatter',
                'x_data': data_df.loc[data_df[c_col] == items[0], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[0], y_col].tolist(),
                'colour': item_a_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': 'a'
            },
            {
                'type': 'scatter',
                'x_data': data_df.loc[data_df[c_col] == items[1], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[1], y_col].tolist(),
                'colour': item_b_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': 'b'
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.scatter(x_col, y_col, c=c_col, data=data_df)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    item_a_label: str = 'Item A'
    item_b_label: str = 'Item B'
    correct_out: dict = {
        'category': 'cartesian',
        'title': plt_title,
        'type': 'scatter',
        'x_axis_type': 'numeric',
        'y_axis_type': 'numeric',
        'x_axis_label': plt_x_label,
        'y_axis_label': plt_y_label,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'scatter',
                'x_data': data_df.loc[data_df[c_col] == items[0], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[0], y_col].tolist(),
                'colour': item_a_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': item_a_label
            },
            {
                'type': 'scatter',
                'x_data': data_df.loc[data_df[c_col] == items[1], x_col].tolist(),
                'y_data': data_df.loc[data_df[c_col] == items[1], y_col].tolist(),
                'colour': item_b_hex,
                'size': 1.0,
                'marker': 'o',
                'alpha': 1.0,
                'name': item_b_label
            }]
    }
    fig = Figure(chart_id='pytest', title=plt_title, x_axis_label=plt_x_label,
                 y_axis_label=plt_y_label)
    fig.scatter(x_col, y_col, c=c_col, data=data_df,
                labels=[item_a_label, item_b_label])
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)


def test_get_data_list():
    ts: pd.Timestamp
    x_data_dt_numeric: list = [ts.timestamp() * 1e6 for ts in x_data_dt]
    x_col_data_dt_numeric: list = [
        ts.timestamp() * 1e6 for ts in data_df_dt[x_col_dt]]

    fig = Figure(chart_id='pytest')
    assert fig.get_data_list(x_data) == (x_data, 'numeric')
    assert fig.get_data_list(np.array(x_data)) == (x_data, 'numeric')
    assert fig.get_data_list(pd.Series(x_data)) == (x_data, 'numeric')
    assert fig.get_data_list(x_data_dt) == (x_data_dt_numeric, 'datetime')
    assert fig.get_data_list(x_col, data_df) == (
        data_df[x_col].tolist(), 'numeric')
    assert fig.get_data_list(x_col_dt, data_df_dt) == (
        x_col_data_dt_numeric, 'datetime')
    with pytest.raises(ValueError):
        fig.get_data_list(x_col_dt, data_df)
    with pytest.raises(TypeError):
        fig.get_data_list(x_col)


def test_get_data_from_df():
    fig = Figure(chart_id='pytest')
    pd.testing.assert_series_equal(
        fig.get_data_from_df(x_col, data_df), data_df[x_col])
    with pytest.raises(TypeError):
        fig.get_data_from_df(x_col, None)
    with pytest.raises(ValueError):
        fig.get_data_from_df(x_col_dt, data_df)


def test_cast_np_datetimes():
    numpy_sequence: list = list(
        np.arange(np.datetime64('2020-01-01'), np.datetime64('2020-01-31')))
    correct_sequence: list = pd.date_range(
        start='2020-01-01', end='2020-01-30', periods=30).tolist()

    fig = Figure(chart_id='pytest')
    assert fig.cast_np_datetimes(numpy_sequence) == correct_sequence
    assert fig.cast_np_datetimes(np.array(numpy_sequence)) == correct_sequence


def test_get_colour_hex():
    fig = Figure(chart_id='pytest')
    assert fig.get_colour_hex() == ['#000000']
    assert fig.get_colour_hex('g') == ['#15b01a']
    assert fig.get_colour_hex('green') == ['#15b01a']
    assert fig.get_colour_hex('b') == ['#0343df']
    assert fig.get_colour_hex('blue') == ['#0343df']
    assert fig.get_colour_hex('r') == ['#e50000']
    assert fig.get_colour_hex('red') == ['#e50000']
    assert fig.get_colour_hex('c') == ['#00ffff']
    assert fig.get_colour_hex('cyan') == ['#00ffff']
    assert fig.get_colour_hex('m') == ['#c20078']
    assert fig.get_colour_hex('magenta') == ['#c20078']
    assert fig.get_colour_hex('y') == ['#ffff14']
    assert fig.get_colour_hex('yellow') == ['#ffff14']
    assert fig.get_colour_hex('k') == ['#000000']
    assert fig.get_colour_hex('black') == ['#000000']
    assert fig.get_colour_hex('w') == ['#ffffff']
    assert fig.get_colour_hex('white') == ['#ffffff']
    assert fig.get_colour_hex('#4c8bf5') == ['#4c8bf5']
    assert fig.get_colour_hex('Google Chrome blue') == ['#000000']


def test_get_ax_label():
    fig = Figure(chart_id='pytest')
    assert fig.get_ax_label('line', '0') == 'line_0'
    assert fig.get_ax_label('line', 'point') == 'point'
    assert fig.get_ax_label('line', 'price') == 'price'


def test_parse_colour_input():
    incorrect_col: str = 'revenue'

    correct_out_group: GroupBy = pd.DataFrame(
        {'x': x_data, 'y': y_data, 'grp': 0}).groupby('grp')
    correct_out_colour_hex: list = ['#000000']
    fig = Figure(chart_id='pytest')
    returned_out_group: GroupBy
    returned_out_colour_hex: list
    returned_out_group, returned_out_colour_hex = fig.parse_colour_input(
        x_data, y_data)
    assert all(returned_out_group.apply(
        lambda x: x.equals(correct_out_group.get_group(x.name)) if x.name in correct_out_group.groups else False))
    assert returned_out_colour_hex == correct_out_colour_hex

    correct_out_group: GroupBy = data_df.loc[:, [
        x_col, y_col]].assign(grp=0).groupby('grp')
    correct_out_colour_hex: list = ['#000000']
    fig = Figure(chart_id='pytest')
    returned_out_group, returned_out_colour_hex = fig.parse_colour_input(
        x_col, y_col, data_df, c=incorrect_col)
    assert all(returned_out_group.apply(
        lambda x: x.equals(correct_out_group.get_group(x.name)) if x.name in correct_out_group.groups else False))
    assert returned_out_colour_hex == correct_out_colour_hex

    correct_out_group: GroupBy = data_df.loc[:, [
        x_col, y_col, c_col]].groupby(c_col)
    correct_out_colour_hex: list = default_colour_map.copy()
    fig = Figure(chart_id='pytest')
    returned_out_group, returned_out_colour_hex = fig.parse_colour_input(
        x_col, y_col, data_df, c=c_col)
    assert all(returned_out_group.apply(
        lambda x: x.equals(correct_out_group.get_group(x.name)) if x.name in correct_out_group.groups else False))
    assert returned_out_colour_hex == correct_out_colour_hex


def test_get_column_access_label():
    fig = Figure(chart_id='pytest')
    assert fig.get_column_access_label(x_data, 'x') == 'x'
    assert fig.get_column_access_label(x_col, 'x') == x_col


def test_is_column_present():
    incorrect_col: str = 'revenue'

    fig = Figure(chart_id='pytest')
    assert fig.is_column_present(x_col, data_df) == True
    with pytest.raises(ValueError):
        fig.is_column_present(incorrect_col, data_df)


def test_bar():
    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'bar',
        'x_axis_type': 'categorical',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'bar',
            'x_data': bar_x_data,
            'y_data': height_data,
            'colour': '#15b01a',
            'name': 'bar_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.bar(bar_x_data, height_data, c='green')
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'bar',
        'x_axis_type': 'categorical',
        'y_axis_type': 'numeric',
        'x_axis_label': 'type',
        'y_axis_label': 'height',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'bar',
            'x_data': bar_data_df[bar_x_col].tolist(),
            'y_data': bar_data_df[height_col].tolist(),
            'colour': '#e50000',
            'name': 'bar_1'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.bar(bar_x_col, height_col, data=bar_data_df, c='red')
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    correct_out: dict = {
        'category': 'cartesian',
        'title': '',
        'type': 'bar',
        'x_axis_type': 'categorical',
        'y_axis_type': 'numeric',
        'x_axis_label': 'type',
        'y_axis_label': 'height',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [
            {
                'type': 'bar',
                'x_data': bar_data_df.loc[bar_data_df[c_col] == bar_items[0], bar_x_col].tolist(),
                'y_data': bar_data_df.loc[bar_data_df[c_col] == bar_items[0], height_col].tolist(),
                'colour': '#006ba4',
                'name': bar_items[0]
            },
            {
                'type': 'bar',
                'x_data': bar_data_df.loc[bar_data_df[c_col] == bar_items[1], bar_x_col].tolist(),
                'y_data': bar_data_df.loc[bar_data_df[c_col] == bar_items[1], height_col].tolist(),
                'colour': '#ff800e',
                'name': bar_items[1]
            }
        ]
    }
    fig = Figure(chart_id='pytest')
    fig.bar(bar_x_col, height_col, data=bar_data_df, c=bar_c_col)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    correct_out['data'][0]['name'] = bar_item_names[0]
    correct_out['data'][1]['name'] = bar_item_names[1]
    fig = Figure(chart_id='pytest')
    fig.bar(bar_x_col, height_col, data=bar_data_df, c=bar_c_col,
            labels=bar_item_names)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)


def test_box():
    correct_out: dict = {
        'category': 'box_whisker',
        'title': '',
        'type': 'box',
        'x_axis_type': 'categorical',
        'y_axis_type': 'numeric',
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'box_whisker',
            'x_data': list(range(2001, 2009)),
            'y_data': [
                {"data": [4, 5, 6, 7, 8, 7, 6, 5]},
                {"data": [4, 5, 1, 7, 8, 7, 6, 5]},
                {"data": [7, 5, 6, 7, 8, 7, 13, 5]},
                {"data": [4, 5, 3, 7, 8, 7, 6, 5]},
                {"data": [10, 5, 6, 7, 8, 7, 6, 5]},
                {"data": [4, 5, 6, 18, 8, 7, 6, 5]},
                {"data": [4, 5, 6, 7, 8, 7, 6, 5]},
                {"data": [3, 5, 6, 1, 8, 7, 6, 5]}
            ],
            'colour': '#000000',
            'name': 'box_1'
        }]
    }

    fig = Figure(chart_id='pytest')
    fig.box(x='x', y='y', data=box_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)


def test_pie():
    fig = Figure(chart_id='pytest')
    with pytest.raises(TypeError):
        fig.pie(x_data_dt, y_data)

    pie_data: list = [{'label': 'Low', 'wedge_size': 50},
                      {'label': 'Medium', 'wedge_size': 30},
                      {'label': 'High', 'wedge_size': 20}]
    correct_out: dict = {
        'category': 'circular',
        'title': '',
        'type': None,
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'pie',
            'value_type': 'percent',
            'data': pie_data,
            'wedge_colour': '#000000'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.pie(height_data, bar_x_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.pie(height_data, bar_x_data)
    with pytest.raises(ValueError):
        fig.bar(bar_x_data, height_data)


def test_doughnut():
    fig = Figure(chart_id='pytest')
    with pytest.raises(TypeError):
        fig.doughnut(x_data_dt, y_data)

    doughnut_data: list = [{'label': 'Low', 'wedge_size': 50},
                           {'label': 'Medium', 'wedge_size': 30},
                           {'label': 'High', 'wedge_size': 20}]
    correct_out: dict = {
        'category': 'circular',
        'title': '',
        'type': None,
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'doughnut',
            'value_type': 'percent',
            'data': doughnut_data,
            'wedge_colour': '#000000'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.doughnut(height_data, bar_x_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.doughnut(height_data, bar_x_data)
    with pytest.raises(ValueError):
        fig.bar(bar_x_data, height_data)


def test_radialbar():
    fig = Figure(chart_id='pytest')
    with pytest.raises(TypeError):
        fig.radialbar(x_data_dt, y_data)

    radialbar_data: list = [{'label': 'Low', 'wedge_size': 50},
                            {'label': 'Medium', 'wedge_size': 30},
                            {'label': 'High', 'wedge_size': 20}]
    correct_out: dict = {
        'category': 'circular',
        'title': '',
        'type': None,
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': 'x',
        'y_axis_label': 'y',
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'radialbar',
            'value_type': 'percent',
            'data': radialbar_data,
            'wedge_colour': '#000000'
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.radialbar(height_data, bar_x_data)
    fig.collate_figure_data(sample_token)
    assert fig.data.to_json() == print_json(correct_out)

    fig = Figure(chart_id='pytest')
    fig.radialbar(height_data, bar_x_data)
    with pytest.raises(ValueError):
        fig.bar(bar_x_data, height_data)


def test_table():
    table_data: pd.DataFrame = data_df.reset_index()
    table_columns: list = table_data.columns.tolist()
    table_values: list = table_data.values.tolist()
    x: list
    data: list = [{'values': x} for x in table_values]

    correct_out: dict = {
        'category': 'datagrid',
        'type': 'table',
        'title': '',
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': None,
        'y_axis_label': None,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'table',
            'columns': table_columns,
            'data': data,
            'columnTypes': ['number', 'number', 'number', 'string']
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.table(data_df)
    fig.collate_figure_data(sample_token)
    assert sorted(fig.data.to_json()) == sorted(print_json(correct_out))

    table_data_dt: pd.DataFrame = data_df_dt.reset_index()
    table_data_dt.loc[:, 'date'] = [ts.timestamp() * 1e6 for ts in table_data_dt['date']]
    table_columns_dt: list = table_data_dt.columns.tolist()
    table_values_dt: list = table_data_dt.values.tolist()
    val: list
    table_values_dt = [[int(val[0]), val[1], int(val[2])] for val in table_values_dt]
    x: list
    data_dt: list = [{'values': x} for x in table_values_dt]

    correct_out: dict = {
        'category': 'datagrid',
        'type': 'table',
        'title': '',
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': None,
        'y_axis_label': None,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'table',
            'columns': table_columns_dt,
            'data': data_dt,
            'columnTypes': ['number', 'datetime', 'number']
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.table(data_df_dt)
    fig.collate_figure_data(sample_token)
    assert sorted(fig.data.to_json()) == sorted(print_json(correct_out))

    cols_to_show: list = ['price', 'sales']
    table_data: pd.DataFrame = data_df.loc[:, cols_to_show].reset_index()
    table_columns: list = table_data.columns.tolist()
    table_values: list = table_data.values.tolist()
    x: list
    data: list = [{'values': x} for x in table_values]

    correct_out: dict = {
        'category': 'datagrid',
        'type': 'table',
        'title': '',
        'x_axis_type': None,
        'y_axis_type': None,
        'x_axis_label': None,
        'y_axis_label': None,
        'chartId': 'pytest',
        'idToken': sample_token,
        'notebookName': 'Unknown',
        'plotBand': [],
        'indicators': [],
        'data': [{
            'type': 'table',
            'columns': table_columns,
            'data': data,
            'columnTypes': ['number', 'number', 'number']
        }]
    }
    fig = Figure(chart_id='pytest')
    fig.table(data_df, cols_to_show)
    fig.collate_figure_data(sample_token)
    assert sorted(fig.data.to_json()) == sorted(print_json(correct_out))


def test_heatmap():
    pass
