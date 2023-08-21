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
# Appstore Exploratory Data Analysis

## Stage II: Rating and Review Statistics

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
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import pandas as pd
from IPython.display import HTML, display_html

from appstore.data.dataset.rating import RatingDataset
formatting = {"thousands":",", "precision":2}
```

## Structural Analysis

## Data Quality Analysis

## Content Analysis

