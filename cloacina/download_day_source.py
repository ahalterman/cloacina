# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from construct_page_list import construct_page_list
from extract_from_b64 import extract_from_b64
from get_results import get_results

def download_day_source(source_name, date, source_day_total, authToken):

    iter_list = construct_page_list(source_day_total)

    results_list = []

    for p in iter_list:
        t = get_results(source_name, date, p[0], p[1], authToken)
        results_list.append(t.text)

    output_list = [] # keep outside the iter
    junk_list = []

    for t in results_list:
        soup = BeautifulSoup(t)

        for num, i in enumerate(soup.findAll("ns1:document")):
            try:
                t = i.text
#                try:
                d = extract_from_b64(t)
                output_list.append(d)
            except:
                junk_list.append(t) # error handling ¯\_(ツ)_/¯
    if junk_list:
        print "There were problems getting text from the base 64 in download_day_source. {0}".format(len(junk_list))


    output = {"stories" : output_list,
              "junk" : junk_list}
    return output
