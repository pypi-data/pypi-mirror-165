

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
<!-- [![forthebadge](https://forthebadge.com/images/badges/made-with-java.svg)](https://forthebadge.com) -->

<div align = center>
<a href = "github.com/plugyawn"><img width="600px" height="180px" src= "https://user-images.githubusercontent.com/76529011/185376373-787f65d5-b78b-4f11-a7fb-e9aa19dc3a04.png"></a>
</div>

-----------------------------------------
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)![Compatibility](https://img.shields.io/badge/compatible%20with-python3.9.x-blue.svg)

CMTT is a wrapper library that makes code-mixed text processing more efficient than ever. More documentation incoming!

### Installation
```
pip install code-mixed-text-toolkit
```

### Get started
How to use this library:

```Python
from code_mixed_text_toolkit.dummy import CodeMixedTextToolkit
import code_mixed_text_toolkit.data

# Dummy function
dummy = CodeMixedTextToolkit()
result = dummy.dummy_function(88)

# Data loading function
result_json = code_mixed_text_toolkit.data.load('https://world.openfoodfacts.org/api/v0/product/5060292302201.json')

# Tokenizer
text = "Hello World! This is CMTT library!"
result_tokenize = word_tokenize(text)
```

### Contributors
 - [Paras Gupta](https://github.com/paras-gupt)
 - [Tarun Sharma](https://github.com/tarun2001sharma)
 - [Reuben Devanesan](https://github.com/Reuben27)
 - [Progyan Das](https://github.com/plugyawn)
