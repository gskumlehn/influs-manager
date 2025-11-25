from app.infra.database import get_session
from app.models.company import Company

class CompanyRepository:
    @staticmethod
    def create(company: Company) -> Company:
        with get_session() as session:
            session.add(company)
            session.flush()
            session.refresh(company)
            return company
    
    @staticmethod
    def find_all():
        with get_session() as session:
            companies = session.query(Company).all()
            return [c.to_dict() for c in companies]
    
    @staticmethod
    def find_by_id(company_id: int):
        with get_session() as session:
            company = session.query(Company).filter(Company.id == company_id).first()
            return company.to_dict() if company else None
    
    @staticmethod
    def find_by_slug(slug: str):
        with get_session() as session:
            company = session.query(Company).filter(Company.slug == slug).first()
            return company.to_dict() if company else None
    
    @staticmethod
    def update(company_id: int, data: dict):
        with get_session() as session:
            company = session.query(Company).filter(Company.id == company_id).first()
            if not company:
                return None
            for key, value in data.items():
                if hasattr(company, key):
                    setattr(company, key, value)
            session.flush()
            session.refresh(company)
            return company.to_dict()
