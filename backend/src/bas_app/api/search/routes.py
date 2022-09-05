import json

from flask import request, jsonify, Response

from . import search
from ... import db
from .tasks import scrape_linkedin, get_task_state, revoke_task
from ...models import User, SearchModel


@search.route('/api/search', methods=['POST'])
def search_jobs():
    data: dict = json.loads(request.data)
    print("data", data)
    user_id = data.pop('user_id', None)
    print("form_values", data)
    print('userid', user_id)
    # TODO add field search_type
    user = User.query.get_or_404(user_id)
    linkedin_credentials = {'email': user.linkedin_email, 'password': user.linkedin_password}
    print('linkedin_credentials', linkedin_credentials)
    search_model = SearchModel(
        what=data.get('what'),
        where=data.get('where'),
        age=data.get('age'),
        radius=data.get('radius'),
        experience=data.get('experience')
    )
    db.session.add(search_model)
    db.session.commit()
    task = scrape_linkedin.s(search_fields=data, linkedin_credentials=linkedin_credentials).apply_async()
    print("task.id", task.id)
    return jsonify({'task_id': task.id, 'model_id': search_model.id}), 202


@search.route('/api/status/<task_id>')
def search_status(task_id):
    response = get_task_state(task_id)
    return jsonify(response)


@search.route('/api/revoke', methods=['POST'])
def search_revoke():
    task_id = request.get_json().get('task_id')
    revoke_task(task_id)
    new_status = get_task_state(task_id)
    if new_status['state'] == 'REVOKED':
        return Response(status=204)
    else:
        return Response(status=500)

