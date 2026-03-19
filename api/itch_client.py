"""
LOWDEX.io — itch.io API Client
Integración real con la API de itch.io.

Documentación oficial: https://itch.io/docs/api/serverside

Endpoints disponibles:
  GET /api/1/KEY/credentials/info  — Información de la API key
  GET /api/1/KEY/me                — Perfil del usuario
  GET /api/1/KEY/my-games          — Juegos del usuario
  GET /api/1/KEY/game/GAME_ID/download_keys — Claves de descarga
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
    
    Uso:
        client = ItchClient(api_key="tu_api_key")
        games = client.get_my_games()
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

    def get_credentials_info(self) -> Dict[str, Any]:
        """Obtiene información sobre las credenciales actuales."""
        return self._get("credentials/info")

    def get_me(self) -> Dict[str, Any]:
        """Obtiene el perfil del usuario autenticado."""
        return self._get("me")

    def get_my_games(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los juegos del usuario autenticado.
        
        Returns:
            Lista de juegos con los campos:
            - id, title, cover_url, url
            - min_price, published, published_at
            - downloads_count, views_count, purchases_count
            - p_windows, p_linux, p_osx, p_android
            - short_text, type
        """
        data = self._get("my-games")
        return data.get("games", [])

    def get_download_keys(self, game_id: int) -> List[Dict[str, Any]]:
        """Obtiene las claves de descarga de un juego específico."""
        data = self._get(f"game/{game_id}/download_keys")
        return data.get("download_keys", [])

    def get_purchases(self, game_id: int) -> List[Dict[str, Any]]:
        """Obtiene las compras de un juego específico."""
        data = self._get(f"game/{game_id}/purchases")
        return data.get("purchases", [])


# ─── Datos de ejemplo para cuando no hay API key ──────────────────────────────

FALLBACK_GAMES = [
    {
        "id": 1001,
        "title": "Caves of Nonsense",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 0,
        "published": True,
        "short_text": "An experimental cave exploration game",
        "user": {"username": "salted_pixels", "url": "https://itch.io"}
    },
    {
        "id": 1002,
        "title": "BRDGZ",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 399,
        "published": True,
        "short_text": "A minimalist bridge-building puzzle",
        "user": {"username": "lowpoly_club", "url": "https://itch.io"}
    },
    {
        "id": 1003,
        "title": "Wander//lost",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 0,
        "published": True,
        "short_text": "A meditative exploration experience",
        "user": {"username": "moody_studio", "url": "https://itch.io"}
    },
    {
        "id": 1004,
        "title": "DATA SCULPTOR",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 0,
        "published": True,
        "short_text": "Shape data into art",
        "user": {"username": "v4p0rwave", "url": "https://itch.io"}
    },
    {
        "id": 1005,
        "title": "isometric aftermath",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 199,
        "published": True,
        "short_text": "Post-apocalyptic isometric strategy",
        "user": {"username": "grid_snap", "url": "https://itch.io"}
    },
    {
        "id": 1006,
        "title": "SIGNAL LOSS",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 0,
        "published": True,
        "short_text": "Atmospheric horror with no signal",
        "user": {"username": "noise_js", "url": "https://itch.io"}
    },
    {
        "id": 1007,
        "title": "CHROMA PEAK",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 500,
        "published": True,
        "short_text": "Neon-soaked platformer",
        "user": {"username": "neon_ghost", "url": "https://itch.io"}
    },
    {
        "id": 1008,
        "title": "monument valley.exe",
        "cover_url": "https://img.itch.zone/aW1nLzE2MDU5MjI5LnBuZw==/315x250%23c/kHFKqv.png",
        "url": "https://itch.io/games",
        "min_price": 0,
        "published": True,
        "short_text": "An impossible architecture puzzle",
        "user": {"username": "dreamware", "url": "https://itch.io"}
    }
]


def format_price(min_price: int) -> str:
    """Formatea el precio de centavos a string legible."""
    if min_price == 0:
        return "Free"
    return f"${min_price / 100:.2f}"


def get_games_for_api(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Función principal para obtener juegos.
    Usa la API real si hay API key, si no devuelve datos de ejemplo.
    """
    key = api_key or ITCH_API_KEY
    
    if key:
        try:
            client = ItchClient(api_key=key)
            games = client.get_my_games()
            return {"games": games, "source": "itch.io", "count": len(games)}
        except ItchAPIError as e:
            return {
                "games": FALLBACK_GAMES,
                "source": "fallback",
                "error": str(e),
                "count": len(FALLBACK_GAMES)
            }
    else:
        return {
            "games": FALLBACK_GAMES,
            "source": "fallback",
            "message": "Configure ITCH_API_KEY para datos reales",
            "count": len(FALLBACK_GAMES)
        }
