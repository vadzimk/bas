import json

from flask import jsonify, request, Response

from . import job
from .data_service import get_current_data, update_one
from ... import db
from ...models import Job


@job.route('/api/jobs')
def jobs():
    return jsonify(get_current_data())


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
    record = json.loads(request.data)
    print('record:', record)
    success = update_one(record)
    db.session.commit()
    if not success:
        return Response(status=400)
    return jsonify(get_current_data())
