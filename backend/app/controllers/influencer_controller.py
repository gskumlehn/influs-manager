from flask import Blueprint, jsonify, request

from app.enums.influencer_status import InfluencerStatus
from app.enums.platform import Platform
from app.services.influencer_service import InfluencerService

influencer_bp = Blueprint("influencer", __name__)

@influencer_bp.route("/campaigns/<int:campaign_id>/influencers", methods=["GET"])
def list_influencers(campaign_id):
    influencers = InfluencerService.get_influencers_by_campaign(campaign_id)
    return jsonify(influencers), 200

@influencer_bp.route("/campaigns/<int:campaign_id>/influencers", methods=["POST"])
def create_influencer(campaign_id):
    data = request.get_json()
    username = data.get("username")
    platform_str = data.get("platform")
    if not username or not platform_str:
        return jsonify({"error": "username e platform são obrigatórios"}), 400
    try:
        platform = Platform(platform_str)
    except ValueError:
        return jsonify({"error": "Platform inválido"}), 400
    try:
        influencer = InfluencerService.create_influencer_from_hypeauditor(
            campaign_id=campaign_id,
            username=username,
            platform=platform
        )
        return jsonify(influencer), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@influencer_bp.route("/influencers/<int:influencer_id>", methods=["GET"])
def get_influencer(influencer_id):
    influencer = InfluencerService.get_influencer_by_id(influencer_id)
    if not influencer:
        return jsonify({"error": "Influenciador não encontrado"}), 404
    return jsonify(influencer), 200

@influencer_bp.route("/influencers/<int:influencer_id>", methods=["PUT"])
def update_influencer(influencer_id):
    data = request.get_json()
    influencer = InfluencerService.update_influencer(influencer_id, data)
    if not influencer:
        return jsonify({"error": "Influenciador não encontrado"}), 404
    return jsonify(influencer), 200

@influencer_bp.route("/influencers/<int:influencer_id>/budget", methods=["PUT"])
def update_budget(influencer_id):
    data = request.get_json()
    budget = data.get("budget")
    if budget is None:
        return jsonify({"error": "budget é obrigatório"}), 400
    influencer = InfluencerService.update_budget(influencer_id, float(budget))
    if not influencer:
        return jsonify({"error": "Influenciador não encontrado"}), 404
    return jsonify(influencer), 200

@influencer_bp.route("/influencers/<int:influencer_id>/status", methods=["PUT"])
def update_status(influencer_id):
    data = request.get_json()
    status_str = data.get("status")
    if not status_str:
        return jsonify({"error": "status é obrigatório"}), 400
    try:
        status = InfluencerStatus(status_str)
    except ValueError:
        return jsonify({"error": "Status inválido"}), 400
    influencer = InfluencerService.update_status(influencer_id, status)
    if not influencer:
        return jsonify({"error": "Influenciador não encontrado"}), 404
    return jsonify(influencer), 200

@influencer_bp.route("/influencers/<int:influencer_id>", methods=["DELETE"])
def delete_influencer(influencer_id):
    success = InfluencerService.delete_influencer(influencer_id)
    if not success:
        return jsonify({"error": "Influenciador não encontrado"}), 404
    return jsonify({"message": "Influenciador removido com sucesso"}), 200
