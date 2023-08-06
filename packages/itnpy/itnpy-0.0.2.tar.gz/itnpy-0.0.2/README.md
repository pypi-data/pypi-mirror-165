# Inverse Text Normalization

A simple, deterministic, and extensible approach to [inverse text normalization](https://www.google.com/search?q=inverse+text+normalization) (ITN) for numbers.

## Overview

This package converts raw spoken-form text (speech recognition output) into user-friendly written-form text. It works best for converting spoken numbers into numerical digits, or other translation tasks that do not change word ordering. A [csv](https://github.com/Brandhsu/itnpy/blob/master/assets/vocab.csv) file is provided to define the basic rules for transforming spoken tokens into written tokens, and extra pre/post-processing may be applied for more specific formatting requirements, i.e. dates, measurements, money, etc.

---

<div align="center">
    <img src="https://raw.githubusercontent.com/Brandhsu/itnpy/master/assets/example.png" width=60%>
</div>

<div align="center">
    These examples were produced by running this <a href="https://github.com/Brandhsu/itnpy/blob/master/scripts/docs.py">script</a>.
</div>

## Installation

This package supports Python versions >= 3.7

To install from [pypi](https://pypi.org/project/itnpy):

```shell
$ pip install itn
```

To install locally:

```shell
$ pip install -e .
```

## Tests

To run tests, use `pytest` in the root folder of this repository:

```shell
$ ls
LICENSE			assets			scripts			src
README.md		requirements.txt	setup.py		tests

$ pytest
```

## Issues

This package has been verified on a limited set of [test-cases](https://github.com/Brandhsu/itnpy/tree/master/tests/assets/). For any translation mistakes, feel free to open a pull request and update [failing.csv](https://github.com/Brandhsu/itnpy/blob/master/tests/assets/inverse_normalize_numbers/failing.csv) with the input, expected output, and mistake; thanks!

## Citation

If you find this work useful, please consider citing it.

```
@misc{hsu2022itn,
  title        = {A simple, deterministic, and extensible approach to inverse text normalization for numbers},
  author       = {Brandhsu},
  howpublished = {https://github.com/Brandhsu/itnpy},
  year         = {2022}
}
```
