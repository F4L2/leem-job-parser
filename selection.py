import pandas as pd
import numpy as np
from tabulate import tabulate
import sys

from static_info import *
import datamining



def pandas_df_to_markdown_table(df):
    # Dependent upon ipython
    # shamelessly stolen from https://stackoverflow.com/questions/33181846/programmatically-convert-pandas-dataframe-to-markdown-table
    from IPython.display import Markdown, display
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    #display(Markdown(df_formatted.to_csv(sep="|", index=False)))
    return Markdown(df_formatted.to_csv(sep="|", index=False))
#     return df_formatted

def df_to_markdown(df, y_index=False):
    blob = tabulate(df, headers='keys', tablefmt='pipe')
    if not y_index:
        # Remove the index with some creative splicing and iteration
        return '\n'.join(['| {}'.format(row.split('|', 2)[-1]) for row in blob.split('\n')])
    return blob



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

df = pd.DataFrame(selection, columns =['Titles', 'Link', "Department", "Time consulted"]) 

# print(tabulate(df, headers='keys', tablefmt='psql'))

### update readme.md

original_stdout = sys.stdout # Save a reference to the original standard output (stdout)
with open('readme.md', 'w') as f:
    sys.stdout = f # change stdout pointer to "readme.md"
    """ everything printed here goes into readme.md """
    print("A Web parser to browse more easily the job post for young graduate on leem.org: {}    I was consulting the fresh graduate job posting section of leem.org, while I've found some interesting jobposts, it was really annoying to browse.  So I made this little program to mine and filter junior jobposts. The results are periodically printed in a table below via a CRON that I've set to run daily.  ".format(LEEM_JEUNE_URL))
    
    
    # print(df.to_markdown(tablefmt="grid"))
    print( pandas_df_to_markdown_table(df) )

    sys.stdout = original_stdout # reset stdout
    