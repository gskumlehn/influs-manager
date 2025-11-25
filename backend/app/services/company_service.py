from app.repositories.company_repository import CompanyRepository

class CompanyService:
    @staticmethod
    def create_company(name: str, slug: str, logo_url: str = None, 
                      primary_color: str = None, secondary_color: str = None,
                      instagram_handle: str = None):
        existing = CompanyRepository.find_by_slug(slug)
        if existing:
            return None
        data = {
            "name": name,
            "slug": slug,
            "logo_url": logo_url,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "instagram_handle": instagram_handle
        }
        return CompanyRepository.create(data)
    
    @staticmethod
    def get_all_companies():
        return CompanyRepository.find_all()
    
    @staticmethod
    def get_company_by_id(company_id: int):
        return CompanyRepository.find_by_id(company_id)
    
    @staticmethod
    def get_company_by_slug(slug: str):
        return CompanyRepository.find_by_slug(slug)
    
    @staticmethod
    def update_company(company_id: int, data: dict):
        return CompanyRepository.update(company_id, data)
