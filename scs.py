from sas7bdat import SAS7BDAT
import argparse
import re
import os
import sys

######  Support Functions

def parseType(typ ):
    """
        convert long variable types to shorterned versions
    """
    if typ == "string":
        return("C")
    elif typ == "number":
        return("N")

def parseProp(i , form , name):
    """
        Format column meta data into a printable string
    """
    RES = "{}{}{}{}{}{}".format(
        name.ljust(form["file"]),
        i.format.ljust(form["form"]),
        parseType(i.type).ljust(form["type"]),
        str(i.length).ljust(form["len"]),
        i.name.decode("utf-8").ljust(form["name"]) ,
        i.label.decode("utf-8").ljust(form["label"])
    )
    return(RES)

def getMeta(fi , form):
    """
        Open and read in a sas7bdat and return a list of its meta data as a printable string
    """
    dat = SAS7BDAT(fi)
    META = [parseProp(i , form , fi) for i in dat.columns]
    dat.close()
    return(META)

# Fomat lengths for each column to be output
form = {
    "file"  : 20,
    "form"  : 12,
    "len"   : 8,
    "name"  : 14,
    "type"  : 5,
    "label" : 10,
}


###### User Inputs

parser = argparse.ArgumentParser()

parser.add_argument(
    metavar  = "",
    nargs    = "*" ,
    dest     = "fi",
    default  = "",
    help     = "Enter name of sas7bdat dataset or expression to search for"
)

parser.add_argument ( 
    "-o" ,
    metavar  = "",
    action   = "store_const",
    const    = any ,
    dest     = "fun",
    default  = all ,
    help     = "Specify 'OR' functionality"
)

args = parser.parse_args()


###### Core Code

# If arguments are present check to see if the first one is a pattern
# I.e. doesn't end in ".sas7bdat"
pat    = [ i for i in args.fi if not re.search("\.sas7bdat$", i) ]
files  = [ i for i in args.fi if re.search("\.sas7bdat$", i) ]

# If no pattern was provided set default "ALL" pattern
if pat == []:
    pat = [""]

# Compile all the various patterns
reg = [ re.compile(i , flags = re.IGNORECASE) for i in pat  ]

# If no files have been provided generate a list of all sas files in this folder and all subdirectories
if files == [] :
    files = [ os.path.join(root,names) for root,dirs,files in os.walk("./") for names in files if names.endswith("sas7bdat")]

if files == []:
    sys.exit(0)

# Derive formatting length for file name based upon longest file name
form["file"] = len(max(files)) + 4

# Print header line
print(
        "File".ljust(form["file"]) +
        "Format".ljust(form["form"]) +
        "Type".ljust(form["type"]) +
        "Len".ljust(form["len"]) +
        "Name".ljust(form["name"]) +
        "Label".ljust(form["label"]) +
        "\n" +
        "-"*70
)

# Get a list of all variables from all desired sas7bdats
strings = [ j for i in files for j in getMeta(i, form) ]

# Filter and print strings as per the provided regex
lines = [ re.sub(r"\xa0+" , "" , i) for i in strings if args.fun(regex.search(i) for regex in reg ) ]
for line in lines:
    print(line)

