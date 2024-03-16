### About

sbt_py is a simple python script that parses .csv files containing author metadata to generate .sbt files used by table2asn for GenBank sequence submission. 

There is currently no automated way to generate table2asn-acceptable .sbt files; this script saves you from the pain that is manually editing .sqn files with author info, and supports generating separate .sbt files for more than 1 author group (another row in the .csv file). 


### CSV prep

See example.csv for required column names.

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

### To run 

`python3 sbt_gen.py <name of .csv file> <name of sbt to be generated>`


