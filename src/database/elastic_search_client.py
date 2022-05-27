from elasticsearch import Elasticsearch
import pymysql
from src.config.config import *


es_client = Elasticsearch([{'host': ROOT_ADDRESS, 'port': ROOT_PORT}])
# mysql_client = pymysql.connect(host=MYSQL_HOST,
#                                user='root',
#                                password='AIOTlab2021',
#                                database='emed',
#                                charset='utf8mb4',
#                                cursorclass=pymysql.cursors.DictCursor)


def ping_es_server():
    es_client.search()


if __name__ == '__main__':
    with mysql_client:
        with mysql_client.cursor() as cursor:
            query = 'SELECT * FROM pill_images WHERE label=\'vithuoc\''
            cursor.execute(query)
            res = cursor.fetchone()
            print(res)
