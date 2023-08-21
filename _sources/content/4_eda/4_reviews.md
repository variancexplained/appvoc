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

## Stage III: Reviews

```{code-cell}
import numpy as np
import pandas as pd
from IPython.display import HTML, display_html

from appstore.container import AppstoreContainer

container = AppstoreContainer()
container.init_resources()
pd.set_option("max_colwidth", 400)
```
