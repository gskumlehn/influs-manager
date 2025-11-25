import os

import requests

class HypeAuditorClient:
    BASE_URL = "https://hypeauditor.com/api/method/auditor.report/"
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_instagram_report(self, username: str) -> dict:
        url = f"{self.BASE_URL}?username={username}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_tiktok_report(self, username: str) -> dict:
        url = f"{self.BASE_URL}?username={username}&social=tiktok"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def extract_metrics(self, report_data: dict) -> dict:
        result = report_data.get("result", {})
        
        followers = result.get("followers", 0)
        aqs = result.get("audience_quality_score", 0)
        full_name = result.get("fullname", "")
        
        return {
            "followers_count": followers,
            "aqs_score": aqs,
            "full_name": full_name,
            "quality_audience": int(followers * (aqs / 100))
        }
