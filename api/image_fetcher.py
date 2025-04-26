import httpx
import asyncio

class ImageFetcher:
    async def get_random_image(self):
        url = "https://api.lolicon.app/setu/v2"
        params = {
            "num": 1,
            "r18": 0,
            "size": "regular"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                data = response.json()
                if not data["data"]:
                    raise Exception("No image found")
                image_data = data["data"][0]
                return {
                    'pid': image_data["pid"],
                    'title': image_data["title"],
                    'author': image_data["author"],
                    'url': image_data["urls"]["regular"]
                }
        except Exception as e:
            raise Exception(f"Failed to fetch image: {str(e)}")