import datetime as dt
import json
import typer

from os import environ
from pathlib import Path
from rich import print

from earthscope_cli.util import APP_DIR, AUTH0_AUDIENCE, AUTH0_DOMAIN, ES_CLI_PREFIX
from earthscope_sdk.auth.auth_flow import (
    InvalidRefreshTokenError,
    NoTokensError,
    NoIdTokenError,
    NoRefreshTokenError,
    ValidTokens,
)
from earthscope_sdk.auth.device_code_flow import (
    DeviceCodeFlow,
    PollingError,
    PollingAccessDeniedError,
    PollingExpiredError,
    RequestDeviceTokensError,
)

app = typer.Typer()

AUTH_STATE_PATH = APP_DIR / "sso_tokens.json"

AUTH0_CLIENT_ID = environ.get(
    f"{ES_CLI_PREFIX}_AUTH0_CLIENT_ID", "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
)
SCOPE = environ.get(
    f"{ES_CLI_PREFIX}_SSO_TOKEN_SCOPE", "openid profile email offline_access"
)

AUTO_REFRESH_THRESHOLD_CONFIG = f"{ES_CLI_PREFIX}_AUTO_REFRESH_THRESHOLD_SECONDS"


class CliDeviceCodeFlow(DeviceCodeFlow):
    def __init__(
        self, domain: str, audience: str, client_id: str, scope: str, path: Path
    ) -> None:
        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_id,
            scope=scope,
        )
        self.path = path

    def load_tokens(self):
        try:
            with self.path.open() as f:
                json_state = json.load(f)
        except FileNotFoundError:
            print("[red]User is not logged in.")
            raise typer.Exit(1)

        self.validate_tokens(json_state)
        return self.tokens

    def save_tokens(self, creds: ValidTokens):
        json_str_state = json.dumps(vars(creds))
        with self.path.open("w") as f:
            f.write(json_str_state)

    def prompt_user(self):
        if not self._device_codes:
            raise RuntimeError(
                "You must start the device flow before prompting the user"
            )

        print(
            f"""Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

{self._device_codes.verification_uri_complete}
"""
        )
        typer.launch(self._device_codes.verification_uri_complete)


device_flow = CliDeviceCodeFlow(
    audience=AUTH0_AUDIENCE,
    client_id=AUTH0_CLIENT_ID,
    domain=AUTH0_DOMAIN,
    scope=SCOPE,
    path=AUTH_STATE_PATH,
)


@app.command(help="Login to Earthscope API using SSO with your user account")
def login():
    try:
        device_flow.do_flow()
    except RequestDeviceTokensError:
        print("[red]Failed to get device code")
        raise typer.Exit(1)
    except PollingAccessDeniedError:
        print("[red]Access denied")
        raise typer.Exit(1)
    except PollingExpiredError:
        print("[red]Authentication session timed out. Restart the authentication")
        raise typer.Exit(1)
    except PollingError as e:
        print(f"[red]Polling failed for unknown reason: {e}")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Device flow failed for unknown reason: {e}")
        raise typer.Exit(1)

    print(f"[green]Successful login! Access token expires at {device_flow.expires_at}")


@app.command(help="Clear your local SSO tokens")
def logout():
    try:
        AUTH_STATE_PATH.unlink()
    except FileNotFoundError:
        print("Not logged in")
    else:
        print("[green]Logged out")


@app.command(
    help="Refresh your SSO session, invalidate your refresh token family, or print out the refresh token"
)
def refresh(
    token: bool = typer.Option(
        False,
        help="Get refresh token",
    ),
    invalidate: bool = typer.Option(
        False,
        help="Invalidate this refresh token family by triggering re-use detection",
    ),
):
    device_flow.load_tokens()
    try:
        if token:
            typer.echo(device_flow.refresh_token)
            raise typer.Exit(0)

        device_flow.refresh(persist=not invalidate)
    except InvalidRefreshTokenError:
        if not invalidate:
            print(
                "[red]Refresh token is not valid. You must re-authenticate to start a new refreshable session."
            )
            raise typer.Exit(1)
        else:
            print("This refresh token is already invalid")
            raise typer.Exit(0)
    except NoRefreshTokenError:
        print("[red]No refresh token present")
        raise typer.Exit(1)

    if invalidate:
        try:
            device_flow.refresh()
        except InvalidRefreshTokenError:
            print("[green]Refresh token family invalidated")
            raise typer.Exit(0)
        else:
            print(
                "[yellow]Token refreshed twice. This does not appear to be a rotating refresh token."
            )

    print(
        f"[green]Successful refresh! New access token expires at {device_flow.expires_at})"
    )


@app.command(help="Print all SSO state information stored locally on this machine")
def state(
    only_path: bool = typer.Option(
        False,
        "--path",
        "-p",
        help="Print the full path to where the state is stored on this machine",
    )
):
    if only_path:
        typer.echo(AUTH_STATE_PATH)
        raise typer.Exit(0)

    device_flow.load_tokens()
    print(vars(device_flow.tokens))


@app.command(
    help="Print the access token body (or token). Automatically refreshes the token when necessary"
)
def access(
    token: bool = typer.Option(
        False,
        "--token",
        "-t",
        help="Get access token",
    ),
    no_auto_refresh: bool = typer.Option(
        False,
        "--no-auto-refresh",
        help="Disable automatic token refresh. The default behavior is to automatically attempt to refresh the token if it can be refreshed and there is less than 1 hour before the token expires.",
    ),
    auto_refresh_threshold: int = typer.Option(
        3600,
        "--auto-refresh-threshold",
        "-a",
        help="The amount of time remaining (in seconds) before token expiration after which a refresh is automatically attempted. Default is one hour.",
        envvar=AUTO_REFRESH_THRESHOLD_CONFIG,
    ),
):
    device_flow.load_tokens()
    if (
        not no_auto_refresh
        and device_flow.ttl < dt.timedelta(seconds=auto_refresh_threshold)
        and device_flow.refreshable
    ):
        try:
            device_flow.refresh()
        except InvalidRefreshTokenError:
            print(
                "[red]Unable to refresh because the refresh token is not valid. Use '--no-auto-refresh' option to get token anyway."
            )
            raise typer.Exit(1)

    try:
        if token:
            typer.echo(device_flow.access_token)
        else:
            print(device_flow.access_token_body)
    except NoTokensError:
        print("[red]No access token present")
        raise typer.Exit(1)


@app.command(help="Print the date & time at which the access token was issued")
def issued():
    device_flow.load_tokens()
    print(device_flow.issued_at)


@app.command(help="Print the date & time at which the access token expires")
def expires():
    device_flow.load_tokens()
    print(device_flow.expires_at)


@app.command(help="Print the ID token body (or token)")
def id(
    token: bool = typer.Option(
        False,
        help="Get ID token",
    )
):
    device_flow.load_tokens()
    try:
        if token:
            typer.echo(device_flow.id_token)
        else:
            print(device_flow.id_token_body)
    except NoIdTokenError:
        print("[red]No ID token present")
        raise typer.Exit(1)


@app.command(help="Print the access token's scope")
def scope():
    device_flow.load_tokens()
    print(device_flow.tokens.scope.split())


@app.command(help="Print the access token's time-to-live (TTL)")
def ttl():
    device_flow.load_tokens()
    if device_flow.ttl.total_seconds() > 0:
        print(device_flow.ttl)
        return

    print("[red]The access token is expired")
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
