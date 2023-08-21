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

## Stage One: App Performance Overview

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

+++

**Import Python Libraries and Provision Dependencies**

```{code-cell}
import os

import numpy as np
import pandas as pd
from IPython.display import HTML, display_html
import warnings
import seaborn as sns
warnings.filterwarnings(action='ignore', category=UserWarning)

import d8analysis as eda
from appstore.container import AppstoreContainer
from appstore.data.dataset.appdata import AppDataDataset
```

```{code-cell}
container = AppstoreContainer()
container.init_resources()
container.wire(packages=['appstore'])
```

**Obtain the Dataset**

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

+++

### Univariate Analysis

#### Quantitative Data

We'll begin the univariate analysis with an examination of the quantitative variables, namely:

- Average User Rating
- Rating Count
- Price
- Release Date

Using quantitative and qualititative methods, we'll discover the central tendency of the data (arithmetic mean, median, mode), its spread (variance, standard deviation, interquartile range, maximum and minimum value) and some features of its distribution (skewness, kurtosis).

##### Average User Rating

```{code-cell}
dataset.plot.pdfcdfplot(x='rating', title='Average User Rating Distribution')

```

 Since the rating scale is in [1,5], its clear that the probability density and histogram above contain apps that have not been rated. To get a sense of the actual ratings, we'll create a new dataset without the non-reviewed apps.

```{code-cell}
df = dataset.as_df()
df = df.loc[df['rating'] != 0]
rated = AppDataDataset(df=df)
```

Ok, let's examine the frequency distribution of the ratings.

```{code-cell}
rated.frequency(x='rating', bins=4)
stats = rated.describe(x='rating')
stats.numeric
rated.plot.pdfcdfplot(x='rating', bins=4, title='Distribution of User Ratings')
rated.plot.histpdfplot(x='rating', title='Distribution of User Ratings')
```

**Key Observations:**

- The long left tail reveals a tendency towards ratings in the 4-5 star range.
- Five star ratings make up 67% of all ratings.
- Multiple peaks are also observed at one star and three star ratings and to a lesser degree with two stars.
- Ratings up to one, two, and three stars, correspond to approximately 8%, 20% and 33% of the cumulative ratings respectively.
- There is no assumption of normality in the distribution of ratings.
- In short, five star ratings dominate customer opinion at this level by a significant margin.
- Note: Taking the average of ordinal values, such as user ratings, is not among the *permissible* statistical transformations whose meanings are preserved when applied to the data, according to measurement theorists, most notably, Harvard psychologist S.S Stevens, who coined the terms *nominal*, *ordinal*, *interval*, and *ratio*. Fortunately, permission is not required in data analysis

+++

##### Rating Count

Rating count can be a harbinger of the intensity of opinion. We'll use the same rated dataset as above.

```{code-cell}
stats = rated.describe(x='ratings')
stats.numeric
rated.plot.histogram(x='ratings',bins=5, title='Distribution of User Rating Count')
```

```{code-cell}
rated.top_n(x='ratings', n=10)
```

```{code-cell}
topn = np.array([10,20,35,50,75,100,200,500,1000])
rated.plot.topn_plot(x='ratings', n=topn)
```

**Key Observations:**

- The distribution of rating counts has a long right tail, with a range from 1 to nearly 31 m ratings.
- The central tendency is placed at a median of 10 ratings per app. The average is pulled in the direction of the outliers.
- Giants of big-tech, social-media, an e-commerce, such as YouTube, Tik-Tok, Spotify, WhatsApp and DoorDash are among the most rated apps in the App Store.
- The top-10 most-rated apps account for nearly 14% of all ratings and less than 1/10th of a percent of all apps. Moreover, the most-rated 1000 apps, who represent 1/3rd of a percent of all apps, consume nearly 75% of all ratings.
- Takeaway: Rating counts are vastly disproportionate.
- Note: Apps with earlier release dates may have higher rating counts. Ratings per day since release will remove the temporal dimension from the rating counts.

```{code-cell}

```

```{code-cell}
with pd.option_context('format.precision',2):
    df1_style = freq.style.set_table_attributes("style='display:inline; margin-right:220px;'").set_caption("Average User Rating Frequency Distribution")
    df2_style = desc.style.set_table_attributes("style='display:inline; margin-right:120px'").set_caption("Average User Rating Descriptive Statistics")
    display_html(df1_style._repr_html_() + df2_style._repr_html_(), raw=True)
```

**Key Observations**

- The five-star ratings represent 67% of nearly 291,000 ratings in the dataset.
- Ratings up to four-star comprise just 33% of all ratings. Three stars and below make up approximately 20% of the data; whereas, one and two star ratings represent less than 10% of all ratings.
- The mean of average user ratings, 4.09 stars, is influenced by the significant left skew. The median of 4.53 is a more robust measure of centrality, given the long left-tail in the distribution.
- The assumption of a normal distribution is violated as shown in the histogram, and the probability density functions.

+++

#### Ratings

Next, we explore the distribution of rating counts in the dataset.

```{code-cell}
p = eda.KDEPlot(data=df_ratings, x='ratings', title="Rating Count\nProbability Density Function")
h = eda.Histogram(data=df_ratings, x='ratings', title="Rating Count\nHistogram")
c = eda.ECDFPlot(data=df_ratings, x='ratings', title="Rating Count\nCumulative Distribution Function")
v = eda.ViolinPlot(data=df_ratings,x='ratings', title="Rating Count Distribution")
plots = [p]

visual = Visual()
for plot in plots:
    visual.add_plot(plot=plot)
visual.visualize()
```
