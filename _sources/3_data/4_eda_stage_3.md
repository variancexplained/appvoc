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

# Reviews

```{code-cell} ipython3
import os
import sys
sys.path.append("/home/john/projects/appstore/appstore")

import numpy as np
import pandas as pd
from IPython.display import HTML, display_html

from appstore.container import AppstoreContainer

container = AppstoreContainer()
container.init_resources()
pd.set_option("max_colwidth", 400)
```

```{code-cell} ipython3
repo = container.data.review_repo()
```

```{code-cell} ipython3
repo.summary
```

```{code-cell} ipython3
repo.info()
```

```{code-cell} ipython3
repo.sample()
```

```{code-cell} ipython3
review = repo.get(id="4937046803")
```

```{code-cell} ipython3
print(review.__str__())
```

```{code-cell} ipython3
repo.archive()
```
