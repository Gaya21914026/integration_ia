import httpx
from app.settings import settings

async def openrouter_chat(message: str, role: str = "user"):
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data={
        "model": settings.OPENROUTER_MODEL, 
        "messages": [
            {
                "role": role,
                "content": message
            }
        ]
    }

    async with httpx.AsyncClient() as client: 
        response = await client.post( settings.OPENROUTER_BASE_URL, 
                                      headers=headers, 
                                      json=data 
                                    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
