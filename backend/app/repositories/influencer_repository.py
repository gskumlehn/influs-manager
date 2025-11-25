from datetime import datetime

from google.cloud import bigquery

from app.infra.database import client, get_table_id

class InfluencerRepository:
    @staticmethod
    def create(data: dict) -> dict:
        table_id = get_table_id("influencer")
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        errors = client.insert_rows_json(table_id, [data])
        if errors:
            raise Exception(f"Error inserting row: {errors}")
        return data
    
    @staticmethod
    def delete(influencer_id: int):
        query = f"DELETE FROM `{get_table_id('influencer')}` WHERE id = @id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "INT64", influencer_id)]
        )
        client.query(query, job_config=job_config).result()
        return True
    
    @staticmethod
    def find_by_campaign_id(campaign_id: int):
        query = f"SELECT * FROM `{get_table_id('influencer')}` WHERE campaign_id = @campaign_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("campaign_id", "INT64", campaign_id)]
        )
        results = client.query(query, job_config=job_config).result()
        return [dict(row) for row in results]
    
    @staticmethod
    def find_by_id(influencer_id: int):
        query = f"SELECT * FROM `{get_table_id('influencer')}` WHERE id = @id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "INT64", influencer_id)]
        )
        results = client.query(query, job_config=job_config).result()
        rows = [dict(row) for row in results]
        return rows[0] if rows else None
    
    @staticmethod
    def update(influencer_id: int, data: dict):
        data["updated_at"] = datetime.utcnow().isoformat()
        set_clause = ", ".join([f"{key} = @{key}" for key in data.keys()])
        query = f"UPDATE `{get_table_id('influencer')}` SET {set_clause} WHERE id = @id"
        params = [bigquery.ScalarQueryParameter("id", "INT64", influencer_id)]
        for key, value in data.items():
            if isinstance(value, str):
                param_type = "STRING"
            elif isinstance(value, (int, float)):
                param_type = "FLOAT64" if isinstance(value, float) else "INT64"
            else:
                param_type = "STRING"
            params.append(bigquery.ScalarQueryParameter(key, param_type, value))
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        client.query(query, job_config=job_config).result()
        return InfluencerRepository.find_by_id(influencer_id)
