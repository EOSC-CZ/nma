# `shared` folder

This folder contains your shared packages - packages that
are used by multiple models/uis in the monorepo.

Feel free to add dependencies to `project.toml` and 
any modules to the `common` folder.

## Usage

This folder is automatically installed to the running repository
when `nrp build` or `nrp develop` is called. You can then import
the modules in your models/uis as follows:

```python
from common import my_module
```