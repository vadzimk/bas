import asyncio
import json
import time

import celery
from flask import request, jsonify, Response

from . import search
from ... import db
from .tasks import scrape_linkedin, get_task_state, revoke_task, scrape_indeed, scrape_builtin
from ...models import User, SearchModel, Task, Search


def set_verification_code(task_id: str, pin: str):
    task = Task.query.get(task_id)
    task.verification_code = pin
    db.session.commit()


@search.route('/api/verification', methods=['POST'])
def verification():
    """handle verification request from linkedin"""
    data = json.loads(request.data)
    print("data", data)
    pin = data.get('pin')
    task_id = data.get('task_id')
    print("pin", pin)
    print("task_id", task_id)
    set_verification_code(task_id, pin)
    return Response('OK', status=200)


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
    match job_board:
        case 'linkedin':
            wanted = dict(
                {key: data.get(key) for key in ["what", "where", "age", "radius"]},
                experience=[data.get('experience')]
            )
            search_model, task = register_search_model_and_task(scrape_linkedin, data, user_id, wanted)
        case 'indeed':
            wanted = dict(
                {key: data.get(key) for key in ["what", "where", "age", "radius"]},
                experience=[data.get('experience')]
            )
            search_model, task = register_search_model_and_task(scrape_indeed, data, user_id, wanted)
        case 'builtin':
            wanted = {key: data.get(key) for key in ["what", "where", "job_category"]}
            search_model, task = register_search_model_and_task(scrape_builtin, data, user_id, wanted)
        case _:
            return Response("invalid job board", status=400)
    task_in_db = Task(id=task.id)
    db.session.add(task_in_db)
    db.session.commit()
    print("search_model.id", search_model.id)
    print("task.id", task.id)
    print("task_in_db.id", task_in_db.id)
    return jsonify({'task_id': task_in_db.id, 'model_id': search_model.id}), 202


def register_search_model_and_task(shared_task, data, user_id, wanted):
    search_model = SearchModel(**wanted)
    db.session.add(search_model)
    db.session.commit()
    task = shared_task.s(
        search_fields=dict(**wanted, limit=data.get("limit")),
        user_id=user_id,
        search_model_id=search_model.id
    ).apply_async()
    return search_model, task


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
