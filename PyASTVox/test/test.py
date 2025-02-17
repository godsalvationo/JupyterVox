#!/usr/bin/python3

# testing file

import ast
import argparse

# help import sibling directories
import sys
sys.path.append("../vox_pyast_parser")

# load the Vox parser
from astparser import astparser
from speech import Speech
import utils

# function to parse a statement
def parse_statement(parser, stmt, verbose):
    # generate AST tree
    tree = ast.parse(stmt)

    # print the tree if verbose
    if verbose:
        utils.ast_visit(tree)

    # generate speech
    s = parser.emit(tree)

    return s

# function to read a test case from the file a test case in a file starts with a
# line of "<<<...", and ends with a line ">>>,,,".
#
# Note that this function does not check for incorrect formatting. So please
# make sure the test case file is correctly formatted.
def read_test_case(file_handle):
    # skip lines until a line of "<<<..."
    for line in file_handle:
        if line.startswith("<<<"):
           break

    # read-in the test  cases
    test_case = ""
    for line in file_handle:
        if not line.startswith(">>>"):
            test_case += line
        else:
            break

    return test_case


# parse the input
parser = argparse.ArgumentParser(description='Testing file for JupyterVox with PyAST')

parser.add_argument('-f', '--file', metavar='FILE', dest='test_case_file',
                    help='path to the test case file')

parser.add_argument('-s', '--stmt', metavar='STATEMENT', dest='stmt',
                    help='a single statement to parse')

parser.add_argument('-v', '-verbose', dest='verbose', action='store_true',
                    help='enable verbose output')

args = parser.parse_args()

if (args.test_case_file is None) and (args.stmt is None):
    print("Please specific test case file or statement")
    exit(1)

# create the parser
vox_parser = astparser()

if not args.stmt is None:
    # parse a single statement
    s = parse_statement(vox_parser, args.stmt, args.verbose)
    print("*  ", args.stmt, "=>", s.text, "\n")
else:
    # parse a test case file
    # open the file
    if args.verbose:
        print("Processing test case file:", args.test_case_file, "\n")
          
    f = open(args.test_case_file, "r")

    # generate speech for each line
    print("Generating speeches ...\n")
    file_all_parsed = False
    while not file_all_parsed:
        test_case = read_test_case(f)

        if test_case == "": # no more test cases
            break

        s = parse_statement(vox_parser, test_case, args.verbose)
    
        print(">>> Test case:\n", test_case, "=>", s.text, "\n")
        #print(s.data)

    print("\nDone.")

    f.close()
