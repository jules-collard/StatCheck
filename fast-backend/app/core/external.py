import aiohttp

async def get_http_session():
    async with aiohttp.ClientSession() as http_session:
        try:
            yield http_session
        except Exception:
            raise
        finally:
            await http_session.close()

async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        assert response.status == 200
        return await response.json()