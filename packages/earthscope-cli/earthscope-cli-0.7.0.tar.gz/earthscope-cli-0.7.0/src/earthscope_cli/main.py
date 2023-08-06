import typer

from earthscope_cli import m2m, sso, user

app = typer.Typer()

app.add_typer(
    m2m.app,
    name="m2m",
    help="Login to Earthscope API with machine-to-machine (m2m) credentials",
)
app.add_typer(
    sso.app, name="sso", help="Login to Earthscope API using SSO with your user account"
)
app.add_typer(user.app, name="user", help="Use Earthscope API user endpoints")


if __name__ == "__main__":
    app()
