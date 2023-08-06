import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import sys

if len(sys.argv) < 3:
    print("Usage: python chartart.py <datasetPath> <heading>")
    exit(0)

print("Creating Notebook ...")
nb = nbf.v4.new_notebook()

markdown_1 = """
# """ + sys.argv[2] + """
"""

markdown_2 = """
## Imports
"""

code_block_1 = """\
# !pip install numpy
# !pip install pandas"""

code_block_2 = """\
# Imports
import warnings
warnings.filterwarnings("ignore")

from chart.helpers import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.colors import ListedColormap"""

markdown_3 = """## Data"""

code_block_3 = """\
df = pd.read_csv(\"""" + sys.argv[1] + """\")
categorical_cols, numeric_cols = parse_columns(df)
df.head()"""

markdown_4 = """## Exploratory Data Analysis"""
markdown_5 = """### Categorical Data"""

code_block_4 = """\
eda_categorical(df, categorical_cols)\
"""
markdown_6 = """### Numeric Data"""

code_block_5 = """\
eda_numeric(df, numeric_cols)\
"""

markdown_7 = """## Correlation"""

code_block_6 = """\
corr_numeric(df, numeric_cols)\
"""

nb['cells'] = [nbf.v4.new_markdown_cell(markdown_1),
               nbf.v4.new_markdown_cell(markdown_2),
               nbf.v4.new_code_cell(code_block_1),
               nbf.v4.new_code_cell(code_block_2),
               nbf.v4.new_markdown_cell(markdown_3),
               nbf.v4.new_code_cell(code_block_3),
               nbf.v4.new_markdown_cell(markdown_4),
               nbf.v4.new_markdown_cell(markdown_5),
               nbf.v4.new_code_cell(code_block_4),
               nbf.v4.new_markdown_cell(markdown_6),
               nbf.v4.new_code_cell(code_block_5),
               nbf.v4.new_markdown_cell(markdown_7),
               nbf.v4.new_code_cell(code_block_6)
               ]


fname = '_'.join(sys.argv[2].split()) + '.ipynb'

ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=False)
ep.preprocess(nb, {'metadata': { 'path': ''}})

with open(fname, 'w') as f:
    nbf.write(nb, f)

print(fname + " created Successfully.")


