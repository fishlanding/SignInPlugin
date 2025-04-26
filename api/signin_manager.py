import json
import os
import datetime
import asyncio

class SignInManager:
    def __init__(self):
        self.records_file = "plugins/SignInPlugin/data/signins.json"
        self.records = {}

    async def load_records(self):
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
        except Exception as e:
            print(f"Error loading sign-in records: {e}")

    async def save_records(self):
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving sign-in records: {e}")

    def has_signed_in(self, user_id: str, date: str) -> bool:
        return user_id in self.records and self.records[user_id].get('last_signin') == date

    def record_signin(self, user_id: str, date: str):
        self.records[user_id] = {
            'last_signin': date,
            'total_signins': self.records.get(user_id, {}).get('total_signins', 0) + 1
        }
        asyncio.create_task(self.save_records())