# Python CPP Example

Test hybrid python-cpp package (an extension module).

## Instructions

1. Install:

```
pip install package_name
```

2. Import the extension module:

```python
from aesthetic_ascii import synthesize

# initialize drive object (to generate visuals)
drive = synthesize.Drive()
# generate a ASCII visual (dark_mode optional)
drive.generate(dark_mode=True)
# save to png
drive.to_png('aesthetic.png')
```

3. Call the funk