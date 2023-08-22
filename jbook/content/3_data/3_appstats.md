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
# Exploratory Data Analysis

## Stage II: Ratings

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

```{code-cell}
repo = container.data.rating_repo()
dataset = repo.get_dataset()
```

### Structural Analysis

The structure and characteristics of the Rating dataset are as follows:

### Data Quality Analysis

### Content Analysis
