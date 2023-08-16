import requests
from datetime import datetime
from urllib.parse import urljoin
import hashlib
from pprint import pprint
import os
import psycopg

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
MARVEL_HOST = "http://gateway.marvel.com"
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_CONN_STRING = f"postgres://{DB_USER}:{DB_PASS}@rajje.db.elephantsql.com/jwzkbace"


def make_marvel_api_call(path, params={}):
    timestamp = str(int(datetime.now().timestamp()))
    hash = calculate_api_hash(timestamp)
    url = urljoin(MARVEL_HOST, path)
    response = requests.get(url, params={"ts": timestamp, "apikey": API_KEY, "hash": hash, **params})
    return response.json()


def calculate_api_hash(timestamp):
    datetime.now().timestamp()
    to_hash = timestamp+API_SECRET+API_KEY
    return hashlib.md5(to_hash.encode()).hexdigest()

def get_comics_ids_by_character(character):
    characters_data = make_marvel_api_call("v1/public/characters", {"name": character})
    character_id = characters_data["data"]["results"][0]["id"]
    character_comics = make_marvel_api_call(f"v1/public/characters/{character_id}/comics")
    comics_ids = [comic["id"] for comic in character_comics["data"]["results"]]
    return comics_ids

def get_characters_by_comic_id(comic_id):
    characters = []
    characters_data = make_marvel_api_call(f"v1/public/comics/{comic_id}/characters")
    for character in characters_data["data"]["results"]:
        characters.append({
            "id": character["id"],
            "name": character["name"],
            "description": character["description"],
            "picture": character["thumbnail"]["path"] + "." + character["thumbnail"]["extension"]
        })
    return characters


def get_related_characters_by_character(character):
    comic_ids = get_comics_ids_by_character("Spectrum")
    characters = {}
    for comic_id in comic_ids:
        new_characters = get_characters_by_comic_id(comic_id)
        for character in new_characters:
            if not character["id"] in characters.keys():
                characters[character["id"]] = character
    return characters

def write_characters_to_db(characters):
    with psycopg.connect(DB_CONN_STRING) as conn:
        with conn.cursor() as cur:
            for character in characters.values():
                cur.execute(
                "INSERT INTO characters VALUES (%s, %s, %s, %s)",
                (int(character["id"]), character["name"], character["description"], character["picture"]))

def _create_table():
    with psycopg.connect(DB_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(
            "CREATE TABLE characters (id int, name text, description text, picture text)")



if __name__ == "__main__":
    #_create_table()
    characters = get_related_characters_by_character("Spectrum")
    #write_characters_to_db(characters)
    pprint(characters)