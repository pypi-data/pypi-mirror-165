# Ubicquia

Python package library for accessing the Ubicquia API. Following 12-factor app principles, the library is external dependency from the applications that requires it. This project will store in Azure but a distribuible lib is public in PyPI.

A public MD `README_PUB.md` created for descritpion in PyPI.

Create `.env` to configure project read the `.example.env` to configure.

## Build a dist

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
pip install ubicquia

# Test PyPI
twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ --no-deps ubicquia
```

## Docs

Technical docs generated with sphinx.

## Captive Portal

1. Crear SSID Open
2. Crear VLAN
3. Crear Captive Portal y configurarlo
4. Definir radio profile (2.4Ghz, 5Ghz)
5. Crear Venue y asociar los elementos anteriores.

## Ref

Create library
<https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14>
<https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f>

Install-requires-vs-requirements
<https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/>

TestPyPI
<https://packaging.python.org/en/latest/guides/using-testpypi/>
<https://packaging.python.org/en/latest/guides/using-testpypi/>

pypirc
<https://packaging.python.org/en/latest/specifications/pypirc/#pypirc>
