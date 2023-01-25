import json
from typing import List

from flask import jsonify, request, Response

from . import card
from .data_service import update_search_models, get_cards_for_user
from ...models import SearchModel


@card.route('/api/cards')
def cards():
    user_id = int(request.args.get('user_id'))
    return jsonify(get_cards_for_user(user_id))


@card.route('/api/cards/', methods=['DELETE'])
def delete_cards():
    """ request.data = {"user_id":int, "model_ids": List[int]} """
    request_data = json.loads(request.data)
    print("request_data", request_data)
    user_id: int = request_data.get('user_id')
    model_ids: List[int] = request_data.get('model_ids')
    if not update_search_models(user_id, model_ids, {SearchModel.is_deleted: True}):
        return Response(f'Update {model_ids} is_deleted failed', status=400)
    return Response('OK', status=202)


