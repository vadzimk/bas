import json
import time

from flask import request, jsonify, Response

from . import search
from ... import db
from .tasks import scrape_linkedin, get_task_state, revoke_task, scrape_indeed
from ...models import User, SearchModel, Task, Search


@search.route('/api/search', methods=['POST'])
def search_jobs():
    """ data = {user_id, job_board, *other_form_fields_specific_to_the_job_board} """
    data: dict = json.loads(request.data)
    print("data", data)
    user_id = data.pop('user_id', None)
    job_board = data.pop('job_board', None)
    print("form_values", data)
    print('userid', user_id)
    # TODO add field search_type
    user = User.query.get_or_404(user_id)
    linkedin_credentials = {'email': user.linkedin_email, 'password': user.linkedin_password}
    print('linkedin_credentials', linkedin_credentials)
    # TODO update the value of job_board in search
    experience = data.get('experience')
    if type(experience) is str:
        experience = [experience]
    elif type(experience) is list:
        pass
    else:
        return Response('experience must be str or list', status=400)
    search_model = SearchModel(
        what=data.get('what'),
        where=data.get('where'),
        age=data.get('age'),
        radius=data.get('radius'),
        experience=experience
    )
    db.session.add(search_model)
    db.session.commit()
    print("search_model.id", search_model.id)
    match job_board:
        case 'linkedin':
            task = scrape_linkedin.s(
                search_fields=data,
                linkedin_credentials=linkedin_credentials,
                user_id=user_id,
                search_model_id=search_model.id
            ).apply_async()
        case 'indeed':
            task = scrape_indeed.s(
                search_fields=data,
                user_id=user_id,
                search_model_id=search_model.id
            ).apply_async()
        case _:
            return Response("invalid job board", status=400)
    task_in_db = Task(id=task.id)
    db.session.add(task_in_db)
    db.session.commit()
    print("task.id", task.id)
    print("task_in_db.id", task_in_db.id)
    return jsonify({'task_id': task_in_db.id, 'model_id': search_model.id}), 202


@search.route('/api/status/<task_id>')
def search_status(task_id):
    response = get_task_state(task_id)
    return jsonify(response)


@search.route('/api/revoke', methods=['POST'])
def search_revoke():
    task_id = request.get_json().get('task_id')
    revoke_task(task_id)
    new_status = None
    for _ in range(9):
        time.sleep(0.5)
        new_status = get_task_state(task_id)['state']
        if new_status == 'REVOKED' or new_status == 'PENDING':
            return jsonify({
                "state": "REVOKED",
                "info": "revoked"
            })
    return Response("could not revoke", status=500)
