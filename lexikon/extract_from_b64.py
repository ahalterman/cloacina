from bs4 import BeautifulSoup
import json

def extract_from_b64(encoded_doc):
    #doc = base64.urlsafe_b64decode(encoded_doc)
    doc = encoded_doc.decode("base64")
    soup = BeautifulSoup(doc)
    news_source = soup.find("meta", {"name":"sourceName"})['content']
    article_title = soup.find("title").text
    publication_date = soup.find("div", {"class":"PUB-DATE"}).text
    article_body = soup.find("div", {"class":"BODY"}).text
    doc_id = soup.find("meta", {"name":"documentToken"})['content']

    data = {"news_source" : news_source,
            "publication_date_raw" : publication_date,
            "article_title" : article_title,
            "article_body" : article_body,
            "doc_id" : doc_id}

    return data
