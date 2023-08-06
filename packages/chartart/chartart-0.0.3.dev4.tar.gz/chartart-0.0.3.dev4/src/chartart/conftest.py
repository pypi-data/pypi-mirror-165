import pandas as pd


sample_token: str = 'Sample'
default_colour_map: list = ['#006ba4', '#ff800e', '#ababab', '#595959', '#5f9ed1', '#c85200', '#898989',
                            '#a2c8ec', '#ffbc79', '#cfcfcf']

x_data: list = [18, 76, 24, 12, 44, 61, 38, 53]
x_data_dt: pd.Series = pd.date_range(
    start='23/03/2021', periods=8, freq='D').to_series()
y_data: list = [100, 143, 189, 122, 176, 156, 119, 137]
data_df: pd.DataFrame = pd.DataFrame({'price': [4, 8, 12, 16, 20, 24, 28, 32],
                                      'sales': [160, 130, 110, 70, 30, 100, 90, 120],
                                      'item': ['a', 'b', 'a', 'a', 'b', 'a', 'b', 'b']})
data_df_dt: pd.DataFrame = pd.DataFrame({'date': pd.date_range(start='23/3/2021', periods=8, freq='M'),
                                         'sales': [268, 252, 231, 267, 210, 221, 246, 218]})
x_col: str = 'price'
x_col_dt: str = 'date'
y_col: str = 'sales'
c_col: str = 'item'
items: list = ['a', 'b']

bar_x_data: list = ['Low', 'Medium', 'High']
height_data: list = [50, 30, 20]
bar_data_df: pd.DataFrame = pd.DataFrame({'type': ['Low', 'Medium', 'High', 'Low', 'Medium', 'High'],
                                          'height': [25, 50, 25, 30, 40, 30],
                                          'item': ['a', 'a', 'a', 'b', 'b', 'b']})
bar_x_col: str = 'type'
height_col: str = 'height'
bar_c_col: str = 'item'
bar_items: list = ['a', 'b']
bar_item_names: list = ['Item A', 'Item B']

i: int
yr: int
box_x_data: list = [yr for yr in range(2001, 2009) for i in range(8)]
box_y_data: list = [4, 5, 6, 7, 8, 7, 6, 5, 4, 5, 1, 7, 8, 7, 6, 5, 7, 5, 6, 7, 8, 7, 
                    13, 5, 4, 5, 3, 7, 8, 7, 6, 5, 10, 5, 6, 7, 8, 7, 6, 5, 4, 5, 6, 18, 
                    8, 7, 6, 5, 4, 5, 6, 7, 8, 7, 6, 5, 3, 5, 6, 1, 8, 7, 6, 5]
box_data: pd.DataFrame = pd.DataFrame({'x': box_x_data, 'y': box_y_data})
# box_data = box_data.sample(frac=1.)
