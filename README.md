# site-tester

Another Python project to automate stuff I'm too lazy to do by hand.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Requirements

- Python
- Data, in the form a csv file

Example CSV data:

```csv
Website
https://ece.ubc.ca/~fvogt/
https://ece.ubc.ca/~ivanov/
```

Virtual environment quickstart (for Windows):

```bash
pip install virtualenv
virtualenv env
source ./env/Scripts/active
pip install -r requirements.txt
pip freeze > requirements.txt
```

## Usage

Run `python link.py -i <input file> -o <output file>`, where 'input file' is the name of a CSV file containing professor names. See `research.py` for more information on the anticipated structure of the CSV data.

### Example

Here's an example console call:

TBD

## Future

TBD
