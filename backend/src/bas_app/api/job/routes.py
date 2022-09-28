import json

import pandas as pd
from flask import jsonify, request, Response
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL

from . import job
from .data_service import get_current_data, update_one, get_current_data_for_models, get_plan_apply, get_did_apply
from ... import db
from ...models import Job, Company, Search


def results_request_args():
    user_id = int(request.args.get('user_id'))
    models = [int(model_id) for model_id in request.args.getlist('model_id')]
    return models, user_id


@job.route('/api/jobs')
def jobs():
    return jsonify(get_current_data_for_models(*results_request_args()))


@job.route('/api/jobs', methods=['PUT'])
def update_many_jobs():
    """ currently only undo delete jobs """
    records = json.loads(request.data)
    print('records:', records)
    for rec in records:
        success = update_one(rec)
        if not success:
            return Response(status=400)
    db.session.commit()
    return jsonify(get_current_data())


@job.route('/api/job', methods=['DELETE'])
def delete_job():
    records = json.loads(request.data)
    print(records)
    db.session.query(Job) \
        .filter(Job.id.in_(tuple(records))) \
        .update({Job.is_deleted: True})
    db.session.commit()
    return jsonify(get_current_data())


@job.route('/api/job', methods=['PUT'])
def update_job():
    request_data = json.loads(request.data)
    record = request_data.get('record')
    user_id = request_data.get('user_id')
    model_ids = [int(m_id) for m_id in request_data.get('model_ids')]
    print('record:', record)
    success = update_one(record)
    db.session.commit()
    if not success:
        return Response(status=400)
    return jsonify(get_current_data_for_models(models=model_ids, user_id=user_id))


@job.route('/api/jobs/plan-apply')
def plan_apply():
    user_id = int(request.args.get('user_id'))
    return jsonify(get_plan_apply(user_id))

@job.route('/api/jobs/plan-apply', methods=['PUT'])
def update_job_plan_apply():
    request_data = json.loads(request.data)
    record = request_data.get('record')
    user_id = request_data.get('user_id')
    print('record:', record)
    success = update_one(record)
    db.session.commit()
    if not success:
        return Response(status=400)
    return jsonify(get_plan_apply(user_id))

@job.route('/api/jobs/did-apply')
def did_apply():
    user_id = int(request.args.get('user_id'))
    return jsonify(get_did_apply(user_id))

@job.route('/api/jobs/did-apply', methods=['PUT'])
def update_job_did_apply():
    request_data = json.loads(request.data)
    record = request_data.get('record')
    user_id = request_data.get('user_id')
    print('record:', record)
    success = update_one(record)
    db.session.commit()
    if not success:
        return Response(status=400)
    return jsonify(get_did_apply(user_id))
