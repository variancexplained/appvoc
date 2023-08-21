---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: appstore
  language: python
  name: python3
---
# AppStore Rating Exploratory Data Analysis

| #  | Variable    | Description                      | Data Type   |
| -- | ----------- | -------------------------------- | ----------- |
| 1  | id          | App Identifier                   | Nominal     |
| 2  | name        | App Name                         | Nominal     |
| 3  | category_id | Four Digit Category Id           | Categorical |
| 4  | category    | Category Name                    | Categorical |
| 5  | rating      | Average Customer Rating          | Interval    |
| 6  | reviews     | Total Number Of Customer Reviews | Discrete    |
| 7  | ratings     | Rating Count                     | Discrete    |
| 8  | onestar     | One Star Rating Count            | Discrete    |
| 9  | twostar     | Two Star Rating Count            | Discrete    |
| 10 | threestar   | Three Star Rating Count          | Discrete    |
| 11 | fourstar    | Four Star Rating Count           | Discrete    |
| 12 | fivestar    | Five Star Rating Count           | Discrete    |

```{code-cell}
import os
import sys
cwd = os.getcwd()
module_path = os.path.abspath(os.path.join(cwd,"../.."))
if module_path not in sys.path:
    sys.path.append(module_path)
```

```{code-cell}
import numpy as np
import pandas as pd
from IPython.display import HTML, display_html

from appstore.data.dataset.rating import RatingDataset
from appstore.container import AppstoreContainer
formatting = {"thousands":",", "precision":2}
```

```{code-cell}
container = AppstoreContainer()
container.init_resources()
container.wire(packages=["appstore.data.dataset"])
```

### Structural Analysis

The structure and characteristics of the Rating dataset are as follows:

```{code-cell}
df1 = dataset.structure
df2 = dataset.dtypes

df1_style = df1.style.set_table_attributes("style='display:inline; margin-right:220px;'").set_caption("Dataset Structure").format(thousands=",")
df2_style = df2.style.set_table_attributes("style='display:inline; margin-right:120px'").set_caption("Dataset Data Types").format(thousands=",")

display_html(df1_style._repr_html_() + df2_style._repr_html_(), raw=True)
```

### Data Quality Analysis

Data type, cardinality, validity, duplication, and size data are summarized at the variable level.

```{code-cell}
dataset.quality.style.format(**formatting)
```

## Content Analysis

```{code-cell}
dataset.summary.style.format(**formatting)
```
