# Pyodide-HTTP

Provides patches for widely used http libraries to make them work in Pyodide environments like JupyterLite.

## Usage

```python
# 1. Install this package
import micropip
await micropip.install('pyodide-http')

# 2. Patch requests
import pyodide_http
pyodide_http.patch_requests()

# 3. Use requests
import requests
response = requests.get('https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/15946.json')
```

## How does this work?

This package applies patches to common http libraries. How the patch works depends on the package.

All requests are replaced with calls using `XMLHttpRequest`. 

### requests

When you call `requests.get` under the hood `requests.request` is called. This method initializes a `Session` as a context manager and calls its `request` method. The pyodide-http package replaces the `Session` constructor. This makes it possible to replace the `Session.request` method with a patched on.  