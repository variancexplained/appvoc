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

## Stage I: App Performance Overview

Stage one of our exploratory data analysis aims to expose patterns and yield insight into the nature and intensity of the customer experience within the IOS app user community.

### The Dataset

The dataset contains the following product descriptive, rating, price, and developer data for some 475,132 apps from the App Store.

| #  | Variable     | Date Type  | Description                              |
| -- | ------------ | ---------- | ---------------------------------------- |
| 1  | id           | Nominal    | App Id from the App Store                |
| 2  | name         | Nominal    | App Name                                 |
| 3  | description  | Nominal    | App Description                          |
| 4  | category_id  | Nominal    | Numeric category identifier              |
| 5  | category     | Nominal    | Category name                            |
| 6  | price        | Continuous | App Price                                |
| 7  | developer_id | Nominal    | Identifier for the developer             |
| 8  | developer    | Nominal    | Name of the developer                    |
| 9  | rating       | Ordinal    | Average user rating since first released |
| 10 | ratings      | Discrete   | Number of ratings since first release    |
| 11 | released     | Continuous | Datetime of first release                |

### EDA Approach

Our exploration will comprise the following five analyses.

1. Structural Analysis: Examine the overall shape, structure, and type of the data.
2. Data Quality Analysis: Assess quality and suitability of the data in terms of missing values, outliers, duplication, cardinality, and feature values.
3. Univariate Analysis: Explore the distributions of rating count, average rating, categories, and price.
4. Bivariate Analysis: Evaluate ratings, rating count, reviews and correlation analysis between two variables.
5. Multivariate Analysis: Cluster, factor, and correspondence analysis of three or more variables simultaneously.
6. Conclusions, insights and questions for stage two.

### Preliminaries

**Import Dependencies** # noqa

```{code-cell}
import numpy as np
import pandas as pd
from IPython.display import HTML, display_html
import seaborn as sns
import d8analysis as eda

from appstore.data.dataset.appdata import AppDataDataset
from appstore.container import AppstoreContainer
```

**Wire and Initialize Dependencies** # noqa

```{code-cell}
container = AppstoreContainer()
container.init_resources()
container.wire(packages=["appstore"])
```

**Obtain the Dataset** # noqa

```{code-cell}
repo = container.data.appdata_repo()
dataset = repo.get_dataset()
```

### Structural Analysis

The structure and characteristics of the AppData dataset are as follows:

```{code-cell}
df1 = dataset.overview
df2 = dataset.dtypes

df1_style = df1.style.set_table_attributes("style='display:inline; margin-right:220px;'").set_caption("Dataset Structure")
df2_style = df2.style.set_table_attributes("style='display:inline; margin-right:120px'").set_caption("Dataset Data Types")

display_html(df1_style._repr_html_() + df2_style._repr_html_(), raw=True)
```

As indicated above, we have approximately 475,000 apps in our dataset, described by 11 features. Let's take a quick look.

```{code-cell}
dataset.sample().style.hide(axis="index")
```

Identity variables, specifically (app) id and developer_id will be retained for data processing purposes, but have no other value and will be largely ignored during this analysis.

### Data Quality Analysis

Data type, cardinality, validity, duplication, and size data are summarized at the variable level.

```{code-cell}
dataset.info.style.hide(axis="index")
```

**Observations**

- With the exception of released (date), we have no missing values.
- Id's are unique and name, description, developer information, are all high-cardinality
- Category id and label are low-cardinality with 26 unique values, each.

+++

#### Numeric Variable Data Quality

Each feature has been cast to an appropriate data type and missing data are not extant for the dataset. Valid values for the numeric variables are:

| Variable | Date Type  | Valid Values                                     |
| -------- | ---------- | ------------------------------------------------ |
| price    | Continuous | Non negative values                              |
| rating   | Interval   | Real valued in [0,5]                             |
| ratings  | Discrete   | Discrete and non-negative                        |
| released | Continuous | Datetimes between June 10, 2008 and present day. |

Let's check the ranges for these variables.

```{code-cell}
stats = dataset.describe(include=[np.number, np.datetime64])
stats.numeric[['min','max']]
```

All numeric and datetime values are within range.

#### Categorical Variable Data Quality

The id, name, description, developer_id, and developer variables are nominal, high cardinality strings. Category and category_id; in contrast, must contain one of 26 category id / category values selected for this analysis.

```{code-cell}
columns = ['category_id', 'category']
dataset.unique(columns=columns).style.hide(axis="index")
```

Category and category_id values are as expected.
