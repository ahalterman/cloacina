import re
from get_results import get_results

def get_source_day_total(source_name, date, authToken):
    t = get_results(source_name, date, 1, 10, authToken)
    c = re.findall('">(\d+?)</ns3:documentsFound', t.text)
    if c != []:
        return c
    else:
        return 0
