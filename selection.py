import pandas as pd
import numpy as np
from tabulate import tabulate
import sys
from datetime import date, datetime

from static_info import *
import datamining


selection = []



results = datamining.Data_mining()

#transform feature format
for res in results:
    for i in range(0,len(res)):
        res[i] = res[i].lower().strip()
    
    link = res[0]
    title = res[1]
    
    days_since_post = [int(s) for s in res[2].split() if s.isdigit()][0]

    city = res[3].split()[0].strip()

    try:
        department = int(res[3].split()[1][1:-1])
    except ValueError:
        #remote location
        department = res[3].split()[4][0:-1]

    fonctions = res[4]

    education = res[5]

    sector = res[6]

    contract = res[7]

    company = res[8]

    consulted = [int(s) for s in res[9].split() if s.isdigit()][0]


    ### Selection / filtering
    if days_since_post > SELECT_DAYS_SINCE_POST:
        continue

    if department not in SELECT_DEPARTMENTS:
        continue

    if fonctions not in SELECT_FONCTIONS:
        continue

    if contract not in SELECT_CONTRACTS:
        continue
    
    selection.append( np.array([title, link, department, consulted]) )



selection = np.array(selection)
selection.transpose

df = pd.DataFrame(selection, columns =['Titles', 'Link', "Department", "Consulted"]) 

# print(tabulate(df, headers='keys', tablefmt='psql'))

### update readme.md

original_stdout = sys.stdout # Save a reference to the original standard output (stdout)
with open('readme.md', 'w') as f:
    sys.stdout = f # change stdout pointer to "readme.md"
    """ everything printed here goes into readme.md """
    print("A Web parser to browse more easily the job post for young graduate on leem.org: {}.  ".format(LEEM_JEUNE_URL)) 
    print("The results are updated in the table below each working day.  ")
    
    print()
    print()

    print(df.to_markdown())

    print("  ")
    print("Last updated the {} at {}.".format(date.today(), datetime.now().strftime("%H:%M:%S")))

    sys.stdout = original_stdout # reset stdout
    
