import requests

def get_fortune():
    try:
        response = requests.get("https://jkapi.com/api/one_yan?type=json")
        if response.status_code == 200:
            data = response.json()
            return data["content"]
        return "获取运势失败，请稍后再试"
    except Exception as e:
        return f"获取运势时出错: {str(e)}"