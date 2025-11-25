from datetime import datetime

from google.cloud import bigquery

from app.infra.database import client, get_table_id

class CompanyRepository:
    @staticmethod
    def create(data: dict) -> dict:
        table_id = get_table_id("company")
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        errors = client.insert_rows_json(table_id, [data])
        if errors:
            raise Exception(f"Error inserting row: {errors}")
        return data
    
    @staticmethod
    def find_all():
        query = f"SELECT * FROM `{get_table_id('company')}`"
        results = client.query(query).result()
        return [dict(row) for row in results]
    
    @staticmethod
    def find_by_id(company_id: int):
        query = f"SELECT * FROM `{get_table_id('company')}` WHERE id = @id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "INT64", company_id)]
        )
        results = client.query(query, job_config=job_config).result()
        rows = [dict(row) for row in results]
        return rows[0] if rows else None
    
    @staticmethod
    def find_by_slug(slug: str):
        query = f"SELECT * FROM `{get_table_id('company')}` WHERE slug = @slug"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("slug", "STRING", slug)]
        )
        results = client.query(query, job_config=job_config).result()
        rows = [dict(row) for row in results]
        return rows[0] if rows else None
    
    @staticmethod
    def update(company_id: int, data: dict):
        data["updated_at"] = datetime.utcnow().isoformat()
        set_clause = ", ".join([f"{key} = @{key}" for key in data.keys()])
        query = f"UPDATE `{get_table_id('company')}` SET {set_clause} WHERE id = @id"
        params = [bigquery.ScalarQueryParameter("id", "INT64", company_id)]
        for key, value in data.items():
            param_type = "STRING" if isinstance(value, str) else "INT64"
            params.append(bigquery.ScalarQueryParameter(key, param_type, value))
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        client.query(query, job_config=job_config).result()
        return CompanyRepository.find_by_id(company_id)
