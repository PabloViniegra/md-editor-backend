from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.schemas.user import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registro de usuario
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: "Usuario creado"
        schema:
          $ref: '#/definitions/User'
      400:
        description: "Datos inválidos"
    """
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login de usuario
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: "Token de acceso"
        schema:
          properties:
            access_token:
              type: string
      401:
        description: "Credenciales inválidas"
    """
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.verify_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Obtener información del usuario autenticado
    ---
    tags:
      - auth
    responses:
      200:
        description: "Información del usuario"
        schema:
          $ref: '#/definitions/User'
      401:
        description: "No autorizado"
    """
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username}), 200
