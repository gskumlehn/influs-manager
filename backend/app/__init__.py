from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.controllers import auth_bp, campaign_bp, company_bp, influencer_bp

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(company_bp, url_prefix="/api/companies")
    app.register_blueprint(campaign_bp, url_prefix="/api/campaigns")
    app.register_blueprint(influencer_bp, url_prefix="/api")
    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200
    return app
