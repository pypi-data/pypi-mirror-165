import os
import typer

from pathlib import Path

APP_DIR = Path(os.environ.get("APP_DIRECTORY", typer.get_app_dir("earthscope-cli")))
os.makedirs(APP_DIR, exist_ok=True)

ES_CLI_PREFIX = "ES_CLI"
AUTH0_AUDIENCE = os.environ.get(
    f"{ES_CLI_PREFIX}_AUTH0_AUDIENCE", "https://account.earthscope.org"
)
AUTH0_DOMAIN = os.environ.get(
    f"{ES_CLI_PREFIX}_AUTH0_DOMAIN", "login.earthscope.org"
)
