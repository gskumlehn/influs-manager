from datetime import datetime

from google.cloud import bigquery

from app.infra.database import client, get_table_id

class UserRepository:
    @staticmethod
    def create(data: dict) -> dict:
        table_id = get_table_id("user")
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        errors = client.insert_rows_json(table_id, [data])
        if errors:
            raise Exception(f"Error inserting row: {errors}")
        return data
    
    @staticmethod
    def find_by_email(email: str):
        query = f"SELECT * FROM `{get_table_id('user')}` WHERE email = @email"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
        )
        results = client.query(query, job_config=job_config).result()
        rows = [dict(row) for row in results]
        return rows[0] if rows else None
    
    @staticmethod
    def find_by_id(user_id: int):
        query = f"SELECT * FROM `{get_table_id('user')}` WHERE id = @id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "INT64", user_id)]
        )
        results = client.query(query, job_config=job_config).result()
        rows = [dict(row) for row in results]
        return rows[0] if rows else None
