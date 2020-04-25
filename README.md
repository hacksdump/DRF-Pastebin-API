# Django Pastebin API

### Generate Google OAuth credentials

Go to [https://console.developers.google.com](https://console.developers.google.com/) and register your application. We'll need client id and client secret.

### Quick setup

* Clone the repository

```shell
git clone git@github.com:hacksdump/DRF-Pastebin-API.git
cd DRF-Pastebin-API
```

* Create a virtual environment and activate it
  
```shell
python3 -m virtualenv venv
source venv/bin/activate
```

* Install python dependencies

```shell
pip install -r requirements.txt
```

* Create database and migrate

```shell
python manage.py migrate
```

* Write config file (edit .env after creation)

```shell
cd tutorial
cp .env.example .env
```

* Start the developmental server

```shell
python manage.py runserver
```

### Consuming the API

#### Auth

1. The client application (API consumer) should be running a server to receive the auth code after redirection from Google consent page. This redirect URI must be registered on google developer console as well.

    POST /auth/get-consent-page-uri/
   
   JSON payload:
    ```json
    {
       "redirect_uri": "http://redirect.uri"
    }
    ```
   JSON Response:
    ```json
    {
       "uri": "https://the.url.the.client.needs.to.visit.to.give.consent"
    }
    ```
   
2. After the user visits the consent page and approves, the auth code is received by the server run by API consumer. This auth code should be sent to our server to get the JWT token which will ultimately give access to protected routes.

    POST /auth/exchange-auth-code-for-jwt/
    JSON payload:
    ```json
    {
	    "redirect_uri":"http://redirect.uri",
	    "oauth_code": "4/zAGtPYBK94C-bKx0RpMP3_mkjsdfs8hfsidhfsfwefssf"
    }
    ```
   JSON Response:
    ```json
    {
        "username": "google_username@gmail.com",
        "access_token": "this_token_is_used_to_authorize_requests",
        "refresh_token": "this_token_is_used_to_generate_new_access_token"
    }
    ```
   
3. Now, use the access_token by passing in headers as:
    
    `Authorization: Bearer <access_token_here>`
