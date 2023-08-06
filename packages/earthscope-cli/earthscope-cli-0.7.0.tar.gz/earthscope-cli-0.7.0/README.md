# EarthScope CLI

A Typer CLI for authenticating with the EarthScope API

## Getting Started

1. (Optional) Suggest setting up and activating a python virtual environment so as to not clutter your system python

   ```shell
   python3 -m venv venv
   . venv/bin/activate
   ```
   
2. Install the CLI:

   ```shell
   pip install earthscope-cli
   ```

3. Use the CLI. The package has a `console_scripts` section which makes a shortcut called `es` available in your python environment.

   ```shell
   es --help
   ```

### Use the CLI with your user profile

```shell
# Login to EarthScope with Device Authorization Flow using one of the following
es sso login
es sso login --token

# Get access token
es sso access --token

# Refresh access token
es sso refresh

# Get your user profile from the `user-management-api` running behind https://test-idm.unavco.org/user/profile/
es user get

# Explore the CLI
es --help
es sso --help
```

### Use the CLI with machine-to-machine client credentials

```shell
# Set required environment variables
export ES_CLI_M2M_CLIENT_ID=my_m2m_client_id
export ES_CLI_M2M_CLIENT_SECRET=my_m2m_client_secret

# Login to EarthScope with Client Credentials Flow using one of the following
es m2m login
es m2m login --token

# Get access token
es m2m access --token

# Lookup a user's anonymous profile info
es user lookup --id 'google-oauth2|115207392315468355758'

# Explore the CLI
es m2m --help
```
