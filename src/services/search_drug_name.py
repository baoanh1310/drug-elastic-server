from flask import Blueprint, request
from src.model.search import *

drug = Blueprint('drug', __name__, url_prefix='/api/drug')


@drug.route('/name', methods=['POST'])
def drug_search_name():
    data = request.json
    print(data)
    size_query = 100
    if data != None and "size_query" in list(data.keys()):
        size_query = data['size_query']
    try:
        result = search_drug_with_name(
            name=data['tenThuoc'], size_query=size_query)
        return result
    except (TypeError) as e:
        raise TypeError('JSON is not serialized')


@drug.route('/match/name', methods=['POST'])
def drug_search_name_match():
    data = request.json
    print(data)
    size_query = 1
    if data != None and "size_query" in list(data.keys()):
        size_query = data['size_query']
    try:
        result = search_drug_with_name_if_match(
            name=data['tenThuoc'], size_query=size_query)
        return result
    except (TypeError) as e:
        raise TypeError('JSON is not serialized')


@drug.route('/id', methods=['POST'])
def drug_search_id():
    data = request.json
    print(data)
    size_query = 10
    if data != None and "size_query" in list(data.keys()):
        size_query = data['size_query']
    try:
        result = search_drug_with_id(
            id=data['soDangKy'], size_query=size_query)
        return result
    except (TypeError) as e:
        raise TypeError('JSON is not serialized')


@drug.route('/match/id', methods=['POST'])
def drug_search_id_match():
    data = request.json
    print(data)
    size_query = 1
    if data != None and "size_query" in list(data.keys()):
        size_query = data['size_query']
    try:
        result = search_drug_with_id_if_match(
            id=data['soDangKy'], size_query=size_query)
        return result
    except (TypeError) as e:
        raise TypeError('JSON is not serialized')


@drug.route('/multifield', methods=['POST'])
def drug_search_multifield():
    data = request.json
    print(data)
    size_query = 100
    if data != None and "size_query" in list(data.keys()):
        size_query = data['size_query']
    try:
        result = search_drug_with_multiple_field(
            text=data['text'], size_query=size_query)
        return result
    except (TypeError) as e:
        raise TypeError('JSON is not serialized')


@drug.route('/all', methods=['GET'])
def drug_all():
    result = get_all_drug(scroll_id)
    return result


@drug.route('/some', methods=['GET'])
def drug_some():
    scroll_id = request.args.get('scroll_id')
    limit = request.args.get('limit')
    print(scroll_id)
    result = get_drug(scroll_id, limit)
    return result


@drug.route('/imagepath', methods=['GET'])
def get_path():
    label = request.args.get('label')
    print(label)
    result = get_image_path(label)
    return result


@drug.route('/annotation', methods=['GET'])
def get_annotation():
    result = get_annots()
    return result
