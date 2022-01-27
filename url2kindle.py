import json
import os
from base64 import b64encode
from subprocess import check_output

import apprise
import magic
import requests
from bs4 import BeautifulSoup

PARSER_PATH = os.environ.get("PARSER_PATH", "mercury-parser")
KINDLE_APPRISE_URL = os.environ["KINDLE_APPRISE_URL"]
KINDLE_TAG = "kindle"
ADMIN_APPRISE_URL = os.environ["ADMIN_APPRISE_URL"]
ADMIN_TAG = "admin"

sender = apprise.Apprise()
sender.add(KINDLE_APPRISE_URL, tag=KINDLE_TAG)
sender.add(ADMIN_APPRISE_URL, tag=ADMIN_TAG)


def safe_filename(filename, default="url2kindle"):
    filename = "".join(
        char if char not in '<>:"“”/\|?*' else " " for char in filename
    )  # Remove invalid chars
    filename = " ".join(filename.split())  # Strip excess whitespace
    return filename or default


def embed_image(src: str) -> str:
    if src.startswith("data:"):
        return src
    image = requests.get(src).content
    mime = magic.from_buffer(image, mime=True)
    if not mime.startswith("image/"):
        return src
    image_base64 = b64encode(image).decode("utf8")
    return f"data:{mime};base64,{image_base64}"


def embed_images(soup: BeautifulSoup) -> BeautifulSoup:
    images = soup.find_all("img")
    for image in images:
        image["src"] = embed_image(image["src"])
    return soup


def url2kindle(url):
    try:
        mercury_output_json = check_output([PARSER_PATH, url])
        mercury_output = json.loads(mercury_output_json)
        body_content = BeautifulSoup(mercury_output["content"], "html.parser")
        body_content = embed_images(body_content)

        html = BeautifulSoup("<html><body></body></html>", "html.parser")
        html.body.append(body_content)

        filename = f"{safe_filename(mercury_output['title'])}.html"
        with open(filename, "w", encoding="utf8") as f:
            f.write(str(html))
        sender.notify(
            title=f"url2kindle",
            body="See attached...",
            attach=filename,
            tag=KINDLE_TAG,
        )
        os.remove(filename)
    except Exception as e:
        sender.notify(title="url2kindle - Error!", body=str(e), tag=ADMIN_TAG)
