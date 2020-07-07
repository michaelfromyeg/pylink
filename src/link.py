'''
Script to automatically test links and log their status to a file
'''

from typing import List, NamedTuple
from enum import Enum
import csv
import sys
import getopt
import requests

# Data definitions

debug = False


class Status(Enum):
  OK = "Site is hosted here"
  DNE = "Nothing exists here"
  NOT_AUTH = "Site is secured; I don't have access"
  REDIRECT_OK = "Site redirects to ece.ubc.ca"
  REDIRECT_BAD = "Site redirects somewhere else"
  ERROR = "My Python script failed :("
  REDIRECT_OTHER = "Redirect led to some other status code"
  OTHER = "Some other status code"

class Row(NamedTuple):
  origin: str
  message: str
  status: Status

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Functions

def main(filenames: [str, str]) -> None:
  '''
  Read data, analyze it, and output it
  '''
  if (debug):
    print('Starting in debug mode...')
  input_file = filenames[0]
  output_file = filenames[1]
  generate(read(input_file), output_file)
  return None


def get_args(argv: List[str]) -> [str, str]:
  input_file = ''
  output_file = ''
  try:
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
  except getopt.GetoptError:
    print('python research.py -i <inputfile> -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('python research.py -i <inputfile> -o <outputfile>')
      sys.exit()
    elif opt in ("-i", "--input"):
      input_file = arg
    elif opt in ("-o", "--output"):
      output_file = arg
  if (debug):
    print('Input file:', input_file)
    print('Output file:', output_file)
  return [input_file, output_file]


def generate(los: List[str], output_file: str) -> None:
  lor = []  # List[str], list of rows to write to the csv file
  for s in los:
    message = ""
    status = None
    try:
      response = requests.get(s)
      if response.history:
        for resp in response.history:
            message += f'{resp.status_code} @ {resp.url}; '
        if ('ece.ubc.ca' in response.url):
          status = Status.REDIRECT_OK
        else:
          status = Status.REDIRECT_BAD
        message += f'and finally {response.status_code} @ {response.url}'
      else:
        if (response.status_code == 404):
          status = Status.DNE
        elif (response.status_code == 403):
          status = Status.NOT_AUTH
        elif (response.status_code == 200):
          status = Status.OK
        else:
          status = Status.OTHER
        message += f'{response.status_code} @ {response.url}'
    except:
      stauts = Status.ERROR
      message = "n/a"
    r = Row(origin=s, message=message, status=status)
    print(f'Done checking {s}!')
    lor.append(r)
  return write_file(lor, output_file)


def write_file(lor: List[Row], output_file: str) -> None:
  with open(f'../output/{output_file}', 'w', newline='') as o:
      writer = csv.writer(o)
      writer.writerow(['Origin', 'Result', 'Status'])
      for row in lor:
        try:
          writer.writerow([row.origin, row.message, row.status.value])
        except:
          writer.writerow([row.origin, row.message, 'ERROR'])
  return None


def read(input_file: str) -> List[str]:  # list of URLs

  # List of csv data
  los = []  # type: List[str]

  try:
    with open(f'../data/{input_file}') as csv_file:

      # Setup CSV reader
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0

      # Loop through file
      for row in csv_reader:
          # Parse headers
          if line_count == 0:
              print(f'{bcolors.WARNING}Column names are {", ".join(row)}. You should have Website (in that order); if you do not, please consult the README.md.{bcolors.ENDC}')
              line_count += 1
          # Append row to lod
          else:
              if (debug):
                print(f'{bcolors.OKBLUE}\tWebsite: {row[0]}{bcolors.ENDC}')
              s = row[0]
              los.append(s)
              line_count += 1
      print(f'{bcolors.OKGREEN}Processed {line_count} lines... now gathering research!{bcolors.ENDC}')

  # Catch bad -i value
  except FileNotFoundError:
    print(f"{bcolors.FAIL}Hmm... that file wasn't found. Make sure {input_file} exists in the data folder.{bcolors.ENDC}")
    return None

  return los


if __name__ == '__main__':
  main(get_args(sys.argv[1:]))
  print(f'{bcolors.ENDC}')  # just in case!
