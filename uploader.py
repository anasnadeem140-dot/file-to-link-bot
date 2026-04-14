import requests

def upload_to_pixeldrain(file_path):
    url = "https://pixeldrain.com/api/file"

    with open(file_path, "rb") as f:
        res = requests.post(url, files={"file": f})

    data = res.json()

    if "id" in data:
        return f"https://pixeldrain.com/u/{data['id']}"

    return None
