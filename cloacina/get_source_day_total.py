import re
from get_results import get_results

# logging is a hassle in multiprocessing, so use print for now. Sorry! 

def get_source_day_total(source_name, date, authToken):
    try:
        t = get_results(source_name, date, 1, 10, authToken)
        if t.status_code == 500:
            #print "There was an error. Check the log file"
            print "Error 500 from server on getting source-day total for {0} on {1}: {2}".format(source_name, date, t.text)
            return 0
        c = re.findall('">(\d+?)</ns3:documentsFound', t.text)
        if c != []:
            return c
        else:
            return 0
    except Exception as e:
        print "There was an error. Check the log file"
        print "Problem getting total for {0}, {1}: {2}".format(source_name, date, e)
        return 0
