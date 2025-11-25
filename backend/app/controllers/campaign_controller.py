from flask import Blueprint, jsonify, request

from app.enums.campaign_status import CampaignStatus
from app.services.campaign_service import CampaignService

campaign_bp = Blueprint("campaign", __name__)

@campaign_bp.route("", methods=["GET"])
def list_campaigns():
    company_id = request.args.get("company_id")
    if company_id:
        campaigns = CampaignService.get_campaigns_by_company(int(company_id))
    else:
        campaigns = CampaignService.get_all_campaigns()
    return jsonify(campaigns), 200

@campaign_bp.route("/<int:campaign_id>", methods=["GET"])
def get_campaign(campaign_id):
    campaign = CampaignService.get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({"error": "Campanha não encontrada"}), 404
    return jsonify(campaign), 200

@campaign_bp.route("", methods=["POST"])
def create_campaign():
    data = request.get_json()
    company_id = data.get("company_id")
    name = data.get("name")
    if not company_id or not name:
        return jsonify({"error": "company_id e name são obrigatórios"}), 400
    status_str = data.get("status", "draft")
    try:
        status = CampaignStatus(status_str)
    except ValueError:
        return jsonify({"error": "Status inválido"}), 400
    campaign = CampaignService.create_campaign(
        company_id=company_id,
        name=name,
        description=data.get("description"),
        status=status
    )
    return jsonify(campaign), 201

@campaign_bp.route("/<int:campaign_id>", methods=["PUT"])
def update_campaign(campaign_id):
    data = request.get_json()
    campaign = CampaignService.update_campaign(campaign_id, data)
    if not campaign:
        return jsonify({"error": "Campanha não encontrada"}), 404
    return jsonify(campaign), 200
