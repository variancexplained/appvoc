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

# Apple App Store Exploratory Data Analysis (EDA)
As of May 2023, Apple's App Store offered over 1.76 million apps across 70 categories, accounting for over 62% of the global revenue share in 2022. This iterative, yet lean, exploratory data analysis (EDA) of over 300,000 apps across 26 categories aims to discover patterns, trends and clusters of opinion, and to generate actionable, high-impact insights for opportunity discover and analysis.

> “Far better an approximate answer to the right question, which is often vague, than an exact answer to the wrong question, which can always be made precise.” — John Tukey

The EDA is guided by the following nine, intentionally vague, yet provoking questions to stimulate discovery of the unknown, latent, yet high-impact/high-value, customer experience in an iterative, and likely chaotic learning process.

1. What best characterizes the nature of customer opinion within the mobile app market today?
2. What best characterizes the intensity of customer opinion?
3. How does opinion and customer satisfaction vary within and across mobile app categories?
4. Are their clusters exposed by the nature and intensity of opinion?
5. What does the distribution of rating and rating volume reveal about app creators / developers?
6. To what degree do these data suggest unmet customer needs, and fruitfull areas for opportunity discovery?

## Datasets
This effort centers around three datasets comprising data obtained from the Apple App Store during May of 2023.

| Name         | Filename       | Description                                           | Examples     |
|--------------|----------------|-------------------------------------------------------|--------------|
| App Overview | appdata.csv.gz | Descriptive data, price, category, rating information |   475,132    |
| App Rating   | ratings.csv.gz | Rating histogram and review counts                    |       9,999  |
| App Reviews  | reviews.csv.gz | Customer reviews                                      |   999,999    |

## EDA Approach
Our analysis will traverse three stages, with three datasets, each providing progressively deeper insight into the voice of the mobile app customer.

- [Stage one](2_eda_stage_1.md) is a high-level examination of the basic product descriptive information, as well as price, average rating, rating count and developer data.
- [stage two](3_eda_stage_2.md), a subset of the data will provide review count and rating histograms of the distribution of ratings and rating counts, evincing the range and intensity of customer opinion.
- [stage three](4_eda_stage_3.md), the analysis turns qualitative as we analyze customer sentiment from reviews, vis-a-vis ratings.
