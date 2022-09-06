from flask import request, Response, jsonify

from . import user


# TODO replace user management with flask login
from ... import db
from ...models import User


@user.route('/api/user', methods=['PUT'])
def update_user():
    """
    user_details = {id, linkedin_email, linkedin_password}
    """
    user_details = request.get_json()
    print(user_details)
    user_id = user_details.get("id")
    print("user_id", user_id)
    user = User.query.get_or_404(user_id)
    # TODO add validation
    user.linkedin_email = user_details.get('linkedin_email')
    user.linkedin_password = user_details.get('linkedin_password')
    db.session.commit()
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})


@user.route('/api/user', methods=['POST'])
def create_user():
    """
    user_details = {linkedin_email, linkedin_password, username}
    """
    user_details = request.get_json()
    print(user_details)
    username = user_details['username']
    user = User.query.filter_by(username=username).first()
    if user:
        return Response(f'username "{username}" already exists', status=409)
    user = User(
        username=username,
        linkedin_email=user_details.get('linkedin_email'),
        linkedin_password=user_details.get('linkedin_password')
    )
    db.session.add(user)
    db.session.commit()
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})


@user.route('/api/user/login', methods=['POST'])
def login_user():
    """
    user_details = {username}
    """
    user_details = request.get_json()
    print("login", user_details)
    user = User.query.filter_by(username=user_details['username']).first()
    print('user:', user)
    if not user:
        return Response(status=404)
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})