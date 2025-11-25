from flask import Blueprint, jsonify, request

from app.services.company_service import CompanyService

company_bp = Blueprint("company", __name__)

@company_bp.route("", methods=["GET"])
def list_companies():
    companies = CompanyService.get_all_companies()
    return jsonify(companies), 200

@company_bp.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    company = CompanyService.get_company_by_id(company_id)
    if not company:
        return jsonify({"error": "Empresa não encontrada"}), 404
    return jsonify(company), 200

@company_bp.route("", methods=["POST"])
def create_company():
    data = request.get_json()
    name = data.get("name")
    slug = data.get("slug")
    if not name or not slug:
        return jsonify({"error": "Nome e slug são obrigatórios"}), 400
    company = CompanyService.create_company(
        name=name,
        slug=slug,
        logo_url=data.get("logo_url"),
        primary_color=data.get("primary_color"),
        secondary_color=data.get("secondary_color"),
        instagram_handle=data.get("instagram_handle")
    )
    if not company:
        return jsonify({"error": "Slug já existe"}), 409
    return jsonify(company), 201

@company_bp.route("/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    data = request.get_json()
    company = CompanyService.update_company(company_id, data)
    if not company:
        return jsonify({"error": "Empresa não encontrada"}), 404
    return jsonify(company), 200
