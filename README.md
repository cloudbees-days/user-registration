CloudBees Days User Registration form


**Purpose**: Allow CloudBees Days workshop attendees to register for access to the environments.


## Info
* Built using [Flask](https://flask.palletsprojects.com/en/1.1.x/).

### Environment variables

| Env var | Example | Description |
| --- | --- | --- |
| LDAP_ADMIN | username | Username of a FreeIPA user who has user admin privileges. |
| LDAP_PASSWORD | password | Password of the FreeIPA user admin. |
| LDAP_SERVER | ipa.example.com | URL (don't include protocol) of your FreeIPA server. |
| SLACK_ENABLED | true | If you want to invite users to your Slack workspace, set this to true |
| SLACK_API_TOKEN | api_token | Use your Slack workspace's API token. |
| SLACK_WORKSPACE | example-workspace | The Slack workspace to invite users to. |

### How to run

#### Locally

```python
# If you don't have pipenv installed, install it
pip install pipenv

# Now install the dependencies
pipenv install

# Run the application (Must have the above environment variables set)
pipenv run gunicorn app:app --bind 0.0.0.0:8000

# The service is now available on port 8000.
```

#### Docker
```
# First build the image
docker build -t user-registration .

# Now run it, filling in the parameters with appropriate values
docker run -p 8000:8000 -e LDAP_ADMIN=admin -e LDAP_PASSWORD=password \
  -e LDAP_SERVER=ipa.example.com -e SLACK_ENABLED=true -e SLACK_API_TOKEN=92309428 \
  -e SLACK_WORKSPACE=example-workspace user-registration
```


## Todo

* [x] Integrate with FreeIPA
* [x] Send off slack invitation
* [x] Create Dockerfile
