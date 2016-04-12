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
            try:
                c_int = int(c[0])
            except TypeError as e:
                c_int = 0
                print "Error for {0}, {1}: {2}".format(source_name, date, e)
            return c_int
        else:
            print "In get_source_day_total, couldn't find total documents: {0}".format(t.text)
            return 0
    except KeyError:
        print "Key error. Are you sure the source is in source_name_id.json?"
    except Exception as e:
        print "Problem getting total for {0}, {1}: {2}".format(source_name, date, e)
        return 0
