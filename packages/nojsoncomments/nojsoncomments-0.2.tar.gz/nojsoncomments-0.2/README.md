# nojsoncomments

nojsoncomments is a Cython extension to remove js-style comments from JSON. Trailing comma is also supported. It is a spin-off of the jstyleson package by Lin Jackson (linjackson): The comment removal code is exactly the same as in jstyleson, but being compiled as a Cython extension, it's over twice as fast. There is also no convenience wrapper. Parsing the JSON is left to the user: this package only does one thing and tries to do it well.

JSON by standard does not allow comments and trailing comma, and the python standard json module does not offer options to parse such informal JSON.

```python
import json
invalid_json_str = """{
    // Single-line comment
    "foo": "bar", // behold that trailing comma
    /*
    Multi-line comment
     */
}
"""
json.loads(invalid_json_str) # raises json.decoder.JSONDecodeError
```

nojsoncomments supports removal of:

* single-line comment
* multi-line comment
* inline comment
* trailing comma

## Installation

`pip install nojsoncomments`


## Usage

Simply like this:

```python
import nojsoncomments
valid_json_str = nojsoncomments.clean(invalid_json_str)
```

## Testing

`python setup.py test`

Note that for the extension compilation to succeed, you may have to do something like this in your shell:

`export ARCHFLAGS="-arch x86_64"`

## License

The MIT License (MIT)
Copyright (c) 2016 linjackson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
