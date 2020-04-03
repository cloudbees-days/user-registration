# CloudBees Days User Registration form


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
| INVITE_CODE | attendee2020 | Set an invite code for basic level of access to restrict who has access to signup. |
| USER_GROUP | attendee | Set the FreeIPA user group for those who sign up with INVITE_CODE value. |
| ELEVATED_INVITE_CODE | admin2020 | Set the invite code for users with elevated level of access (e.g. workshop admins). |
| ELEVATED_USER_GROUP | sa-users | Set the FreeIPA user group for those who sign up with the ELEVATED_INVITE_CODE value. |


### How to run

#### Locally

```bash
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
* [x] Add multiple invite codes for different levels
