# -*- coding: utf-8 -*-
import requests
import re
import json

with open('source_name_id.json') as source_file:    
    source_dict = json.load(source_file)

def get_results(source_name, date, start_result, end_result, authToken):
    #searchterm = "a OR an OR the"
    searchterm = "a"
    if re.search("Arabic", source_name):
        searchterm = u"أن OR من OR هذا OR أن OR يا"
        print searchterm

    source = source_dict[source_name]

    req = """<SOAP-ENV:Envelope
       xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
       SOAP-ENV:encodingStyle= "http://schemas.xmlsoap.org/soap/encoding/">
        <soap:Body xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <Search xmlns="http://search.search.services.v1.wsapi.lexisnexis.com">
       <binarySecurityToken>{authToken}</binarySecurityToken>
       <sourceInformation>
        <ns1:sourceIdList xmlns:ns1="http://common.search.services.v1.wsapi.lexisnexis.com">
         <ns2:sourceId xmlns:ns2="http://common.services.v1.wsapi.lexisnexis.com">{source}</ns2:sourceId>
        </ns1:sourceIdList>
       </sourceInformation>
       <query>{searchterm}</query>
       <projectId>8412</projectId>
       <searchOptions>
        <ns3:dateRestriction xmlns:ns3="http://common.search.services.v1.wsapi.lexisnexis.com">
         <ns3:startDate>{date}</ns3:startDate>
         <ns3:endDate>{date}</ns3:endDate>
        </ns3:dateRestriction>
       </searchOptions>
       <retrievalOptions>
        <ns4:documentView xmlns:ns4="http://result.common.services.v1.wsapi.lexisnexis.com">FullText</ns4:documentView>
        <ns5:documentMarkup xmlns:ns5="http://result.common.services.v1.wsapi.lexisnexis.com">Display</ns5:documentMarkup>
        <ns6:documentRange xmlns:ns6="http://result.common.services.v1.wsapi.lexisnexis.com">
         <ns6:begin>{start_result}</ns6:begin>
         <ns6:end>{end_result}</ns6:end>
        </ns6:documentRange>
       </retrievalOptions>
      </Search>
    </soap:Body>
    </SOAP-ENV:Envelope>""".format(authToken = authToken, date = date, source = source, searchterm = searchterm, start_result = start_result, end_result = end_result)

    headers = {"Host": "www.lexisnexis.com",
                "Content-Type": "text/xml; charset=UTF-8",
                "Content-Length": len(req),
                "Origin" : "http://www.lexisnexis.com",
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
                "SOAPAction": "Search"}

    try:
        t = requests.post(url = "http://www.lexisnexis.com/wsapi/v1/services/Search",
                         headers = headers,
                         data = req)
        return t
    
    except Exception as e:
        print "Problem in `get_results` for {0} on {1}: {2}".format(source_name, date, e)

if __name__ == "__main__":
    auth =  "" # put in fresh authToken before using
    t = get_results("New York Times", "2015-09-01", 1, 10, auth)
    print t.text
