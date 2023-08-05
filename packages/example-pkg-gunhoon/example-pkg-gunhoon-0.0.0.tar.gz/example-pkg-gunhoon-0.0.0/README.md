# Example Package

This is a simple example package.

## How to build

Make sure you have the latest versions of PyPA's `build` installed:
```bash
python3 -m pip install --upgrade build
```

Build the package by running the following command:
```bash
python3 -m build
```

This command generate two files in the `dist` directory:
```bash
example_pkg_gunhoon-0.0.1-py3-none-any.whl
example_pkg_gunhoon-0.0.1.tar.gz
```

## How to upload

Install `twine` to upload the distribution packages:
```bash
python3 -m pip install --upgrade twine
```

Run `twine` to upload all archives under `dist` directory:
```bash
python3 -m twine upload dist/*
```
