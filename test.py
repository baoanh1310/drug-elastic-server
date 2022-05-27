from elasticsearch import helpers
from elasticsearch import Elasticsearch
import requests
import pymysql

ROOT_ADDRESS = '202.191.57.62'
ROOT_PORT = 9200

WORKING_INDEX = 'emed'
DRUG_TYPE = '_doc'
MAX_SIZE = 1000

es_client = Elasticsearch([{'host': ROOT_ADDRESS, 'port': ROOT_PORT}])


def get_all_drug():
    '''
        GET emed/_doc/_search
        {
        "query": {
            "match_all": {
                }
            }
        }
    '''
    query = {"size": MAX_SIZE, "query": {"match_all": {}}}
    match_docs = helpers.scan(es_client, query=query, index=WORKING_INDEX, scroll='1m', size=MAX_SIZE)
    total = 0
    docs = []
    for doc in match_docs:
        docs.append(doc['_source'])
        total += 1

    res = {"total": total, "matches": docs}
    return res


def get_drug(scroll_id='', limit=MAX_SIZE):
    query = {"size": MAX_SIZE, "query": {"match_all": {}}}
    if scroll_id == '' or scroll_id == None:
        match_docs = es_client.search(body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE, scroll='1m')
    else:
        try:
            match_docs = es_client.scroll(scroll_id=scroll_id, scroll='1m')
        except Exception:
            return {'valid': False, 'message': 'Resubmit with new scroll_id'}
    print(match_docs['_scroll_id'])
    sc_id = match_docs['_scroll_id']
    docs = match_docs['hits']['hits']
    tot = len(match_docs['hits']['hits'])

    res = {'valid': True, 'match': docs, 'total': tot, 'scroll_id': sc_id}
    return res


def ping_server():
    path = 'http://202.191.57.62:1999/api/drug/some?scroll_id=&limit=200'
    res = requests.get(path)
    data = res.json()
    print(data['match'][0])


MYSQL_HOST = '202.191.57.62'
MYSQL_PORT = 3306

MYSQL_DTB = 'emed'


# mysql_client = pymysql.connect(host=MYSQL_HOST,
#                                user='root',
#                                password='AIOTlab2021',
#                                database='emed',
#                                charset='utf8mb4',
#                                cursorclass=pymysql.cursors.DictCursor)

mysql_client = pymysql.connect(host=MYSQL_HOST,
                               user='anhduy',
                               password='anhduy0911',
                               database='emed',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    with mysql_client.cursor() as cursor:
        query = 'SELECT * FROM pill_images WHERE label=\'vithuoc\''
        cursor.execute(query)
        res = cursor.fetchall()
        urls = [row['image_url'] for row in res]
        respose = {'total': len(res), 'image_urls': urls}
        print(urls[:5])
