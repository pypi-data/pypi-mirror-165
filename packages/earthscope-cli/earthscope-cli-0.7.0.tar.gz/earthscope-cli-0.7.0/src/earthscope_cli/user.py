from typing import List
import typer

from rich import print
from earthscope_cli.m2m import CliClientCredentialsFlow
from earthscope_cli.sso import device_flow
from earthscope_sdk.user.user import get_user, lookup_anon

app = typer.Typer()


@app.command()
def get():
    device_flow.load_tokens()
    user = get_user(device_flow.access_token)
    print(user)


@app.command()
def lookup(
    ids: List[str] = typer.Option(
        [],
        "--id",
        help="User ID to lookup. Specify this option multiple times to lookup more than one user",
    ),
    emails: List[str] = typer.Option(
        [],
        "--email",
        help="User email to lookup. Specify this option multiple times to lookup more than one user",
    ),
):
    m2m_flow = CliClientCredentialsFlow.get()
    try:
        resp = lookup_anon(m2m_flow.access_token, ids=ids, emails=emails)
        print(resp)
    except ValueError as e:
        print(f"[red]{e}")
        typer.Exit(1)
