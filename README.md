### About

sbt_py is a simple python script that parses .csv files containing author metadata to generate .sbt files used by table2asn for GenBank sequence submission. 

There is currently no automated way to generate table2asn-acceptable .sbt files; this script saves you from the pain that is manually editing .sqn files with author info, and supports generating separate .sbt files for more than 1 author group (another row in the .csv file). 

**IMPORTANT**: Make sure 'Sequence_ID' is the first column in your .src file. Table2asn doesn't seem to work otherwise. 

### CSV prep

See example.csv for required column names.

#### Author name formatting:

All names should be formatted as: 
**first name** space **middle name (if supplied)** space **last name**,

Note separating each name by comma. 

#### Supported columns are 
* submission authors

* corresponding author
    * name
    * department
    * department division
    * country
    * sub-country
    * city
    * address
    * email
    * postal-code

* additional submission comment 1
* additional submission comment 2


*More columns will eventually be added; feel free to make a request*

### To run 

`python3 sbt_gen.py <name of .csv file>`


