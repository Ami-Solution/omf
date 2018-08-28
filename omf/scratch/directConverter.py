'''
Convert CYMDIST .mdb or Windmil .std/.seq to GridLAB-D .glm.
Usage1: python directorConverter -std PATH_TO_F1.std -seq PATH_TO_F1.seq
Usage2: python directorConverter -mdb PATH_TO_F1.mdb
Output is written to the current working directory.
'''
from __future__ import print_function

from builtins import str
from os.path import exists, splitext, abspath
from os import getcwd
import argparse, sys
sys.path.append('../')
import milToGridlab as mil
import cymeToGridlab as cyme
import feeder
import traceback

def handleMilFile(std_path, seq_path, failure = False):
  ''' Conversion routine for the std and seq files. '''
    # Attempt to open std and seq files and convert to glm.
  try:
    with open(std_path, 'r') as std_file, open(seq_path, 'r') as seq_file:
      output_path = std_path.split('/')[-1].replace('.std', '.glm') # We wish to put the file in the current running directory.
      output_file = open(output_path, 'w')
      glm, x_scale, y_scale = mil.convert(std_file.read(), seq_file.read())
      output_file.write(feeder.sortedWrite(glm))
      print('GLM FILE WRITTEN FOR STD/SEQ COMBO.')
  except IOError:
    print('UNABLE TO WRITE GLM FILE.')
    failure = True
  except err:
    print(traceback.format_exc())
  finally:
    output_file.close()
  return failure

def handleMdbFile(mdb_path, modelDir, failure = False):
  ''' Convert mdb database to glm file. '''
  try:
    outputFname = mdb_path.split('/')[-1].replace('.mdb', '.glm')
    with open(outputFname, 'w') as output_file:
      glm, x_scale, y_scale = cyme.convertCymeModel(mdb_path, modelDir)
      output_file.write(feeder.sortedWrite(glm))
  except IOError:
    print('UNABLE TO WRITE GLM FILE.')
    failure = True
  except IndexError:
    print('INDEX ACCESSING ERROR IN CYME MODEL FUNCTION AT: ' + str(sys.exc_info()[2]))
    print(traceback.format_exc())
  except KeyError:
    print('DICTIONARY ERROR IN CYME MODEL FUNCTION AT: ' + str(sys.exc_info()[2]))
  except Exception as err:
    print(str(e))
    print(traceback.format_exc())
    failure = True
  finally:
    output_file.close()
  return failure

def is_valid_file(parser, file_name):
  ''' Check validity of user input '''
  valid_names = ["mdb", "seq", "std"]
  # Check to see that file exists. 
  if not exists(file_name):
    parser.error("FILE %s DOES NOT EXIST." % file_name)
  suffix = splitext(file_name)[1][1:]
  # Check to ensure that no invalid name is being passed.
  if suffix not in valid_names:
    parser.error("FILE SUFFIX FOR %s INVALID." % file_name)
  print("VALID MATCH CONFIRMED FOR FILE %s." % file_name)
  return file_name

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-std", help="Single std file. Must go with seq file.", type=lambda f: is_valid_file(parser, f))
  parser.add_argument("-seq", help="Single seq file. Must go with std file.", type=lambda f: is_valid_file(parser, f))
  parser.add_argument("-mdb", help="Single mdb file, with both network and database exported to the same file.", type=lambda f: is_valid_file(parser, f))
  args = parser.parse_args()
  if (args.std and args.seq):
    handleMilFile(args.std, args.seq)
  elif (args.mdb):
    home_folder = getcwd()
    handleMdbFile(args.mdb, home_folder)
  else:
    raise Exception("INVALID FILE INPUT.")

if __name__ == "__main__":
  main()
