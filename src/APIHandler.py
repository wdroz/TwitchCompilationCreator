from src.utils import get_headers

import config
import requests
import logging


class APIHandler:
    @staticmethod
    def get_yt_playlist_size(playlist_id: str) -> int:
        logging.info("Getting amount of playlist items")
        url = (
            f"https://www.googleapis.com/youtube/v3/playlistItems"
        )
        payload = {"part": id, "playlistId": playlist_id, "key": config.API_KEY}
        resp = requests.get(url, params=payload, headers={})
        if resp.status_code == 200:
            return resp.json()["pageInfo"]["totalResults"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")

    @staticmethod
    def get_new_twitch_token() -> str:
        logging.info("Getting new token from server")
        url = "https://id.twitch.tv/oauth2/token"
        payload = {"client_id": config.CLIENT_ID, "client_secret": config.CLIENT_SECRET,
                   "grant_type": "client_credentials"}
        resp = requests.post(url, param=payload, headers={"Client-ID": config.CLIENT_ID})
        if resp.status_code == 200:
            with open("token", "w") as outfile:
                outfile.write(resp.json()["access_token"])
            return resp.json()["access_token"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")

    @staticmethod
    def get_twitch_game_id(name: str) -> int:
        url = f"https://api.twitch.tv/helix/games"
        payload = {"name": name}
        resp = requests.get(url, params=payload, headers=get_headers())
        if resp.status_code == 200:
            return resp.json()["data"][0]["id"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")
