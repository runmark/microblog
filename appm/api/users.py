from flask import jsonify, request, url_for

from appm import db
from appm.api import bp
from appm.api.auth import token_auth
from appm.api.errors import bad_request
from appm.models import User


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    endpoint = 'api.get_users'
    data = User.to_collection_dict(User.query, page, per_page, endpoint)
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    pass


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    pass


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    # if not ('username' in data and 'email' in data and 'password' in data):
    # if any('username' not in data, 'email' not in data, 'password' not in data):
    if not set(('username', 'email', 'password')).issubset(data.keys()):
        return bad_request('must include username, email, password')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if 'username' in data and user.username != data['username'] and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and user.email != data['email'] and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different username')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
