
## Synopsis

This library provides a simple python interface to 
NASA's [Satellite Situation Center](https://sscweb.gsfc.nasa.gov/)
(SSC).  This library implements the client side of the 
[SSC RESTful web services](https://sscweb.gsfc.nasa.gov/WebServices/REST/).
For more general details about the SSC web services, see
https://sscweb.gsfc.nasa.gov/WebServices/REST/.

## Code Example

This package contains example code calling most of the available web services.
To run the included example, do the following

    python -m sscws

---

This 
["Getting Started"](https://sscweb.gsfc.nasa.gov/WebServices/REST/py/GetStarted.html) 
page contains information to help someone begin using the sscws library to 
access information from the 
[Satellite Situation Center](https://sscweb.gsfc.nasa.gov/) in a Python program.

---

Also, the following [Jupyter notebooks](https://jupyter.org/) demonstrate
different features of the library:
1. [Simple Location Example](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsExample.html) ([ipynb file](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsExample.ipynb))demonstrating a simple 3D plot of orbit information.
2. [Complex Location Example](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsBTraceExample.html) ([ipynb file](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsBTraceExample.ipynb)) requesting many values including magnetic field line tracing. This example also demonstrates how to diagnose a problem with an invalid request.
3. [Radial Conjunction With Ground Location](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsRadialConjunction.html) ([ipynb file](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsRadialConjunction.ipynb)).
4. [Magnetic Field Line Conjunction Example](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsConjunctionExample.html) ([ipynb file](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsConjunctionExample.ipynb)) with related data retrieval/plotting using [cdasws](https://pypi.org/project/cdasws/).

## Motivation

This library hides the HTTP, JSON/XML, and CDF details of the SSC web 
services. A python developer only has to deal with python objects and 
methods.

## Dependencies

At this time, the only dependency are:
1. [requests](https://pypi.org/project/requests/)
2. [numpy](https://pypi.ort/project/numpy/)
3. [matplotlib](https://pypi.org/project/matplotlib/).  This is an optional dependency.  If it is not installed, the example will simple skip plotting some data.

The critical dependencies above will automatically be installed when this 
library is.

## Installation

To install this package

    $ pip install -U sscws

or to include plotting

    $ pip install -U sscws[plot]


## API Reference

Refer to
[sscws package API reference](https://sscweb.gsfc.nasa.gov/WebServices/REST/py/sscws/index.html)

or use the standard python help mechanism.

    from sscws import SscWs
    help(SscWs)

## Tests

The tests directory contains 
[unittest](https://docs.python.org/3/library/unittest.html)
tests.

## Contributors

Bernie Harris.  
[e-mail](mailto:NASA-SPDF-Support@nasa.onmicrosoft.com) for support.

## License

This code is licensed under the 
[NASA Open Source Agreement](https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt) (NOSA).
