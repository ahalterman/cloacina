import requests
import xml.etree.ElementTree as ET
import json

def authenticate(username, password):
    request = """
    <SOAP-ENV:Envelope
       xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
       SOAP-ENV:encodingStyle= "http://schemas.xmlsoap.org/soap/encoding/">
        <soap:Body xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <Authenticate xmlns="http://authenticate.authentication.services.v1.wsapi.lexisnexis.com">
            <authId>{0}</authId>
            <password>{1}</password>
          </Authenticate>
        </soap:Body>
    </SOAP-ENV:Envelope>
    """.format(username, password)

    headers = {"Host": "wskcert-www.lexisnexis.com",
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": len(request),
            "SOAPAction": "Authenticate"}

    t = requests.post(url="https://wskcert-www.lexisnexis.com/wsapi/v1/services/Authentication",
                     headers = headers,
                     data = request)

    t = t.text
    p = ET.fromstring(t)
    p = p[0][0]
    for i in p.findall('{http://authenticate.authentication.services.v1.wsapi.lexisnexis.com}binarySecurityToken'):
        return i.text
