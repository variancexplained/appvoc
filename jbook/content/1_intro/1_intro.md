---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: appvoc
  language: python
  name: python3
---
# Introduction

The global mobile application market, valued at $ 475.9 billion in 2022, is expected to reach $755.50 $billion in revenue by 2027, growing at 8.58% compound annual growth rate (CAGR) {cite}`AppWorldwideStatista`.

[[enter revenue by segment]]

Increased internet penetration, low-cost mobile data plans, and the availability and range of smartphones, tablets,  and wearable mobile devices have bolstered demand for, and availability of, gaming, entertainment, e-commerce, healthcare, and education applications. In the wake of the coronavirus (COVID-19) outbreak, social-media, gaming and entertainment-based applications led the market in downloads.

[[enter line plot downloads by segment.]]

The ubiquity of the iPhone propelled Apple to one of the most valuable companies in the world, with revenue increasing from $37.4 billion in 2008, the year the iPhone and App Store were launched, to over $394.3 billion in 2022 {cite}`AppDataReport`.

[[apple revenue]]

Apple's App Store ecosystem, host to nearly 1.8 million apps {cite}`AppDataReport`  across 70 categories, were downloaded or re-downloaded on average 1.5 billion times each week in 2022.  In all, Apple facilitated some $1.1 trillion in developer billings and sales last year {cite}`DevelopersGeneratedTrillion`, accounting for over 62% of the global revenue share in 2022.

"Companies need to prove their worth — day after day, month after month, year after year.”– Kaiser Mulla-Feroze.

Yet, failure, to put it delicately, is a fact of life for app developers. Keeping customers engaged is no easy feat. The average mobile app loses nearly 77% of its Daily Active Users (DAUs) within the first three days of installation. Ninety percent of users abandon the app after a month, and by three months 95% of users are gone. The single-use abandonment rate stands at  25%, according to Localytics {cite}`AppUninstallStatistics`.  Based upon anonymized data points from over 135 million mobilephones, losing 80% of your customer base in three days is status quo in the mobile app industry {cite}`NewDataShows`.

> 'Users try out a lot of apps but decide which ones they want to 'stop using' within the first 3-7 days. Data show that the majority of users at day 7, tend to stick around much longer.

Capturing users during that initial nascent period and retaining them over the long haul crucially requires an in-depth and nuanced understanding of the customer, her motivations, and needs at onboarding and as they evolve.

This Voice of Customer (VoC) Analysis aims to explore the nature, and quality of the Apple mobile app customer experience, to characterize the degree of satisfaction  in the mobile user base.

> “Far better an approximate answer to the right question, which is often vague, than an exact answer to the wrong question,
> which can always be made precise.” — John Tukey

The following guiding questions were designed to elicit the unknown, latent, yet high-impact/high-value, customer experience in a process of exploration and discovery.

1. What best characterizes the nature of customer opinion within the mobile app market today?
2. How can the intensity of customer opinion be understood?
3. How do opinion and customer satisfaction vary within and across mobile app categories?
4. What clusters of customer experience are revealed through the ratings and reviews.?
5. What do the reviews, ratings and rating volume reveal about app creators/developers?
6. To what degree do these data suggest unmet customer needs, and promising areas for opportunity discovery?

To this end, app, rating, and review data for 26 app categories were sampled from the Apple App Store during the period from July 15th, 2023 through August 15th 2023. Exploratory techniques and text analysis methods were employed throughout the study to harvest insight into the customer experience.  The rest of this work is organized as follows: Section 2, the **dataset overview** introduces the dataset, its methods of construction, variables, and descriptive statistics.  Section 3 covers the **data quality analysis**. The purpose of this profiling exercise was to assess the quality, correctness, structure, consistency, and suitability of the data for analysis.  Section 3 describes the **exploratory data analysis,** an depth analysis to discover trends, patterns, variable importance, and  the underlying structure of the data to verify assumptions and to gain  maximum insight from the data. Section 4 is a **sentiment analysis**, using natural language processing, text analysis, and computational  linguistics to identify, extract, and quantify customer sentiment. Section 5, **cluster analysis**, characterizes groups of customers, developers, and apps based on ratings, reviews, and common themes. Section 6 is a **collocation analysis** that reveals latent needs and topics from a quantitative analysis of the co-occurrence of words that happen more often than would be expected by chance.  Section 7 evaluates through thematic analysis, common themes, topics, ideas, and patterns of meaning that come up repeatedly in reviews. Finally, section 8, **automatic summarization** will employ AI methods for shortening a set of data computationally, to create a subset that represents the most important or relevant information within the original content.


## Dataset Overview

This effort centers around three datasets comprising data obtained from the Apple App Store during May of 2023.

| Name         | Filename       | Description                                           | Examples |
| ------------ | -------------- | ----------------------------------------------------- | -------- |
| App Overview | appdata.csv.gz | Descriptive data, price, category, rating information | 475,132  |
| App Rating   | ratings.csv.gz | Rating histogram and review counts                    | 9,999    |
| App Reviews  | reviews.csv.gz | Customer reviews                                      | 999,999  |

## Data Collection Methodology

## Structure and Organization

## Data Processing and Manipulation

## Sharing and Access

## Data Specifics
