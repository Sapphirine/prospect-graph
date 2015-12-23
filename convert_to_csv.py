#------------------------------------------------------------------
# convert_to_csv.py
#
# Desc  :  Utility to convert a plain text pipe delimited file into
#          a format that can be loaded into Neo4J using Cypher
# Author:  Janet Prumachuk
# Date  :  Nov 2015
#------------------------------------------------------------------
import sys, csv

infile  = sys.argv[1]
outfile = sys.argv[2]

with open(infile,"rb") as file_pipe:
    reader_pipe = csv.reader(file_pipe, delimiter='|', quoting=csv.QUOTE_NONE)
    with open(outfile, "wb") as file_csv:
        writer_csv = csv.writer(file_csv, delimiter="|", quoting=csv.QUOTE_NONNUMERIC)
        for row in reader_pipe:
            writer_csv.writerow(row)
