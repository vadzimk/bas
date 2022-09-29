import json

from flask import request, jsonify, Response

from . import filter_visibility
from .data_service import get_filtered_companies
from ... import db
from ...models import CompanyUserNote


@filter_visibility.route('/api/filter-visibility/company')
def filtered_companies():
    user_id = int(request.args.get('user_id'))
    return jsonify(get_filtered_companies(user_id))


@filter_visibility.route('/api/filter-visibility/company', methods=['PUT'])
def unfilter_company():
    request_data = json.loads(request.data)
    user_id = request_data.get('user_id')
    company_id = request_data.get('company_id')

    existing_company_user_note = db.session.query(CompanyUserNote) \
        .filter(
        CompanyUserNote.company_id == company_id,
        CompanyUserNote.user_id == user_id,
        CompanyUserNote.is_filtered == True
    ).first()
    if not existing_company_user_note:
        return Response(status=400)
    else:
        existing_company_user_note.is_filtered = False
        db.session.commit()
        return jsonify(get_filtered_companies(user_id))



