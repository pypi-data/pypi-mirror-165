from typing import Optional, Union, Tuple
from ipykernel.comm import Comm
from IPython.display import IFrame
from pandas.core.groupby.generic import GroupBy

import datetime
import hashlib
import ipynbname
import json
import numpy as np
import pandas as pd
import requests
import warnings


# try:
#     import ipynbname
# except FileNotFoundError:
#     pass

webAppBaseUrl = 'https://chartart.web.app' #'http://localhost:6060' #
apiGatewayBaseUrl = 'https://chartart4-gw-4sjw1jja.uc.gateway.dev' #'http://localhost:6061' #
refreshTokenUrl = 'https://securetoken.googleapis.com/v1/token?key=AIzaSyAi1uTlyQnilyV0ZrS5LEpUMfBFOUzakwI'

def init(mode: str):
    if(mode == 'cloudps'):
        global webAppBaseUrl
        global apiGatewayBaseUrl
        webAppBaseUrl = 'https://cloudps.web.app' #'http://localhost:6060' #
        apiGatewayBaseUrl = 'https://cloudps-gw-9n7rzkhc.uc.gateway.dev' #'http://localhost:6061' #

def initApp(_webAppBaseUrl: str, _apiGatewayBaseUrl: str):
        global webAppBaseUrl
        global apiGatewayBaseUrl
        webAppBaseUrl = _webAppBaseUrl
        apiGatewayBaseUrl = _apiGatewayBaseUrl

idToken = None
executionStartTime = datetime.datetime.now()  

def generateToken():
  refreshToken = ''
  try:
      f = open('identity.json')
      d = json.load(f)
      if 'idToken' in d:
        return d['idToken']
      if 'refreshToken' not in d:
          raise(Exception("Refresh or ID token not found in file"))
      refreshToken = d['refreshToken']
  except:
      return "Identity file not accessible"
  
  options: dict = {
    'grant_type': 'refresh_token',
    'refresh_token': refreshToken
  }

  response = requests.post(refreshTokenUrl, data=options)
  respJson = response.json()

  if 'error' in respJson:
    raise Exception(respJson['error']['message'])
  
  return respJson['id_token']

def getIdToken():
    global idToken
    global executionStartTime
    timeElapsed =  datetime.datetime.now() -  executionStartTime
    timeElapsed =  timeElapsed.seconds/60 
    if ((idToken is None) or (timeElapsed>59)):
        executionStartTime = datetime.datetime.now()
        idToken = generateToken()
    
    return idToken

def get_param_from_json(fp: str, param: str) -> str:
    """
    
    Load user ID token from the specified file path.
    :param fp: Path to ID token JSON file.
    :return: A string ID.
    """
    try:
        with open(fp, 'r') as f:
            d: dict = json.load(f)
            return d[param]
    except FileNotFoundError:
        raise FileNotFoundError("Identity file not accessible")


def get_notebook_name() -> str:
    try:
        return ipynbname.name()
    except FileNotFoundError:
        return 'Unknown'

def isNotebook():
    """This function is used to get if lib is getting called from standalone python script or from notebook.
    """
    try:
        shell = get_ipython().__class__.__name__
        return True
    except NameError:
        return False 

isNotebook = isNotebook()

class Figure:
    def __init__(self, chart_id: Union[int, float, str], title: str = None,
                 x_axis_label: str = None, y_axis_label: str = None, isRealTime:bool = False,
                 xAxisMaximum: Optional[Union[int, float, str]] = None, xAxisMinimum: Optional[Union[int, float, str]] = None, xAxisOpposedPosition: Optional[bool] = None, xAxisLabelRotation: Optional[int] = None,  xAxisIsVisible: Optional[bool] = None, xAxisDateFormat: Optional[str] = None, xAxisRangePadding: Optional[str] = None, xAxisPlotOffset: Optional[float] = None,
                 yAxisMaximum: Optional[Union[int, float, str]] = None, yAxisMinimum: Optional[Union[int, float, str]] = None, yAxisOpposedPosition: Optional[bool] = None, yAxisLabelRotation: Optional[int] = None,  yAxisIsVisible: Optional[bool] = None, yAxisDateFormat: Optional[str] = None, yAxisRangePadding: Optional[str] = None, yAxisPlotOffset: Optional[float] = None,
                 flex: int = 1):
        # TODO: Convert the instance attributes to class attributes?
        # TODO: Add support for X and Y axis limits.
        # TODO: Add support for dual Y axis.
        self.notebook_name = get_notebook_name()
        """
        Chart ID needs to be compulsorily specified by the user. It seems cumbersome but let's wait for
        user feedback to confirm the hypothesis. If confirmed, there are some ways to deal with it including:
        - Delete document from Preview collection once a Post is created from it.
        - Set up a tracker that deletes data from obsolete/old documents from the Preview collection.
        - We can also construct a ID from the JSON that is sent to server but this can lead to replication
        if the data is slightly modified like one column is log-transformed.
        
        Chart ID is currently needed to minimise the storage requirements in Firestore as documents from 
        Preview collection are not deleted after they are converted into Posts.
        :param xAxisMaximum: In the maximum properties of the axis, you can specify the maximum values with respect to the entire data source.
        :param xAxisMinimum: In the minimum properties of the axis, you can specify the minimum values with respect to the entire data source.
        :param xAxisOpposedPosition: The opposedPosition property of axis can be used to place the axis at the opposite side of its default position.
        :param xAxisLabelRotation: The labelRotation property of axis can be used to rotate the axis labels position.
        :param xAxisIsVisible: When the axis visibility is set to false, then the axis elements like ticks, labels, title, etc will be hidden.
        :param xAxisDateFormat: Date time format in case of date time axis
        :param xAxisRangePadding:   auto :  will apply `none` as padding for horizontal numeric axis, while the vertical numeric axis takes `normal` as padding calculation.
                                    none : ChartRangePadding.none, will not add any padding to the minimum and maximum values.
                                    normal : ChartRangePadding.normal, will apply padding to the axis based on the default range calculation.
                                    additional : will add an interval to the minimum and maximum of the axis.
                                    round :  will round the minimum and maximum values to the nearest possible value.
        :param xAxisPlotOffset: The plotOffset property is used to offset the rendering of the axis at start and end position.
        
        :param yAxisMaximum: In the maximum properties of the axis, you can specify the maximum values with respect to the entire data source.
        :param yAxisMinimum: In the minimum properties of the axis, you can specify the minimum values with respect to the entire data source.
        :param yAxisOpposedPosition: The opposedPosition property of axis can be used to place the axis at the opposite side of its default position.
        :param yAxisLabelRotation: The labelRotation property of axis can be used to rotate the axis labels position.
        :param yAxisIsVisible: When the axis visibility is set to false, then the axis elements like ticks, labels, title, etc will be hidden.
        :param yAxisDateFormat: Date time format in case of date time axis
        :param yAxisRangePadding:   auto :  will apply `none` as padding for horizontal numeric axis, while the vertical numeric axis takes `normal` as padding calculation.
                                    none : ChartRangePadding.none, will not add any padding to the minimum and maximum values.
                                    normal : ChartRangePadding.normal, will apply padding to the axis based on the default range calculation.
                                    additional : will add an interval to the minimum and maximum of the axis.
                                    round :  will round the minimum and maximum values to the nearest possible value.
        :param yAxisPlotOffset: The plotOffset property is used to offset the rendering of the axis at start and end position.
        :param flex: In grid/split layout this is the ratio of size
        """
        if isinstance(chart_id, (int, float)):
            chart_id = str(chart_id)
        self.chart_id = chart_id
        self.title = ''
        if title:
            self.title = title
            
        self.flex = 1
        if flex:
            self.flex = flex

        self.x_axis_label = 'x'
        if x_axis_label:
            self.x_axis_label = x_axis_label

        self.y_axis_label = 'y'
        if y_axis_label:
            self.y_axis_label = y_axis_label

        self.x_axis_type = 'numeric'
        self.y_axis_type = 'numeric'
        self.fig_type = None
        self.axes_type = None

        self.isRealTime = isRealTime
        self.seqNum = 0
        self.data = Data()
        self.axes_count = 0

        # x axis params
        self.xAxisProperties: dict = {}
        if xAxisMaximum:
            self.xAxisProperties['maximum'] = xAxisMaximum
        if xAxisMinimum:
            self.xAxisProperties['minimum'] = xAxisMinimum
        if xAxisOpposedPosition:
            self.xAxisProperties['opposedPosition'] = xAxisOpposedPosition
        if xAxisLabelRotation:
            self.xAxisProperties['labelRotation'] = xAxisLabelRotation
        if xAxisIsVisible:
            self.xAxisProperties['isVisible'] = xAxisIsVisible
        if xAxisDateFormat:
            self.xAxisProperties['dateFormat'] = xAxisDateFormat
        if xAxisRangePadding:
           self. xAxisProperties['rangePadding'] = xAxisRangePadding
        if xAxisPlotOffset:
            self.xAxisProperties['plotOffset'] = xAxisPlotOffset

        # y axis params
        self.yAxisProperties: dict = {}
        if yAxisMaximum:
            self.yAxisProperties['maximum'] = yAxisMaximum
        if yAxisMinimum:
            self.yAxisProperties['minimum'] = yAxisMinimum
        if yAxisOpposedPosition:
            self.yAxisProperties['opposedPosition'] = yAxisOpposedPosition
        if yAxisLabelRotation:
            self.yAxisProperties['labelRotation'] = yAxisLabelRotation
        if yAxisIsVisible:
            self.yAxisProperties['isVisible'] = yAxisIsVisible
        if yAxisDateFormat:
            self.yAxisProperties['dateFormat'] = yAxisDateFormat
        if yAxisRangePadding:
            self.yAxisProperties['rangePadding'] = yAxisRangePadding
        if yAxisPlotOffset:
            self.yAxisProperties['plotOffset'] = yAxisPlotOffset

        self.colour_map: dict = {
            'g': '#15b01a',
            'green': '#15b01a',
            'b': '#0343df',
            'blue': '#0343df',
            'r': '#e50000',
            'red': '#e50000',
            'c': '#00ffff',
            'cyan': '#00ffff',
            'm': '#c20078',
            'magenta': '#c20078',
            'y': '#ffff14',
            'yellow': '#ffff14',
            'k': '#000000',
            'black': '#000000',
            'w': '#ffffff',
            'white': '#ffffff'
        }
        self.default_colour_hex: str = ''
        self.default_colour_name: str = ''
        self.default_colour_map: list = ['']
        self.len_default_colour_map: int = len(self.default_colour_map)

        self.fig_type_mapping = {
            'cartesian': ['line', 'scatter', 'bar'],
            'circular': ['pie'],
            'datagrid': ['table']
        }

        self.plot_band: list = []
        self.technical_indicators: list = []
        self.valid_technical_indicators: dict = {
            'atrIndicator': ['period'],
            'bollingerBandIndicator': ['period'],
            'emaIndicator': ['period', 'valueField'],
            'macdIndicator': ['longPeriod'],
            'momentumIndicator': ['period'],
            'rsiIndicator': ['period', 'overbought', 'oversold'],
            'smaIndicator': ['period', 'valueField'],
            'stochasticIndicator': ['kPeriod', 'dPeriod'],
            'tmaIndicator': ['period', 'valueField']
        }

        self.annotations: list = []

        # ''.join(random.choices(string.ascii_uppercase +
        #                string.digits, k = 10))

    def set_title(self, title: str):
        self.title = title

    def set_x_label(self, lbl: str):
        self.x_axis_label = lbl

    def set_y_label(self, lbl: str):
        self.y_axis_label = lbl

    def set_xAxisMaximum(self, xAxisMaximum: Union[int, float, str]):
         self.xAxisProperties['maximum'] = xAxisMaximum

    def set_xAxisMinimum(self, xAxisMinimum: Union[int, float, str]):
         self.xAxisProperties['minimum'] = xAxisMinimum

    def set_xAxisOpposedPosition(self, xAxisOpposedPosition: bool):
         self.xAxisProperties['opposedPosition'] = xAxisOpposedPosition

    def set_xAxisLabelRotation(self, xAxisLabelRotation: int):
         self.xAxisProperties['labelRotation'] = xAxisLabelRotation

    def set_xAxisIsVisible(self, xAxisIsVisible: bool):
         self.xAxisProperties['isVisible'] = xAxisIsVisible

    def set_xAxisDateFormat(self, xAxisDateFormat: str):
         self.xAxisProperties['dateFormat'] = xAxisDateFormat

    def set_xAxisRangePadding(self, xAxisRangePadding: str):
         self.xAxisProperties['rangePadding'] = xAxisRangePadding

    def set_xAxisPlotOffset(self, xAxisPlotOffset: float):
         self.xAxisProperties['plotOffset'] = xAxisPlotOffset

    def set_yAxisMaximum(self, yAxisMaximum: Union[int, float, str]):
         self.yAxisProperties['maximum'] = yAxisMaximum

    def set_yAxisMinimum(self, yAxisMinimum: Union[int, float, str]):
         self.yAxisProperties['minimum'] = yAxisMinimum

    def set_yAxisOpposedPosition(self, yAxisOpposedPosition: bool):
         self.yAxisProperties['opposedPosition'] = yAxisOpposedPosition

    def set_yAxisLabelRotation(self, yAxisLabelRotation: int):
         self.yAxisProperties['labelRotation'] = yAxisLabelRotation

    def set_yAxisIsVisible(self, yAxisIsVisible: bool):
         self.yAxisProperties['isVisible'] = yAxisIsVisible

    def set_yAxisDateFormat(self, yAxisDateFormat: str):
         self.yAxisProperties['dateFormat'] = yAxisDateFormat

    def set_yAxisRangePadding(self, yAxisRangePadding: str):
         self.yAxisProperties['rangePadding'] = yAxisRangePadding

    def set_yAxisPlotOffset(self, yAxisPlotOffset: float):
         self.yAxisProperties['plotOffset'] = yAxisPlotOffset

    def set_annotation(self, htmlText: str, x: Optional[Union[int, float, str]] = None, y: Optional[Union[int, float, str]] = None, radius: Optional[str] = None):
        """
        Use this method to add annotation on cartesian or circular chart
        Call this method multiple times to add multiple annotations
        :param htmlText: Annotation content in the form of html text
        :param x: x axis % or value in case of cartesian chart
        :param y: y axis % or value in case of cartesian chart
        :param radius: radius of circular chart as string in % e.g ("20%")
        """
        annotation: dict = {}
        annotation['htmlText'] = htmlText
        if x:
            annotation['x'] = x
        if y:
            annotation['y'] = y
        if radius:
            annotation['radius'] = radius

        self.annotations.append(annotation)

    def get_chartIds(self):
        return [{'type':'chart','id':self.chart_id}]


    def line(self, x: Union[str, list, np.ndarray, pd.Series], y: Union[str, list, np.ndarray, pd.Series],
             data: Optional[pd.DataFrame] = None, c: Optional[str] = None, ls: str = '-', lw: float = 1.0,
             labels: Union[Optional[str], Optional[list]] = None, animationDelay: Optional[float] = None, 
             animationDuration: Optional[float]=None, animationType: Optional[str]='parallel'):
        """
        Constructs a line plot.

        :param x: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param y: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param data: A Pandas data frame whose columns are to be plotted.
        :param c: A string of either hex colour code, a column name from `data`, or one of the following
        ['g', 'green', 'b', 'blue', 'r', 'red', 'c', 'cyan', 'm', 'magenta', 'y', 'yellow', 'k', 'black',
        'w', 'white'] to be used to colour the line(s).
        :param ls: A string specifying line style which can be one of ['-', '--', '.-'].
        :param lw: A float specifying line width.
        :param labels: A string or list of strings specifying labels of each line.
        :return:
        """
        self.check_input_data_validity(x, y, data)
        self.axes_type = 'line'
        if animationType == 'sequential':
            current_fig_type: str = 'lineRace'
        else:   
            current_fig_type: str = 'cartesian'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        line_colours: list
        data_groups, line_colours = self.parse_colour_input(x, y, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(y, default='y')
        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: list
        x_axis_type: str
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, x_axis_type = self.get_data_list(
                grp_df.loc[:, _x].values, data)
            # TODO: Check if a group of figures can have multiple axis types.
            self.x_axis_type = x_axis_type
            y_data, y_axis_type = self.get_data_list(
                grp_df.loc[:, _y].values, data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            # - Line types
            # - Line widths
            line_colour: str = line_colours[i % self.len_default_colour_map]
            line_label: str = self.get_ax_label('line', str(grp_id), labels[i])
            self.modify_axis_labels(x, y)

            line_info: dict = {
                'type': 'line',
                'xData': x_data,
                'yData': y_data,
                'color': line_colour,
                'lineStyle': ls,
                'lineWidth': lw,
                'name': line_label,
            }

            if animationDelay is not None:
                line_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                line_info['animationDuration'] = animationDuration

            self.data.insert(line_info)

            i += 1

    def race(self,x: Union[str, list, np.ndarray, pd.Series], y: Union[str, list, np.ndarray, pd.Series],
             data: Optional[pd.DataFrame] = None, c: Optional[str] = None, ls: str = '-', lw: float = 1.0,
             raceType: Optional[str] = 'bar',labels: Union[Optional[str], Optional[list]] = None,
             animationDelay: Optional[float] = None, animationDuration: Optional[float]=None, animationRollingWindow: Optional[int] = None):
        """
        Constructs a line plot.

        :param x: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param y: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param data: A Pandas data frame whose columns are to be plotted.
        :param c: A string of either hex colour code, a column name from `data`, or one of the following
        ['g', 'green', 'b', 'blue', 'r', 'red', 'c', 'cyan', 'm', 'magenta', 'y', 'yellow', 'k', 'black',
        'w', 'white'] to be used to colour the line(s).
        :param ls: A string specifying line style which can be one of ['-', '--', '.-'].
        :param lw: A float specifying line width.
        :param labels: A string or list of strings specifying labels of each line.
        :param animationDelay: wait before starting animation. applicable if animationType == parallel
        :param animationDuration: total time to animate entire series
        :param animationType: parallel or sequential, dapapoints will get printed accordingly.
        :param animationRollingWindow: rolling window for animation, applicable only if animationType == sequential and raceType is line
        :return:
        """
        self.check_input_data_validity(x, y, data)
        if raceType == 'line':
            racetype = 'lineRace'
            current_fig_type: str = 'lineRace'
            self.axes_type = 'lineRace'
        elif raceType == 'bar':
            racetype = 'barRace' 
            current_fig_type: str = 'barRace'
            self.axes_type = 'barRace'

        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        line_colours: list
        data_groups, line_colours = self.parse_colour_input(x, y, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(y, default='y')
        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: list
        x_axis_type: str
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, x_axis_type = self.get_data_list(
                grp_df.loc[:, _x].values, data)
            # TODO: Check if a group of figures can have multiple axis types.
            self.x_axis_type = x_axis_type
            y_data, y_axis_type = self.get_data_list(
                grp_df.loc[:, _y].values, data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            # - Line types
            # - Line widths
            line_colour: str = line_colours[i % self.len_default_colour_map]
            line_label: str = self.get_ax_label('line', str(grp_id), labels[i])
            self.modify_axis_labels(x, y)
            line_info: dict = {
                'type': racetype,
                'xData': x_data,
                'yData': y_data,
                'color': line_colour,
                'lineStyle': ls,
                'lineWidth': lw,
                'name': line_label,
            }

            if animationDelay is not None:
                line_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                line_info['animationDuration'] = animationDuration
            if animationRollingWindow is not None:
                line_info['animationRollingWindow'] = animationRollingWindow


            self.data.insert(line_info)

            i += 1

    @staticmethod
    def check_input_data_validity(x: Union[str, list, np.ndarray, pd.Series],
                                  y: Union[str, list, np.ndarray, pd.Series],
                                  data: Optional[pd.DataFrame] = None):
        if not isinstance(x, (str, list, np.ndarray, pd.Series, pd.Index)):
            raise ValueError(f'`x` should either be a column name or one of '
                             f'list, NumPy array, or Pandas series.')
        if not isinstance(y, (str, list, np.ndarray, pd.Series, pd.Index)):
            raise ValueError(f'`y` should either be a column name or one of '
                             f'list, NumPy array, or Pandas series.')
        if data is not None:
            if not isinstance(data, pd.DataFrame):
                raise ValueError('`data` should be a Pandas dataframe.')
            if (not isinstance(x, str)) or (x not in data.columns):
                raise ValueError('`x` should be a column in the dataframe.')
            if (not isinstance(y, str)) or (y not in data.columns):
                raise ValueError('`y` should be a column in the dataframe.')
        else:
            if isinstance(x, str):
                raise ValueError('`x` should be a column in the dataframe.')
            if isinstance(y, str):
                raise ValueError('`y` should be a column in the dataframe.')

    def check_multi_axes_consistency(self, current_type: str) -> Optional[bool]:
        if (self.fig_type is None) or (self.fig_type == current_type):
            return True

        raise ValueError(f'Plots of type {current_type} (examples '
                         f'{self.fig_type_mapping[current_type]}) cannot '
                         f'be combined with plots of type {self.fig_type} '
                         f'(examples {self.fig_type_mapping[self.fig_type]}).')

    def parse_colour_input(self, x: Union[str, list, np.ndarray, pd.Series], y: Union[str, list, np.ndarray, pd.Series],
                           data: Optional[pd.DataFrame] = None, c: Union[Optional[str], Optional[list]] = None) -> Tuple[GroupBy, list]:
        if data is None:
            return pd.DataFrame({'x': list(x), 'y': list(y), 'grp': 0}).groupby('grp'), self.get_colour_hex(c)
        if c not in data.columns:
            return data.loc[:, [x, y]].assign(grp=0).groupby('grp'), self.get_colour_hex(c)

        colour_groups: GroupBy = data.loc[:, [x, y, c]].groupby([c])

        return colour_groups, list(colour_groups.groups.keys())

    @staticmethod
    def get_column_access_label(d: Union[str, list, np.ndarray, pd.Series],
                                default: str):
        if isinstance(d, str):
            return d

        return default

    @staticmethod
    def is_column_present(d: str, data: pd.DataFrame) -> bool:
        if d not in data:
            raise ValueError(f'Cannot find column {d} in input data frame.')

        return True

    @staticmethod
    def check_user_labels(num_groups: int, labels: Union[Optional[str], Optional[list]] = None) -> list:
        if labels is None:
            return [None] * num_groups

        if isinstance(labels, str):
            labels = [labels]

        if len(labels) != num_groups:
            raise ValueError(f'Number of input labels ({len(labels)}° does not match the number of groups '
                             f'({num_groups})')

        return labels

    def get_data_list(self, d: Union[str, list, np.ndarray, pd.Series],
                      data: Optional[pd.DataFrame] = None) -> Tuple[list, str]:
        if isinstance(d, str):
            d = self.get_data_from_df(d, data)
        axis_type: str = self.get_axis_type(d[0])
        out_d: list
        if axis_type == 'datetime':
            out_d = self.convert_datetime_to_epoch(d)
        elif isinstance(d, (np.ndarray, pd.Series, pd.Index)):
            # `tolist()` convert datetime objects to integers representing time elapsed,
            # in nanoseconds, since `1970-01-01 00:00`.
            out_d = d.tolist()
        else:
            out_d = d.copy()

        return out_d, axis_type

    def convert_datetime_to_epoch(self, d: Union[list, np.ndarray, pd.Series]) -> list:
        d = self.cast_np_datetimes(d)
        ts: Union[datetime.datetime, pd.Timestamp]
        out_d = [ts.timestamp() * 1e9 for ts in d]

        return out_d

    def get_data_from_df(self, d: str, data: Optional[pd.DataFrame]) -> Optional[pd.Series]:
        if self.is_column_present(d, data):
            return data[d].copy()

    @staticmethod
    def cast_np_datetimes(d: Union[list, np.ndarray]) -> list:
        ts: Union[datetime.datetime, pd.Timestamp, np.datetime64]
        return [pd.Timestamp(ts) if isinstance(ts, np.datetime64) else ts for ts in d]

    @staticmethod
    def get_axis_type(x: Union[int, float, datetime.datetime, np.datetime64]) -> str:
        if isinstance(x, (datetime.datetime, np.datetime64, pd.Timestamp)):
            return 'datetime'
        elif isinstance(x, (int, float, np.int8, np.int16, np.int32, np.int64,
                            np.float16, np.float32, np.float64)):
            return 'numeric'
        elif isinstance(x, str):
            return 'categorical'
        else:
            raise ValueError(f'Line chart supports X-axis of types integer, float, datetime.datetime, and '
                             f'np.datetime64 and not {type(x)}')

    def get_colour_hex(self, c: Union[Optional[str], Optional[list]]  = None) -> list:
        if not c:
            return [self.default_colour_hex]
        colour_hex_list =[]

        if isinstance(c, str):
            c=[c]

        for colour in c:
            colour_hex: Optional[str] = self.colour_map.get(colour, None)
            if not colour_hex:
                if colour.startswith('#'):
                    colour_hex_list.append(colour)
                    continue
                else:
                    warnings.warn(
                        f'{colour} is not a valid colour. Using the default {self.default_colour_name}.')
                    colour_hex_list.append(self.default_colour_hex)
                    continue

            colour_hex_list.append(colour_hex)

        return colour_hex_list

    def get_ax_label(self, ax_type: str, grp_label: str, user_label: Optional[str] = None) -> str:
        if user_label is None:
            if grp_label == '0':
                return f'{ax_type}_{self.axes_count}'
            else:
                return grp_label
        else:
            return user_label

    def modify_axis_labels(self, x: Union[str, list, np.ndarray, pd.Series],
                           y: Union[str, list, np.ndarray, pd.Series]):
        if isinstance(x, str) and (self.x_axis_label == 'x'):
            self.x_axis_label = x
        if isinstance(y, str) and (self.y_axis_label == 'y'):
            self.y_axis_label = y

    def hline(self, y: Union[int, float], label: Optional[str] = None):
        if label is None:
            label = y
        self.plot_band.append({
            'yAxis': {
                'start': y,
                'end': y,
                'text': label
            },

        })

    def vline(self, x: Union[int, float], label: Optional[str] = None):
        if label is None:
            label = x
        self.plot_band.append({
            'xAxis': {
                'start': x,
                'end': x,
                'text': label
            }
        })

    def scatter(self, x: Union[str, list, np.ndarray, pd.Series], y: Union[str, list, np.ndarray, pd.Series],
                data: Optional[pd.DataFrame] = None, c: Optional[str] = None, size: float = 1.0, marker: str = 'o',
                alpha: float = 1.0, labels: Union[Optional[str], Optional[list]] = None,animationDelay: Optional[float] = None, 
                animationDuration: Optional[float]=None, animationType: Optional[str]='parallel'):
        """
        Constructs a scatter plot.

        :param x: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param y: A list, NumPy array, Pandas series or a column name from `data` to plot on the X-axis.
        :param data: A Pandas data frame whose columns are to be plotted.
        :param c: A string of either hex colour code, a column name from `data`, or one of the following
        ['g', 'green', 'b', 'blue', 'r', 'red', 'c', 'cyan', 'm', 'magenta', 'y', 'yellow', 'k', 'black',
        'w', 'white'] to be used to colour the points.
        :param size: A float specifying the point size.
        :param marker: A string specifying the point shape which can be one of ['o', '*'].
        :param alpha: A float between 0 and 1 denoting opacity of points.
        :param labels: A string or list of strings specifying labels of each point.
        :return:
        """
        self.check_input_data_validity(x, y, data)
        self.axes_type = 'scatter'
        
        if animationType == 'sequential':
            current_fig_type: str = 'lineRace'
        else:   
            current_fig_type: str = 'cartesian'
        
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        point_colours: list
        data_groups, point_colours = self.parse_colour_input(x, y, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(y, default='y')
        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: list
        x_axis_type: str
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, x_axis_type = self.get_data_list(
                grp_df.loc[:, _x].values, data)
            self.x_axis_type = x_axis_type
            y_data, y_axis_type = self.get_data_list(
                grp_df.loc[:, _y].values, data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            # - Point types
            # - Point sizes
            point_colour: str = point_colours[i % self.len_default_colour_map]
            point_label: str = self.get_ax_label(
                'point', str(grp_id), labels[i])
            self.modify_axis_labels(x, y)

            point_info: dict = {
                'type': 'scatter',
                'xData': x_data,
                'yData': y_data,
                'color': point_colour,
                'size': size,
                'marker': marker,
                'alpha': alpha,
                'name': point_label,
            }

            if animationDelay is not None:
                point_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                point_info['animationDuration'] = animationDuration

            self.data.insert(point_info)

            i += 1

    def bar(self, x: Union[str, list, np.ndarray, pd.Series, pd.Index],
            height: Union[str, list, np.ndarray, pd.Series], data: Optional[pd.DataFrame] = None, c: str = None,
            labels: Optional[list] = None,barType:Optional[str]='vertical' ,animationDelay: Optional[float] = None, 
             animationDuration: Optional[float] = None, animationType: Optional[str]='parallel', animationRollingWindow: Optional[int] = None):
        """
        Constructs a bar chart.

        :param x: A list, NumPy array, Pandas series, Pandas index, or column name of `data` to plot bars for.
        :param height: A list, NumPy array, Pandas series, or column name of `data` denoting height of each bar.
        :param data: A Pandas data frame whose columns are to be plotted.
        :param c: A string of either hex colour code, a column name from `data`, or one of the following
        ['g', 'green', 'b', 'blue', 'r', 'red', 'c', 'cyan', 'm', 'magenta', 'y', 'yellow', 'k', 'black',
        'w', 'white'] to be used to colour the bars.
        :param labels: A string or list of strings specifying labels of each bar.
        :param animationDelay: wait before starting animation. applicable if animationType == parallel
        :param animationDuration: total time to animate entire series
        :param animationType: parallel or sequential, dapapoints will get printed accordingly.
        :param animationRollingWindow: rolling window for animation, applicable only if animationType == sequential
        :return:
        """
        self.check_not_datetime(x[0])
        self.axes_type = 'bar'
        self.check_input_data_validity(x, height, data)

        if animationType == 'sequential':
            current_fig_type: str = 'lineRace'
        else:   
            current_fig_type: str = 'cartesian'

        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        bar_colours: list
        data_groups, bar_colours = self.parse_colour_input(x, height, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(height, default='y')
        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: list
        x_axis_type: str
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, x_axis_type = self.get_data_list(
                grp_df.loc[:, _x].values, data)
            self.x_axis_type = x_axis_type
            y_data, y_axis_type = self.get_data_list(
                grp_df.loc[:, _y].values, data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            bar_colour: str = bar_colours[i]
            bar_label: str = self.get_ax_label('bar', str(grp_id), labels[i])
            self.modify_axis_labels(x, height)
            if barType == 'vertical':
                barType = 'column'
            elif barType == 'horizontal':
                barType = 'bar'
            bar_info: dict = {
                'type': barType,
                'xData': x_data,
                'yData': y_data,
                'color': bar_colour,
                'name': bar_label,
            }

            if animationDelay is not None:
                bar_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                bar_info['animationDuration'] = animationDuration
            if animationRollingWindow is not None:
                bar_info['animationRollingWindow'] = animationRollingWindow

            self.data.insert(bar_info)

            i += 1

    def check_not_datetime(self, x: Union[int, float, datetime.datetime,
                                          np.datetime64]):
        if self.get_axis_type(x) in ['datetime', 'np.datetime64']:
            raise TypeError('Pie/Bar chart does not support datetime values.')

    def box(self, x: Union[str, list, np.ndarray, pd.Series, pd.Index],
            y: Union[str, list, np.ndarray, pd.Series],
            data: Optional[pd.DataFrame] = None, c: str = None,
            labels: Optional[list] = None, animationDelay: Optional[float] = None, 
             animationDuration: Optional[float] = None):
        self.check_not_datetime(x[0])
        self.axes_type = 'box'
        self.check_input_data_validity(x, y, data)
        current_fig_type: str = 'boxWhisker'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        box_colours: list
        data_groups, box_colours = self.parse_colour_input(x, y, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(y, default='y')

        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: Optional[list]
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, _ = self.get_data_list(grp_df.loc[:, _x].values, data)
            self.x_axis_type = 'categorical'
            y_data, y_axis_type = self.get_data_list(grp_df.loc[:, _y].values,
                                                     data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            box_colour: str = box_colours[i % self.len_default_colour_map]
            box_label: str = self.get_ax_label('box', str(grp_id), labels[i])
            self.modify_axis_labels(x, y)

            formatted_x_data: list
            formatted_y_data: list
            formatted_x_data, formatted_y_data = \
                self.format_data_for_box_plot(x_data, y_data)

            box_info: dict = {
                'type': 'boxWhisker',
                'xData': formatted_x_data,
                'yData': formatted_y_data,
                'color': box_colour,
                'name': box_label,
            }

            if animationDelay is not None:
                box_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                box_info['animationDuration']= animationDuration

            self.data.insert(box_info)

            i += 1

    @staticmethod
    def format_data_for_box_plot(x_data: list,
                                 y_data: list) -> Tuple[list, list]:
        xy_data: GroupBy = pd.DataFrame(
            {'x': x_data, 'y': y_data}).groupby('x')
        xy_grp_id: str
        xy_grp_df: pd.DataFrame
        formatted_x_data: list = []
        formatted_y_data: list = []
        for xy_grp_id, xy_grp_df in xy_data:
            formatted_x_data.append(xy_grp_id)
            formatted_y_data.append({'data': xy_grp_df['y'].tolist()})

        return formatted_x_data, formatted_y_data

    def hist(self, y: Union[str, list, np.ndarray, pd.Series],
             data: Optional[pd.DataFrame] = None, c: Optional[str] = None,
             binwidth: int = 50, show_normal_curve: bool = False,
             labels: Optional[list] = None, animationDelay: Optional[float] = None, 
             animationDuration: Optional[float] = None):
        if data is None:
            x: list = [0 for _ in range(len(y))]
        else:
            x: str = 'x'
            data.loc[:, 'x'] = [0 for _ in range(len(data))]

        self.check_not_datetime(y[0])
        self.check_input_data_validity(x, y, data)
        current_fig_type: str = 'histogram'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        hist_colours: list
        data_groups, hist_colours = self.parse_colour_input(x, y, data, c)
        labels = self.check_user_labels(len(data_groups), labels)
        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(y, default='y')
        i: int = 0
        grp_id: int
        grp_df: pd.DataFrame
        x_data: list
        y_data: list
        x_axis_type: str
        y_axis_type: str
        for grp_id, grp_df in data_groups:
            x_data, x_axis_type = self.get_data_list(grp_df.loc[:, _x].values,
                                                     data)
            self.x_axis_type = x_axis_type
            y_data, y_axis_type = self.get_data_list(grp_df.loc[:, _y].values,
                                                     data)
            self.y_axis_type = y_axis_type
            # TODO: Add support for custom:
            # - Colour maps
            hist_colour: str = hist_colours[i % self.len_default_colour_map]
            hist_label: str = self.get_ax_label('hist', str(grp_id), labels[i])
            self.modify_axis_labels(x, y)

            hist_info: dict = {
                'type': 'histogram',
                'yData': y_data,
                'binInterval': binwidth,
                'color': hist_colour,
                'showNormalDistributionCurve': show_normal_curve,
                'name': hist_label
            }

            if animationDelay is not None:
                hist_info['animationDelay'] = animationDelay
            if animationDuration is not None:
                hist_info['animationDuration'] = animationDuration

            self.data.insert(hist_info)

            i += 1

    def pie(self, x: Union[list, np.ndarray, pd.Series], label: Union[list, np.ndarray, pd.Series, pd.Index],
            c: Union[list,str] = None, animationDelay: Optional[float] = None, animationDuration: Optional[float] = None, animationType: Optional[str]='parallel'):
        """
        Constructs a pie chart.

        :param x: A list, NumPy array, or Pandas series denoting the size of each pie.
        :param label: A list, NumPy array, Pandas series, or Pandas index denoting the label of each pie.
        :param c: A hex code or string specifying pie colour.
        :param animationDelay: wait before starting animation. applicable if animationType == parallel
        :param animationDuration: total time to animate entire series
        :param animationType: parallel or sequential, dapapoints will get printed accordingly.
        :return:
        """
        self._construct_circular_chart(x, label, c, 'pie',animationDelay,animationDuration,animationType)

    def _construct_circular_chart(self, x: Union[list, np.ndarray, pd.Series],
                                  label: Union[list, np.ndarray, pd.Series, pd.Index],
                                  c: Union[list,str] = None, kind: str = 'pie',animationDelay: Optional[float] = None, 
                                  animationDuration: Optional[float] = None, animationType: Optional[str]='parallel'):
        self.check_not_datetime(x[0])
        self.check_input_data_validity(x, label)
        if animationType == 'sequential':
            current_fig_type: str = 'circularRace'
        else:   
            current_fig_type: str = 'circular'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.axes_count += 1
        data_groups: GroupBy
        bar_colours: list
        data_groups, pie_colours = self.parse_colour_input(x, label, None, c)

        _x: str = self.get_column_access_label(x, default='x')
        _y: str = self.get_column_access_label(label, default='y')
        i: int = 0
        wedge_data: list
        label_data: list
        for grp_id, grp_df in data_groups:
            wedge_data, _ = self.get_data_list(grp_df.loc[:, _x].values)
            self.x_axis_type = None
            label_data, _ = self.get_data_list(grp_df.loc[:, _y].values)
            self.y_axis_type = None
            pie_dict = {'label': label_data, 'wedgeSize': wedge_data}
            if len(pie_colours)==0:
                pie_dict ['color'] = pie_colours
            pie_data: list = pd.DataFrame(pie_dict).to_dict(orient='records')
            pie_value_type: str = self.get_pie_value_type(wedge_data)
            pie_info: dict = {
                'type': kind,
                'valueType': pie_value_type,
                'data': pie_data,
            }

            if animationDelay is not None:
                pie_info['animationDelay'] = animationDelay

            if animationDuration is not None:
                pie_info['animationDuration'] = animationDuration

            self.data.insert(pie_info)

            i += 1
    def doughnut(self, x: Union[list, np.ndarray, pd.Series], label: Union[list, np.ndarray, pd.Series, pd.Index],
                 c: Union[list,str] = None,animationDelay: Optional[float] = None, animationDuration: Optional[float] = None, animationType: Optional[str]='parallel'):
        """
        Constructs a doughnut chart.

        :param x: A list, NumPy array, or Pandas series denoting the size of each doughnut piece.
        :param label: A list, NumPy array, Pandas series, or Pandas index denoting the label of each doughnut piece.
        :param c: A hex code or string specifying each doughnut colour.
        :param animationDelay: wait before starting animation. applicable if animationType == parallel
        :param animationDuration: total time to animate entire series
        :param animationType: parallel or sequential, dapapoints will get printed accordingly.
        :return:
        """
        self._construct_circular_chart(x, label, c, 'doughnut',animationDelay,animationDuration,animationType)

    def radialbar(self, x: Union[list, np.ndarray, pd.Series], label: Union[list, np.ndarray, pd.Series, pd.Index],
                  c: Union[list,str] = None,animationDelay: Optional[float] = None, animationDuration: Optional[float] = None, animationType: Optional[str]='parallel'):
        """
        Constructs a radial bar chart.

        :param x: A list, NumPy array, or Pandas series denoting the size of each radial bar.
        :param label: A list, NumPy array, Pandas series, or Pandas index denoting the label of each radial bar.
        :param c: A hex code or string specifying radial bar colour.
        :param animationDelay: wait before starting animation. applicable if animationType == parallel
        :param animationDuration: total time to animate entire series
        :param animationType: parallel or sequential, dapapoints will get printed accordingly.
        :return:
        """
        self._construct_circular_chart(x, label, c, 'radialbar',animationDelay,animationDuration,animationType)

    @staticmethod
    def get_pie_value_type(x: list) -> str:
        if sum(x) == 100.:
            return 'percent'
        else:
            return 'absolute'

    def table(self, df: pd.DataFrame, cols: Union[str, list] = 'all'):
        self.axes_type = 'table'
        current_fig_type: str = 'datagrid'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        cols_to_render: list = self.get_cols_to_render(cols, df)
        df_to_render: pd.DataFrame = df.loc[:, cols_to_render].copy()

        table_info: dict = self.reorient_df_for_datagrid(df_to_render)
        table_info['type'] = 'table'

        self.data.insert(table_info)

    def html(self, htmlText: str = None):
        """Generate HTML.

        :param htmlText: HTML text to render, refer https://demo.fwfh.dev/supported/tags.html  for supported tags.
        :return:
        """
        current_fig_type: str = 'html'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        html_info: dict = {}
        html_info['type'] = 'html'
        html_info['htmlText'] = htmlText
        self.data.insert(html_info)

    def markdown(self, markdownText: str = None):
        """Generate Markdown.

        :param markdownText: Markdown text to render.
        :return:
        """
        current_fig_type: str = 'markdown'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        markdown_info: dict = {}
        markdown_info['type'] = 'markdown'
        markdown_info['markdownText'] = markdownText
        self.data.insert(markdown_info)

    @staticmethod
    def get_cols_to_render(cols: Union[str, list], df: pd.DataFrame) -> list:
        if cols == 'all':
            return list(df.columns)
        elif isinstance(cols, str):
            return [cols]
        else:
            return cols.copy()

    def set_datagrid_figure_details(self):
        self.x_axis_type = None
        self.y_axis_type = None
        self.x_axis_label = None
        self.y_axis_label = None

    def reorient_df_for_datagrid(self, df: pd.DataFrame) -> dict:
        df = df.reset_index()
        df_map: dict = df.to_dict(orient='split')
        df_map['columnTypes'] = self.guess_column_types(df)
        x: list
        col_type: str
        df_map['data'] = [{'values': self.format_column_values(x, df_map['columnTypes'])}
                          for x in df_map['data']]
        _ = df_map.pop('index')

        return df_map

    def format_column_values(self, x: list, col_types: list) -> list:
        formatted_x: list = []
        col_type: str
        for val, col_type in zip(x, col_types):
            if col_type == 'datetime':
                formatted_x.extend(self.convert_datetime_to_epoch([val]))
            else:
                formatted_x.extend([val])

        return formatted_x

    @staticmethod
    def guess_column_types(df: pd.DataFrame) -> list:
        col_types: list = []
        col_name: str
        for col_name in df.columns:
            py_col_sample = df.loc[:, col_name].iloc[0]
            if isinstance(py_col_sample, (int, float,
                                          np.int8, np.int16, np.int32, np.int64,
                                          np.float16, np.float32, np.float64)):
                col_types.append('number')
            elif isinstance(py_col_sample, (datetime.datetime, pd.Timestamp, np.datetime64)):
                col_types.append('datetime')
            else:
                col_types.append('string')

        return col_types

    def heatmap(self, df: pd.DataFrame, cmap: str = 'default', vmin: float = None, vmax: float = None,
                annotate: bool = False, invertedColors: bool = False):
        """Generate heatmap.

        :param df:
        :param cmap:
        :param vmin:
        :param vmax:
        :param annotate:
        :return:
        """
        current_fig_type: str = 'heatmap'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        heatmap_info: dict = self.reorient_df_for_datagrid(df)
        heatmap_info['type'] = 'heatmap'
        heatmap_info['cmap'] = cmap
        heatmap_info['vmin'] = vmin
        heatmap_info['vmax'] = vmax
        heatmap_info['showCellValues'] = annotate
        heatmap_info['invertedColors'] = invertedColors

        self.data.insert(heatmap_info)

    def treemap(self,levels: list, data : pd.DataFrame,values,c:list,layout: str = "squarified"):

        current_fig_type: str = 'treemap'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        treemap_info: dict = {
            'type': 'treemap',
        }

        levelList=[]
        for level,color in zip(levels,c):
            levelList.append({"groupMapper": level,
                              "color": color})

        treemap_info["levels"]=levelList
        treemap_info["weightValueMapper"] = values
        treemap_info["layout"] =  layout
        treemap_info["legend"] = {
                           "mode": "bar",
                           "position": "top"
                        }
        treemap_info["enableDrilldown"] =  True
        levels.append(values)
        treemap_info['data'] = data[levels].to_dict(orient='records')
        self.data.insert(treemap_info)

    def map(self, mapOf: str, data: Union[str, list, np.ndarray, pd.Series], primaryValueMapper : str, zoomLevel: Optional[float] = None, focalLatitude: Optional[float] = None, 
            focalLongitude: Optional[float] = None, shapeColorValueMapper: Optional[str] = None, shapeColorMapper: Optional[list] = None, 
            bubbleSizeMapper: Optional[str] = None, bubbleColorValueMapper: Optional[str] = None, bubbleColorMappers: Optional[list] = None, legend: Optional[dict] = None, marker: Optional[list] = None):
        """Generate Map.

        :param mapOf: world or india 
        :param data: list of input data values , see example below
        :param primaryValueMapper: key to bind given data to jeo json data.
        :param zoomLevel: Used to set the current zoom level of the map. Default value is 1 which will show the whole map in the viewport.
        :param focalLatitude: Latitude value of focal point of the map layer based on which zooming happens.
        :param focalLongitude: Longitude value of focal point of the map layer based on which zooming happens.
        :param shapeColorValueMapper: A Field from data which decides color of shapes.
        :param shapeColorMapper: A value or range of values and its corresponding color mapping for shapes. 
        :param bubbleSizeMapper: A field from data which decides size of bubble.
        :param bubbleColorValueMapper: A field from data which decides color of shape.
        :param bubbleColorMappers: A value or range of values and its corresponding color mapping for bubbles.
        :param legend: legends for a map.
        :return:
        """
        current_fig_type: str = 'map'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.set_datagrid_figure_details()
        map_info: dict = {
            'type': 'map',
        }

        map_info["mapOf"] = mapOf
        map_info["primaryValueMapper"] = primaryValueMapper
        if zoomLevel is not None:
            map_info['zoomLevel'] = zoomLevel
        if focalLatitude is not None:
            map_info['focalLatitude'] = focalLatitude
        if focalLongitude is not None:
            map_info['focalLongitude'] = focalLongitude
        if shapeColorValueMapper is not None:
            map_info['shapeColorValueMapper'] = shapeColorValueMapper
        if shapeColorMapper is not None:
            map_info['shapeColorMapper'] = shapeColorMapper  
        if bubbleSizeMapper is not None:
            map_info['bubbleSizeMapper'] = bubbleSizeMapper
        if bubbleColorValueMapper is not None:
            map_info['bubbleColorValueMapper'] = bubbleColorValueMapper
        if bubbleColorMappers is not None:
            map_info['bubbleColorMappers'] = bubbleColorMappers
        if legend is not None:
            map_info['legend'] = legend
        if marker is not None:
            map_info['marker'] = marker

        map_info['data'] = data
        self.data.insert(map_info)

    def candlestick(self, df: pd.DataFrame, label: Optional[str] = None, indicators: Optional[list] = None, animationDelay: Optional[float] = None, animationDuration: Optional[float] = None):
        """Generate candlestick chart.

        :param df: Dataframe with time index and four columns representing
        open, close, high, and low values.
        :param label: (Optional) Name of the script being shown by the chart.
        :param indicators: (Optional) Name and/or parameters of technical indicators to overlay on the chart.
        :type df: pd.DataFrame

        Technical indicators can either be specified as a string or a dictionary consisting of the indicator name
        and its optional parameters. Details of supported indicators are as follows:
        1. ATR indicator
            (a) We can specify the indicator name and period as follows:
            ```
            {'name': 'atrIndicator',
             'period': 10}
            ```

             (b) We can specify only the indicator name as `atrIndicator`. The default period is .

        2. Bollinger Band Indicator
            (a) This indicator has an optional parameter called `period`. We can specify it as follows:
            ```
            {'name': 'bollingerBandIndicator',
             'period': 10}
            ```

            (b) Only the indicator name can be specified as `bollingerBandIndicator`. The default period is .

        3. EMA Indicator
            (a) To specify it using the period and value field:
            ```
            {'name': 'emaIndicator',
             'period': 10,
             'valueField': 'value'}
            ```

            (b) We can specify it as a string `emaIndicator` to use the default period () and value field ().

        4. MACD Indicator
            (a) To specify the long period:
            ```
            {'name': 'macdIndicator',
             'longPeriod': 10}
            ```

            (b) As a string, we can provide the indicator as `macdIndicator` with the default long period set to .

        5. Momentum Indicator
            (a) It also has an optional period:
            ```
            {'name': 'momentumIndicator',
             'period': 10}
            ```

            (b) We can specify it as a string `momentumIndicator` which uses the default period of .

        6. RSI Indicator (period, overbought, oversold)
            (a) To chart this indicator with custom values of parameters, the dictionary looks as follows:
            ```
            {'name': 'rsiIndicator',
             'period': 10,
             'overbought': 30,
             'oversold': 70}
            ```

             (b) To specify just the indicator name, we can specify `rsiIndicator`. The default values for period,
             overbought, and oversold are respectively.

        7. SMA Indicator (period, valueField)
            (a) This indicator has two optional fields which can be specified as follows:
            ```
            {'name': 'smaIndicator',
             'period': 10,
             'valueField': 'value'}
            ```

            (b) Just specifying the indicator value `smaIndicator` uses the default value of period and valueField
            which are .

        8. Stochastic Indicator (kPeriod, dPeriod)
            (a) To specify the parameters of this indicator, we can provide:
            ```
            {'name': 'stochasticIndicator',
             'kPeriod': 5,
             'dPeriod': 10}
            ```

            (b) If we only specify `stochasticIndicator`, the computation is done using `kPeriod = ` and `dPeriod = `.

        9. TMA Indicator (period, valueField)
            (a) This indicator has two optional parameters:
            ```
            {'name': 'tmaIndicator',
             'period': 10,
             'valueField': 'value'}
            ```

            (b) We can also specify the indicator as a string, `tmaIndicator`, which uses period as and valueField
            as .
        """
        required_cols: list = [['open', 'Open'], ['close', 'Close'],
                               ['high', 'High'], ['low', 'Low']]
        self.verify_candlestick_data(df, required_cols)
        df = self.standardise_column_names(df, required_cols)
        current_fig_type: str = 'candle'
        if self.check_multi_axes_consistency(current_fig_type):
            self.fig_type = current_fig_type
        self.x_axis_type = 'datetime'
        self.y_axis_type = 'numeric'
        if label is None:
            label = 'Candlestick'
        candlestick_info: dict = {
            'type': 'candle',
            'xData': self.convert_datetime_to_epoch(df.index.values),
            'low': df['low'].tolist(),
            'high': df['high'].tolist(),
            'open': df['open'].tolist(),
            'close': df['close'].tolist(),
            'name': label
        }

        if animationDelay is not None:
            candlestick_info['animationDelay'] = animationDelay

        if animationDuration is not None:
            candlestick_info['animationDuration'] = animationDuration

        if indicators is not None:
            indicator: str
            indicator_info: list = []
            for indicator in indicators:
                _ = self.validate_indicator(indicator)
                indicator_name: str = self.get_indicator_name(indicator)
                indicator_info.append({
                    'seriesName': label,
                    'indicator': indicator,
                    'legendItemText': indicator_name
                })
            self.technical_indicators = indicator_info

        self.data.insert(candlestick_info)

    def validate_indicator(self, indicator: Union[str, dict]) -> bool:
        if isinstance(indicator, str):
            self.check_indicator_name(indicator)

        if isinstance(indicator, dict):
            self.check_indicator_name(indicator['name'])
            supplied_indicator_params: list = list(indicator.keys())
            supplied_indicator_params.remove('name')
            self.check_indicator_params(supplied_indicator_params)

        return True

    @staticmethod
    def get_indicator_name(indicator: Union[str, dict]) -> str:
        if isinstance(indicator, dict):
            return indicator['name']

        return indicator

    def check_indicator_name(self, indicator: str) -> bool:
        if indicator not in list(self.valid_technical_indicators.keys()):
            raise ValueError(f'{indicator} is not a valid technical indicator. Please refer to the documentation'
                             f' to get the list of supported indicators.')

        return True

    def check_indicator_params(self, params: list, name: str) -> bool:
        valid_indicator_params: list = self.valid_technical_indicators[name]
        param: str
        for param in params:
            if param not in valid_indicator_params:
                raise ValueError(f'{param} is not valid parameter for the indicator {name}. Please refer to the '
                                 f'documentation to get the list of supported indicators and parameters.')

        return True

    @staticmethod
    def verify_candlestick_data(df: pd.DataFrame, required_cols: list):
        if not isinstance(df.index[0], (pd.Timestamp, datetime.datetime)):
            raise ValueError(f'Input data frame should have datetime index.')
        req_col: list
        for req_col in required_cols:
            if (req_col[0] not in df.columns) and (req_col[1] not in df.columns):
                raise ValueError(f"Input data frame should have a column named"
                                 f" '{req_col[0]}' or '{req_col[1]}'")

    @staticmethod
    def standardise_column_names(df: pd.DataFrame,
                                 required_cols: list) -> pd.DataFrame:
        req_col: list
        for req_col in required_cols:
            df = df.rename(columns={req_col[1]: req_col[0]})

        return df

    def show(self, id: Optional[str]= None):
        id_token: str = getIdToken()
        """url: str = get_param_from_json('./identity.json', 'projectUrl') """
        if id is None:
            id = self.notebook_name
        self.collate_figure_data(id_token, id)
        try:
            #print('Connecting to ' + apiGatewayBaseUrl + '/upload')
            
            #print(self.data.to_json())
            response = requests.post(apiGatewayBaseUrl + '/upload',
                                     data=self.data.to_json(),
                                     headers={'Content-type': 'application/json', 'authorization': 'Bearer ' + id_token})
            resp = response.json()
            #print(resp)
            if 'code' in resp and resp['code'] == 401:
                return resp['message']
            
            if 'error' in resp:
                return resp['error']

            # self.db.collection(u'preview').document(str(uuid.uuid1())) #.collection('charts')
            # .document(str(uuid.uuid1())).set(data)
            return IFrame(webAppBaseUrl + '/#preview?uid=' +
                          str(resp['userId']) + '&notebookName=' +
                          id + '&chartId=' + self.chart_id, width=900, height=500)
            # return self.data.to_json()
        except ConnectionError:
            raise ConnectionError("Error in connection.")

    def collate_figure_data(self, token: str, id: str):
        self.data.add_figure_details(**{
            'category': self.fig_type,
            'type': self.axes_type,
            'title': self.title,
            'xAxisType': self.x_axis_type,
            'yAxisType': self.y_axis_type,
            'xAxisLabel': self.x_axis_label,
            'yAxisLabel': self.y_axis_label,
            'isRealTime': self.isRealTime,
            'plotBand': self.plot_band,
            'indicators': self.technical_indicators,
            'chartId': self.chart_id,
            'seqNum': self.seqNum,
            'flex': self.flex,
            'idToken': token,
            'notebookName': id,
            'xAxisProperties': self.xAxisProperties,
            'yAxisProperties': self.yAxisProperties,
            'annotations': self.annotations
        })
        self.data.add_data_to_figure()


class Group:
    def __init__(self, grp_id: Union[str, int, float],layout="carousal"):
        self.notebook_name = get_notebook_name()
        self.seqNum = 0
        if isinstance(grp_id, (int, float)):
            grp_id = str(grp_id)
        self.grp_id = grp_id
        self.layout = layout
        self.figures: list = []

    def add(self, figure: Figure):
        figure.seqNum = self.seqNum
        self.seqNum += 1
        self.figures.append(figure)

    def get_chartIds(self):
        return [{'type':'chart','id':self.grp_id}]
        #chartIds: list = []
        #for f in self.figures:
        #    chartIds.extend(f.get_chartIds())
        #return chartIds

    def show(self, id: Optional[str]= None):
        id_token: str = getIdToken()
        """baseUrl: str = get_param_from_json('./identity.json', 'projectUrl')"""
        if id is None:
            id = self.notebook_name
        figure_data: list = []
        f: Figure
        for f in self.figures:
            f.collate_figure_data(id_token, id)
            figure_data.append(f.data.to_dict())

        try:
            group_data: str = json.dumps({
                'notebookName': id,
                'grpId': self.grp_id,
                'layout':self.layout,
                'idToken': id_token,
                'data': figure_data
            })

            
            response = requests.post(apiGatewayBaseUrl + '/uploadGroup', data=group_data,
                                     headers={'Content-type': 'application/json', 'authorization': 'Bearer ' + id_token})

            resp = response.json()
            if 'code' in resp and resp['code'] == 401:
                return resp['message']
            
            if 'error' in resp:
                return resp['error']

            # self.db.collection(u'preview').document(str(uuid.uuid1())) #.collection('charts')
            # .document(str(uuid.uuid1())).set(data)
            return IFrame(webAppBaseUrl + '/#preview?uid=' + str(resp['userId']) + '&notebookName=' + id + '&layout=' + self.layout +
                          '&grpId=' + self.grp_id, width=900, height=500)
            # return self.data.to_json()
        except ConnectionError:
            return "Error in connection"


class Data:
    def __init__(self):
        # `axes` is equivalent to Matplotlib's `Axes` object.
        self.axes = []
        self.figure = {}

    def insert(self, info: dict):
        self.axes.append(info)

    def pop_last_axes(self):
        return self.axes.pop()

    def add_figure_details(self, **kwargs):
        k: str
        v: Union[str, int]
        for k, v in kwargs.items():
            self.figure[k] = v

    def add_data_to_figure(self):
        self.figure['data'] = self.axes.copy()

    def to_json(self) -> str:
        return json.dumps(self.figure, indent=4, sort_keys=True)

    def to_dict(self) -> dict:
        return self.figure


def createPost(id: str):
    """ create post from priview doc
    :param id: post  ID
    """
    if id is None:
        print("Error: No id specified")
        return

    # TODO: Move to a new class/file?
    idToken = getIdToken()

    myData: str = json.dumps({
        'cloneFromDoc': id
    })

    try:
        response = requests.post(apiGatewayBaseUrl + '/createPost', data=myData,
                                    headers={'Content-type': 'application/json', 'authorization': 'Bearer ' + idToken})
        #print(response)
        try:
            resp = response.json()
            if 'error' in resp:
                print ('Error : ' + resp['error'])
                return resp['error']
            else:
                return 'Created Post...'
        except ExceErr:
            print('Error in parsing response to json')
    except:
        print ("Error : Connection Error")

def Publish(data, id: Optional[str]= None, features: Optional[str]= None, showPreview: Optional[bool]= True):
    """This function creates priview document for a post.
    :param data: json string of chart ids e.g [{"type": "chart", "id": "html_chart"}]
    :param id: post  ID. if this method is called from Post class then it will be input parameter of post ID. If this method is called from charart js plugin this will be null and we will use notebook name as post ID.
    :param showPreview: This will decide if we should launch preview in new browser tab or not.
    """
    #TODO : check if this check covers both empty and None
    if not data:
        print("Error: No data to publish")
        return
    if id is None:
        #Id will be notebook name for jupyter notebook use case.
        id = get_notebook_name()

    # TODO: Move to a new class/file?
    idToken = getIdToken()

    myData: dict = {
        'notebookName': id,
        'ids': data
    }

    
    if features is not None:
        myData['features'] = features
    
    
    my_comm = ''
    try:
        response = requests.post(
            apiGatewayBaseUrl + '/previewPost', data=myData, headers={'authorization': 'Bearer ' + idToken})
   
        respJson = response.json()
        print(respJson)

        if 'code' in respJson and respJson['code'] == 401:
            return 'Error: ' + respJson['message']

        url = webAppBaseUrl + '/#previewPost?uid=' + str(
            respJson['userId']) + '&notebookName=' + id + '&idToken=' + idToken

        # self.db.collection(u'preview').document(str(uuid.uuid1())) #.collection('charts')
        # .document(str(uuid.uuid1())).set(data)
        #return IFrame(url, width=900, height=500)
        # Script mode
        return webAppBaseUrl + '/#previewPost?uid=' + str(
            respJson['userId']) + '&notebookName=' + id + '&idToken=<Token>'
        # return self.data.to_json()
    except:

        return "Error in connection"

class Post:
    def __init__(self, postId: str, postTitle: str = None):
        self.postId = postId
        self.postTitle = postTitle
        self.chartIds: list = []
        self.addedPostTitleInfo = False
        self.filters = None

    def addFilters(self,filters):
        self.filters = filters

    def add(self, content: Union[Figure, Group]):

        #Note : This code adds post title info. Not adding post title info inside publish method  because publish method is getting called from chart Art js plugin as well. 
        if(self.postTitle is not None and self.addedPostTitleInfo is False):
            postTitleInfo : dict = [{
                'type': 'markdown',
                'markdownType':'postTitle',
                'markdownText': self.postTitle,
                'titleText': self.postTitle,
                'isPostTitle' : True
            }]
            self.chartIds.extend(postTitleInfo)
            self.addedPostTitleInfo = True

        response = content.show(self.postId)
        self.chartIds.extend(content.get_chartIds())

    def preview(self):
        return Publish(json.dumps(self.chartIds), self.postId)

    def publish(self):
        Publish(json.dumps(self.chartIds), self.postId,json.dumps(self.filters), showPreview = False)
        return createPost(self.postId + '_preview')
         

if __name__ == '__main__':
    """ data_fn: str = 'data/dogecoin_price.csv'
    data: pd.DataFrame = pd.read_csv(data_fn)
    data.loc[:, 'Date'] = pd.to_datetime(data['Date'])

    f = Figure(title='Line Sample')
    f.line(data['Date'], data['Close'], c='g', ls='--', lw=2.0)
    f.line(data['Date'], data['Open'], c='r', ls='.-', lw=1.5)
    print(f.show()) """
