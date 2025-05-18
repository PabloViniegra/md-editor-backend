from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.post import Post
from app.schemas.post import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

posts_bp = Blueprint('posts', __name__)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@posts_bp.route("/", methods=["POST"])
@jwt_required()
def create_post():
    """
    Crear un nuevo post
    ---
    tags:
      - posts
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
            - content
          properties:
            title:
              type: string
            content:
              type: string
    responses:
      201:
        description: "Post creado"
        schema:
          $ref: '#/definitions/Post'
    """
    user_id = int(get_jwt_identity())
    data = request.json
    post = Post(
        title=data["title"],
        content=data["content"],
        user_id=user_id
    )
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post), 201


@posts_bp.route("/", methods=["GET"])
@jwt_required()
def list_posts():
    """
    Listar posts del usuario
    ---
    tags:
      - posts
    security:
      - Bearer: []
    parameters:
      - in: query
        name: search
        type: string
        description: "Término a buscar en el título"
      - in: query
        name: order_by
        type: string
        description: "Campo para ordenar (default: created_at)"
    responses:
      200:
        description: "Lista de posts"
        schema:
          type: array
          items:
            $ref: '#/definitions/Post'
    """
    user_id = int(get_jwt_identity())
    q = Post.query.filter_by(user_id=user_id)

    term = request.args.get('search')
    order = request.args.get('order_by', 'created_at')
    if term:
        q = q.filter(Post.title.ilike(f"%{term}%"))
    if hasattr(Post, order):
        column = getattr(Post, order)
    else:
        column = Post.created_at
    q = q.order_by(column.desc())
    return posts_schema.jsonify(q.all()), 200


@posts_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_post(id):
    """
    Obtener un post por ID
    ---
    tags:
      - posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: "ID del post a recuperar"
    responses:
      200:
        description: Datos del post
        schema:
          $ref: '#/definitions/Post'
      404:
        description: "Post no encontrado para el usuario autenticado"
    """
    user_id = int(get_jwt_identity())
    post = Post.query.filter_by(id=id, user_id=user_id).first_or_404()
    return post_schema.jsonify(post), 200


@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    """
    Actualizar un post existente
    ---
    tags:
      - posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
        description: ID del post a actualizar
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
              description: Nuevo título (opcional)
            content:
              type: string
              description: Nuevo contenido (opcional)
    responses:
      200:
        description: Post actualizado
        schema:
          $ref: '#/definitions/Post'
      404:
        description: Post no encontrado para el usuario autenticado
      400:
        description: Datos de entrada inválidos
    """
    user_id = int(get_jwt_identity())
    post = Post.query.filter_by(id=post_id, user_id=user_id).first_or_404()
    data = request.json
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()
    return post_schema.jsonify(post), 200


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    """
    Eliminar un post
    ---
    tags:
      - posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
        description: ID del post a eliminar
    responses:
      200:
        description: Mensaje de confirmación
        schema:
          properties:
            message:
              type: string
              example: Post deleted
      404:
        description: Post no encontrado para el usuario autenticado
    """
    user_id = int(get_jwt_identity())
    post = Post.query.filter_by(id=post_id, user_id=user_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200
