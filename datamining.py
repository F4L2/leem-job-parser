from static_info import *

import requests
import sys
from bs4 import BeautifulSoup


def Data_mining():
    all_results = []
    PAGE = LEEM_JEUNE_URL

    ### loop over all pages
    while(PAGE):

        ### parse webpage
        html_doc = ""
        resp = requests.get( PAGE )
        if resp.ok:
            html_doc = resp.text
        else:
            sys.exit('Initial URL does not exist:  {}'.format( PAGE ))

        soup = BeautifulSoup(html_doc, 'html.parser') 


        ### loop over every job posts
        for fiche in soup.findAll("div", {"class": "fiche-teaser filet-bottom"}):
            
            link = LEEM_URL + fiche.find("h3", {"class": "fiche-title"}).find("a", href=True)['href']
            title = fiche.find("h3", {"class": "fiche-title"}).find("a").text
            meta = [line.text for line in fiche.findAll("li")]
            result = [link, title] + meta

            all_results.append( result )



        ### find next page
        next_page_address = soup.find("div", {"class": "pager-wrapper"}).find("li", {"class": "pager-next last"})

        try:
            PAGE = LEEM_URL + next_page_address.find("a", href=True)['href']
        except AttributeError:
            # reached the last page

            return all_results
