import json
import os
import tkinter as tk
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# precisa dessas infos de auth do hoyolab, user_id e os 2 token de cookies
USER_ID = os.getenv("USER_ID")
LTOKEN_V2 = os.getenv("LTOKEN_V2")
LTUID_V2 = os.getenv("LTUID_V2")
TOKEN = f"ltoken_v2={LTOKEN_V2};ltuid_v2={LTUID_V2};"

URL_LIST_BASE: str = "https://sg-act-nap-api.hoyolab.com"
URL_LIST_BASE_PARAMS: str = (
    "/event/game_record_zzz/api/zzz/avatar/basic?server=prod_gf_us&role_id="
)
URL_CHAR_DATA: str = (
    "https://sg-act-nap-api.hoyolab.com/event/"
    "game_record_zzz/api/zzz/avatar/info?id_list[]="
)
URL_CHAR_PARAM: str = "&need_wiki=true&server=prod_gf_us&role_id="

HEADERS = {
    "Cookie": TOKEN,
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    ),
    "Referer": "https://act.hoyolab.com/",
    "Origin": "https://act.hoyolab.com",
}


def load_chars_data() -> list:
    resquested_chars_id: dict = _request_json(
        f"{URL_LIST_BASE}{URL_LIST_BASE_PARAMS}{USER_ID}"
    )
    chars_id: dict = resquested_chars_id["data"]["avatar_list"]
    chars_data: list = _request_chars_data(chars_id)
    return chars_data


def _request_json(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=5)
    return json.loads(resp.text)


def _request_chars_data(json_chars: dict) -> list:
    char_json_list: list = []
    for char_name in json_chars:
        url = f'{URL_CHAR_DATA}{str(char_name["id"])}{URL_CHAR_PARAM}{USER_ID}'
        print(f'load data -> {char_name["full_name_mi18n"]}', end='... ')
        json_aux = _request_json(url)
        char_json_list.append(json_aux)
        print("Success!")
    return char_json_list


def write_files(chars_data: list) -> None:
    file_name = "hoyolab_character.json"
    with open(f'{os.getcwd()}{os.sep}{file_name}', "w", encoding="UTF-8") as file:
        file.write(json.dumps(chars_data, indent=4))

    print(f"{file_name} saved!")


def show_done_message():
    """tkinter window to pause the application and show the user
    the script is done."""

    root = tk.Tk()
    root.title('HOYOLAB ZZZ Scraper')

    window_width = 300
    window_height = 100

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    root.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')

    label = tk.Label(root, text='Done', font=("Helvetica", 12))
    label.pack(pady=10)

    button = tk.Button(root, text='Close', command=root.destroy)
    button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    hoyolab_chars: list = load_chars_data()
    write_files(hoyolab_chars)
    show_done_message()
