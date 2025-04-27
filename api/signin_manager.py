import json
from datetime import date

class SignInManager:
    def __init__(self, file_path="../data/signin_data.json"):
        self.file_path = file_path
        self.data = self.load_data()

    async def load_records(self):
        """异步加载签到记录"""
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def has_signed_in(self, user_id, date_str):
        # 将用户ID转换为字符串以确保一致性
        return self.data.get(str(user_id), {}).get(date_str, False)

    def record_signin(self, user_id, date_str):
        # 将用户ID转换为字符串以确保一致性
        uid = str(user_id)
        if uid not in self.data:
            self.data[uid] = {}
        self.data[uid][date_str] = True
        self.save_data()