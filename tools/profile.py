import json

PROFILE_FILE = "data/profile.json"

def load_profile():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"name": "", "nickname": "sayang"}

def save_profile(data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def set_nickname(nickname):
    profile = load_profile()
    profile["nickname"] = nickname
    save_profile(profile)
    return f"Oke, sayangku! Panggilanmu diubah menjadi '{nickname}' 💖."

def get_nickname():
    profile = load_profile()
    return profile.get("nickname", "sayang")