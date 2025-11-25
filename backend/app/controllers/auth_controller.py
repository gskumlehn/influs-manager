from flask import Blueprint, jsonify, request

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.company_service import CompanyService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    result = AuthService.login(email, password)
    if not result:
        return jsonify({"error": "Credenciais inválidas"}), 401
    user = result["user"]
    response_data = {
        "token": result["token"],
        "user": user
    }
    if user.get("company_id"):
        company = CompanyService.get_company_by_id(user["company_id"])
        response_data["company"] = company
    return jsonify(response_data), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "client")
    company_id = data.get("company_id")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    if role not in ["admin", "client"]:
        return jsonify({"error": "Role inválido"}), 400
    user = AuthService.register(email, password, role, company_id)
    if not user:
        return jsonify({"error": "Email já cadastrado"}), 409
    return jsonify(user), 201

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token não fornecido"}), 401
    token = auth_header.split(" ")[1]
    payload = AuthService.decode_token(token)
    if not payload:
        return jsonify({"error": "Token inválido ou expirado"}), 401
    user = UserRepository.find_by_id(payload["user_id"])
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    response_data = {"user": user}
    if user.get("company_id"):
        company = CompanyService.get_company_by_id(user["company_id"])
        response_data["company"] = company
    return jsonify(response_data), 200
