# SCS - SAS Contents Scanner

Utility tool for exploring the contents of SAS7BDAT datasets. NOTE - This tool is essentially a  wrapper around the [sas7bdat](https://pypi.org/project/sas7bdat/) module made by Jared Hobbs. 

## Installation

Simply clone the repository and copy the scs bash script to your bin. 

cp ~/scs/scs  ~/bin/

If you did not clone the repository to your home area then you will need to edit the scs script to update the path to whether you have cloned the repository to. 

## Usage

Once installed you can call the script as follows: 

```
> scs ae.sas7bdat trt
File           Format      Type Len     Name          Label
----------------------------------------------------------------------
ae.sas7bdat    $           C    1       AETRTEM       Treatment Emergent
ae.sas7bdat    $           C    1       AECONTRT      Concomitant or Additional Trtmnt Given
```

All arguments that end in `.sas7bdat` are considered as datasets to be explored, all other arguments are considered as regular expressions to search for within the variable name and label. By default, multiple expressions are treated as AND conditions. If you wish to treat them as OR conditions use the `-o` argument for example:

```
> scs  -o ae.sas7bdat trt gr
File           Format      Type Len     Name          Label
----------------------------------------------------------------------
ae.sas7bdat    $           C    1       AETRTEM       Treatment Emergent
ae.sas7bdat    $           C    1       AECONTRT      Concomitant or Additional Trtmnt Given
ae.sas7bdat    $           C    3       AETOXGR       Toxicity Grade
```

If no regular expressions are provided the function will simply return all variables in the dataset. Likewise, if no datasets are specified the function will recursively scan all datasets in your current directory and below. 



