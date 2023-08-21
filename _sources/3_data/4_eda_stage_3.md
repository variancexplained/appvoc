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

```{code-cell}
import os
import sys
cwd = os.getcwd()
module_path = os.path.abspath(os.path.join(cwd,"../.."))
if module_path not in sys.path:
    sys.path.append(module_path)
```
