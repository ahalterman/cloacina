import datetime


def add_entry(collection, news_source, article_title, publication_date_raw, article_body, lang, doc_id):
    toInsert = {"news_source": news_source,
                "article_title": article_title,
                "publication_date_raw": publication_date_raw,
                "date_added": datetime.datetime.utcnow(),
                "article_body": article_body,
                "stanford": 0,
                "language": lang,
                "doc_id" : doc_id}
    object_id = collection.insert(toInsert)
    return object_id


