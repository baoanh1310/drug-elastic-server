import sys
sys.path.append('../')

from src.database.elastic_search_client import *
from src.config.config import *
from elasticsearch import helpers


def search_drug_with_name(name, size_query=100):
    '''
        GET emed/_doc/_search
        {
        "query": {
            "match": {
                "tenThuoc": "gena"
                }
            }
        }
    '''
    query = {"size": size_query, "query": {"match": {"tenThuoc": name}}}

    match_docs = es_client.search(
        body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE)
    if match_docs['hits']['total'] > 0:
        docs = [doc['_source'] for doc in match_docs['hits']['hits']]
        tot = match_docs['hits']['total']
        if tot > size_query:
            tot = size_query
        res = {"total": tot, "matches": docs}
        return res

    return {}


def search_drug_with_name_if_match(name, size_query=1):
    '''
        GET emed/_search 
        {
            "query": {
                "bool": 
                {
                "must": [
                    {
                    "match": { "tenThuoc": "ana" }
                    }
                ]
                }
            }
        }
    '''
    query = {
        "size": size_query,
        "query": {
            "bool":
            {
                "must": [
                    {
                        "match": {"tenThuoc.no_analyze": name}
                    }
                ]
            }
        }
    }

    match_docs = es_client.search(
        body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE)
    if match_docs['hits']['total'] > 0:
        docs = [doc['_source'] for doc in match_docs['hits']['hits']]
        tot = match_docs['hits']['total']
        if tot > size_query:
            tot = size_query
        res = {"total": tot, "matches": docs}
        return res

    return {}


def search_drug_with_id(id, size_query=10):
    '''
        GET emed/_doc/_search
        {
        "query": {
            "match": {
                "soDangKy": "gena"
                }
            }
        }
    '''
    query = {"size": size_query, "query": {"match": {"soDangKy": id}}}

    match_docs = es_client.search(
        body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE)
    if match_docs['hits']['total'] > 0:
        docs = [doc['_source'] for doc in match_docs['hits']['hits']]
        tot = match_docs['hits']['total']
        if tot > size_query:
            tot = size_query
        res = {"total": tot, "matches": docs}
        return res

    return {}


def search_drug_with_id_if_match(id, size_query=1):
    '''
        GET emed/_search 
        {
            "query": {
                "bool": 
                {
                "must": [
                    {
                    "match": { "tenThuoc": "ana" }
                    }
                ]
                }
            }
        }
    '''
    query = {
        "size": size_query,
        "query": {
            "bool":
            {
                "must": [
                    {
                        "match": {"soDangKy.no_analyze": id}
                    }
                ]
            }
        }
    }

    match_docs = es_client.search(
        body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE)
    if match_docs['hits']['total'] > 0:
        docs = [doc['_source'] for doc in match_docs['hits']['hits']]
        tot = match_docs['hits']['total']
        if tot > size_query:
            tot = size_query
        res = {"total": tot, "matches": docs}
        return res

    return {}


def search_drug_with_multiple_field(text, size_query=100):
    '''
        GET emed/_doc/_search
        {
            "query": {
                "multi_match": {
                "query": "bệnh nhân tiểu đường",
                "fields": [ "tenThuoc", "soDangKy", "chiDinh", "thanhPhan"]
                }
            }
        }
    '''
    query = {"size": size_query, "query": {"multi_match": {"query": text,
                                                           "fields": ["tenThuoc", "soDangKy", "chiDinh", "thanhPhan"]}}}

    match_docs = es_client.search(
        body=query, index=WORKING_INDEX, doc_type=DRUG_TYPE)
    if match_docs['hits']['total'] > 0:
        docs = [doc['_source'] for doc in match_docs['hits']['hits']]
        tot = match_docs['hits']['total']
        if tot > size_query:
            tot = size_query
        res = {"total": tot, "matches": docs}
        return res

    return {}


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
    query = {"size": limit, "query": {"match_all": {}}}
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


def get_image_path(label=''):
    mysql_client = pymysql.connect(host=MYSQL_HOST,
                                   user='anhduy0911',
                                   password='anhduy0911',
                                   database='emed',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor,
                                   autocommit=True)
    # mysql_client.ping(reconnect=True)
    response = {}
    isPres = False
    with mysql_client.cursor() as cursor:
        if label == '' or label == 'donthuoc':
            isPres = True
            query = f'SELECT * FROM pill_images WHERE label IS NULL'
        else:
            query = f'SELECT * FROM pill_images pi, pill p WHERE pi.pill_id = p.id AND pi.label=\'{label}\''
        cursor.execute(query)
        res = cursor.fetchall()
        if not isPres:
            urls = [{'url': row['image_url'], 'name': row['name']} for row in res]
        else:
            urls = [{'url': row['image_url'], 'name': ''} for row in res]

        response = {'total': len(res), 'image_urls': urls}

    if not bool(response):
        response = {'error': 'some response related to mysql client!'}
    mysql_client.close()
    return response


def get_annots():
    mysql_client = pymysql.connect(host=MYSQL_HOST,
                                   user='root',
                                   password='AIOTlab2021',
                                   database='emed',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor,
                                   autocommit=True)

    response = {}
    # mysql_client.ping(reconnect=True)
    with mysql_client.cursor() as cursor:
        query = f'SELECT * FROM annotation'
        cursor.execute(query)
        res = cursor.fetchall()
        response = {'total': len(res), 'matches': res}

    if not bool(response):
        response = {'error': 'some response related to mysql client!'}
    mysql_client.close()
    return response


if __name__ == '__main__':
    search_drug_with_name('gena')
