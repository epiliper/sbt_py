import pandas as pd
from shutil import copy
import argparse
from os import path
import sys

### define args

parser = argparse.ArgumentParser(
        description = "Parses .csv files to create .sbt files for table2asn sequence record generation") 

parser.add_argument(
        'csv_loc',
        help = 'location of metadata.csv for .sqn generation'
        )

parser.add_argument(
        'name_of_sbt',
        help = 'name of .sbt to be generated'
        )

try: 
    args = parser.parse_args()
except BaseException:
        parser.print_help()
        sys.exit(0)


### text blocks used to populate .sbt file 
name_frame = """        {
          name name {
            last "last_name",
            first "first_name",
            middle "",
            initials "",
            suffix "",
            title ""            
          }
        },
"""

afil_frame = """      affil std {
        affil "afil_dept",
        div "afil_div",
        city "afil_city",
        sub "afil_sub",
        country "afil_country",
        street "afil_street",
        email "afil_email",
        postal-code "afil_postcode"
      }
"""

comment_frame = """Seqdesc ::= user {
  type str "Submission",
  data {
    {
      label str "AdditionalComment",
      data str "_alt_comment_"
    }
  }
}
"""

def generate_sbt(csv_loc, name_of_sbt):

    df = pd.read_csv(path.abspath(csv_loc))
    name_of_sbt = name_of_sbt

    ### make sure name given is valid
    
    if len(name_of_sbt) == 0:
        name_of_sbt = 'generated.sbt'

    if '.sbt' not in name_of_sbt: 
        name_of_sbt = name_of_sbt + '.sbt'


    all_cols = ['authors', 
               'afil_name',
               'afil_dept', 
               'afil_div',
               'afil_city',
               'afil_sub', 
               'afil_country',
               'afil_street',
               'afil_email',
               'afil_postcode',
               'alt_comment1',
               'alt_comment2']

    afil_cols = all_cols[2:]

    ### get information needed only for the .sbt (e.g. not strain, collection, etc.)
    sbt_info = df[all_cols]

    ### remove duplicate entries from .sbt metadata to not generate a mess of dupe .sbt's 
    sbt_info = sbt_info.drop_duplicates()

    sbt_info = sbt_info.astype('string')
    
    authors_last = []
    authors_first = []

    num_of_sbts = 0

    # for row in sbt_info.itertuples():
    for row in sbt_info.to_dict('records'):
        try: 

            [authors_last.append(last.split(' ')[1]) for last in row['authors'].split(', ')]
            [authors_first.append(first.split(' ')[0]) for first in row['authors'].split(', ')]

        except IndexError:
            print("ERROR: Author in 'authors' column is missing surname/middlename. Verify data and run again.")
            sys.exit(0)

        ### fill in affiliations
        try:
            afil_populated = afil_frame

            for col in afil_cols:
                afil_populated = afil_populated.replace(col, row[col])
            
        except TypeError:
            print(f"ERROR: missing data in required column: {col}. Enter placeholder value and run again.")
            sys.exit(0)

        ### generate dynamic filenames for more than 1 sbt

        filename = name_of_sbt

        if num_of_sbts != 0:
            filename = name_of_sbt + str(num_of_sbts)

        num_of_sbts += 1

        copy('template.sbt', filename)

        print(f"Number of sbts generated: {num_of_sbts}")

        # generate a copy of the template .sbt
        # populate it with author names, and corresponding author affiliation/contact info

        num_blocks = 0
        with open(filename, 'r+') as sbt:
            content = sbt.readlines() 

        for last, first in zip(authors_last, authors_first):
            block_to_insert = name_frame.replace("last_name", last)
            block_to_insert = block_to_insert.replace("first_name", first)

            ### if not last: replace 
            ###     }
            ### } 
            ### with            
            ###     }
            ### }, 
            if num_blocks == 0:

                block_to_insert = block_to_insert.replace("},", "}")

            content.insert(16, block_to_insert)
            num_blocks += 1

        content.insert(11, afil_populated)
        content.insert(18 + num_blocks, afil_populated)

        try:

            content[4] = content[4].replace("afil_last", row['afil_name'].split(' ')[1])
            content[5] = content[5].replace("afil_first", row['afil_name'].split(' ')[0])

        except IndexError:
            print("ERROR: Affiliated author is missing name/surname. Reenter data and run again.")
            sys.exit(0)

        with open(filename, 'w+') as sbt: 
            sbt.writelines(content)

            if row['alt_comment1']!= '':
                alt1_populated = comment_frame.replace('_alt_comment_', row['alt_comment1'])
                sbt.write(alt1_populated)

            if row['alt_comment2']!= '':
                alt2_populated = comment_frame.replace('_alt_comment_', row['alt_comment2'])
                sbt.write(alt2_populated)

generate_sbt(args.csv_loc, args.name_of_sbt)

