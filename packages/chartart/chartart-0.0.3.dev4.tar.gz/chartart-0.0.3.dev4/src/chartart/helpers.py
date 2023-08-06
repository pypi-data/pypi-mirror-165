import pandas as pd
import numpy as np
from charta.plot import Figure, Group

def parse_columns(df):
    count = len(df)
    categoricalCols = []
    numericalCols = []
    for i in np.arange(df.shape[1]):
        valueCount = df[df.columns[i]].value_counts()
        valueCount.index =  valueCount.index.map(str)
        top15 = np.sum(valueCount.to_list()[:15])
        if top15/count > 0.7:
            categoricalCols.append(df.columns[i])
        elif df.dtypes[i] in ['int64','float64']:
            numericalCols.append(df.columns[i])
    return categoricalCols, numericalCols


def eda_categorical(df, categorical_cols, grpId):
    count = len(df)
    plotList = []
    idx = 0
    g = Group(grpId=grpId)
    # TODO: The `if` is only for demo on Sep 28.
    for col in categorical_cols:
        idx = idx + 1
        if idx > 2:
            continue
        if idx == 1:
            plot_type: str = 'bar'
        else:
            plot_type: str = 'pie'
        f = Figure(chartId=str(idx) + '_' + grpId, title='EDA of categorical columns',
                   type=plot_type)
        valueCount = df[col].value_counts()
        valueCount.index =  valueCount.index.map(str)
        top5 = np.sum(valueCount.to_list()[:5])
        top15 = np.sum(valueCount.to_list()[:15])

        # if top5/count > 0.7:
        #     top_5_data: pd.Series = valueCount.iloc[:5]
        #     f.pie(top_5_data.values, top_5_data.index, c='blue')
        # elif top15/count > 0.7:
        top_15_data: pd.Series = valueCount.iloc[:15]
        if idx == 1:
            f.bar(top_15_data.index, top_15_data.values, c='green')
        else:
            f.pie(top_15_data.values, top_15_data.index)
        
        g.add(f)

    return g.show()


def eda_numeric(df, numeric_cols, chartId):
    data_idx: pd.Series = pd.Series(np.arange(1, len(df) + 1))
    line_colours: list = ['green', 'blue', 'red', 'cyan', 'magenta', 'yellow', 'black']
    f = Figure(chartId=chartId, title='EDA of numerical columns',
               type='line')
    col_name: str
    i: int
    for i, col_name in enumerate(numeric_cols):
        f.line(data_idx, df[col_name], c=line_colours[i % 7])
    return f.show()


def corr_numeric(df, numeric_cols, chartId):
    corr_df = df[numeric_cols].corr()
    f = Figure(chartId=chartId, title='Correlation table of numeric columns', type='table')
    f.table(corr_df)
    return f.show()

