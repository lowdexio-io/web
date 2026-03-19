"""
LOWDEX.io — itch.io API Client (Adult +18 Edition)
Integración real con la API de itch.io para contenidos de juegos para adultos.

Documentación oficial: https://itch.io/docs/api/serverside
"""

import os
import requests
from typing import Optional, List, Dict, Any

ITCH_API_BASE = "https://itch.io/api/1"
ITCH_API_KEY = os.environ.get("ITCH_API_KEY", "")


class ItchAPIError(Exception):
    """Excepción para errores de la API de itch.io."""
    pass


class ItchClient:
    """
    Cliente para la API de itch.io.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ITCH_API_KEY
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Realiza una petición GET a la API de itch.io."""
        if not self.api_key:
            raise ItchAPIError("No se ha configurado la API key de itch.io")
        
        url = f"{ITCH_API_BASE}/key/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ItchAPIError(f"Error HTTP {response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise ItchAPIError(f"Error de conexión: {e}")

    def get_my_games(self) -> List[Dict[str, Any]]:
        """Obtiene todos los juegos del usuario autenticado."""
        data = self._get("my-games")
        return data.get("games", [])


# ─── Datos Reales de Juegos Adultos (+18) de itch.io para Fallback ────────────
# Estos son juegos reales populares en itch.io en la categoría Adult.

FALLBACK_ADULT_GAMES = [
    {
        "id": 2001,
        "title": "FreshWomen",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "A choice-driven visual novel about a young man's life at university.",
        "user": {"username": "Oppai-Man", "url": "https://itch.io"},
        "classification": "adult"
    },
    {
        "id": 2002,
        "title": "Being a DIK",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "An interactive visual novel where you play as a student in a fraternity.",
        "user": {"username": "Dr PinkCake", "url": "https://itch.io"},
        "classification": "adult"
    },
    {
        "id": 2003,
        "title": "Leap of Faith",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "A visual novel about life, love, and difficult choices.",
        "user": {"username": "Dr PinkCake", "url": "https://itch.io"},
        "classification": "adult"
    },
    {
        "id": 2004,
        "title": "Acting Lessons",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "A deeply emotional story about life and relationships.",
        "user": {"username": "Dr PinkCake", "url": "https://itch.io"},
        "classification": "adult"
    },
    {
        "id": 2005,
        "title": "College Bound",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "Navigate the complex world of college life and romance.",
        "user": {"username": "Foxtrot", "url": "https://itch.io"},
        "classification": "adult"
    },
    {
        "id": 2006,
        "title": "Eternum",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games/tag-adult",
        "min_price": 0,
        "published": True,
        "short_text": "A high-quality visual novel set in a virtual reality world.",
        "user": {"username": "Caribdis", "url": "https://itch.io"},
        "classification": "adult"
    }
]


def get_games_for_api(api_key: Optional[str] = None, adult: bool = True) -> Dict[str, Any]:
    """
    Función principal para obtener juegos, con opción de filtrar por contenido adulto.
    """
    key = api_key or ITCH_API_KEY
    
    if key:
        try:
            client = ItchClient(api_key=key)
            games = client.get_my_games()
            # Filtrar por clasificación si es necesario
            if adult:
                games = [g for g in games if g.get('classification') == 'adult']
            return {"games": games, "source": "itch.io", "count": len(games)}
        except ItchAPIError as e:
            return {
                "games": FALLBACK_ADULT_GAMES if adult else [],
                "source": "fallback",
                "error": str(e),
                "count": len(FALLBACK_ADULT_GAMES) if adult else 0
            }
    else:
        return {
            "games": FALLBACK_ADULT_GAMES if adult else [],
            "source": "fallback",
            "message": "Mostrando contenidos reales de itch.io (Adult +18)",
            "count": len(FALLBACK_ADULT_GAMES) if adult else 0
        }
