# WebCase django JWT authentication

Based on [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/) with a little bit of additional goodies.

Us it's documentation as a source of truth. All changes and additional info about configuration are described here, in this documentation.

## Installation

```sh
pip install wc-django-jwt
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
]

WCD_JWT = {
  # Serializer class for JWT token.
  'TOKEN_OBTAIN_SERIALIZER': 'wcd_jwt.serializers.TokenObtainPairSerializer',
  # Serializer class for JWT token refresh.
  'TOKEN_REFRESH_SERIALIZER': 'wcd_jwt.serializers.TokenRefreshSerializer',

  # Authentication class that will be used by auth middleware to check tokens.
  'AUTHENTICATION_CLASS': 'wcd_jwt.authentication.JWTAuthentication',
  # Available token types to match on.
  'TOKEN_TYPES': [
    'rest_framework_simplejwt.tokens.AccessToken',
    'rest_framework_simplejwt.tokens.RefreshToken',
  ],
  # Should you rotate refresh tokens on access refresh.
  'ROTATE_REFRESH_TOKENS': False,
  # Should you update lsat login field on user on token obtain call.
  'UPDATE_LAST_LOGIN': False,
}

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    # Might be used to authenticate DRF requests.
    'wcd_jwt.authentication.JWTAuthentication',
  )
}

MIDDLEWARE = [
  ...
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  ...
  # Authentication middleware must be placed after django's
  # `AuthenticationMiddleware`.
  'wcd_jwt.middleware.AuthenticationMiddleware',
  ...
]
```

There are ready for use frontend for django rest framework. It mostly provided by `djangorestframework-simplejwt` with some additional changes.

In `urls.py`:

```python
from wcd_jwt.views import make_urlpatterns as jwt_make_urlpatterns

urlpatters = [
  ...
  path(
    'api/v1/auth/token/',
    include((jwt_make_urlpatterns(), 'wcd_jwt'),
    namespace='jwt-auth')
  ),
]
```

And after all that manipulations you end up with 4 views for jwt tokens authentication.

Function `make_urlpatterns` can take your custom views and replace default ones.

## Token registry

Tokens by default are generate-and-forget things. In case you need to remember what tokens were created and for what users there is a contrib package added: `wcd_jwt.contrib.registry`.

It registers all your generated tokens. And may be used to force-expire any of them.

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
  'wcd_jwt.contrib.registry',
]

WCD_JWT = {
  # Serializer class for JWT token refresh should be changed to:
  'TOKEN_REFRESH_SERIALIZER': 'wcd_jwt.contrib.registry.serializers.TokenRefreshSerializer',

  # If you want to block user not after trey'r access token expired, but
  # at any time they made request change authentication class to:
  'AUTHENTICATION_CLASS': 'wcd_jwt.contrib.registry.authentication.JWTAuthentication',
}

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'wcd_jwt.contrib.registry.authentication.JWTAuthentication',
  )
}

WCD_JWT_REGISTRY = {
  # Token expire serializer may be replaced like this:
  'TOKEN_EXPIRE_SERIALIZER': 'wcd_jwt.contrib.registry.serializers.TokenExpireSerializer',

  # Automatically expire all other token in a tree except client's
  # available refresh and access tokens.
  # Works only when `TOKEN_REGISTRATION_ON_SIGNAL` enabled.
  'TOKEN_EXPIRE_ON_REFRESH': False,

  # Pipeline functions list for token registration runner.
  'TOKEN_REGISTRATION_PIPELINE': [
    'wcd_jwt.contrib.registry.services.pipeline.register_pairs',
    'wcd_jwt.contrib.registry.services.pipeline.connecting_user',
  ],
  # Automatically runs token registration on wcd_jwt obtain and
  # refresh signals sended.
  'TOKEN_REGISTRATION_ON_SIGNAL': True,
  # Run token registration parallel to main request. It lowers response
  # wait time.
  # It uses Thread(daemon=True) to accomplish "parallelism".
  'TOKEN_REGISTRATION_ON_SIGNAL_PARALLEL': False,
}
```

The same for urls.

In `urls.py`:

```python
from wcd_jwt.contrib.registry.views import make_urlpatterns as jwt_registry_make_urlpatterns

urlpatters = [
  ...
  path(
    'api/v1/auth/token/',
    include((jwt_registry_make_urlpatterns(), 'wcd_jwt_registry'),
    namespace='jwt-auth-registry')
  ),
]
```

Registry provides 2 models:
- `Token` - Stores information about generated tokens. They are hierarchical. Hierarchy is based on which token was used to generate those from response. Refresh token will always be a parent for access token.
- `TokenUserConnection` - Connects user to token model.

There is only one view at the moment that adds ability to expire any valid token.

To display tokens on the client you may made your own views. Package will not provide them, because there certainly will be additional logic to display, so wer'e not event bothering ourselves).

Tokens has some query methods to made querying easier:

```python
list_of_expired_tokens = Token.objects.expired()
list_of_active_tokens = Token.objects.active()

# Method `collect_tree` we can collect all the ids from token related trees
# for any number of tokens we wish.
# Here we collecting tree ids for some `token1`.
list_of_ids_for_all_the_token_relatives_tree = Token.objects.collect_tree(
  ids=[token1.id]
)

# We may easily find tokens for a certain user:
list_of_users_tokens = Token.objects.filter(
  user_connections__user=some_user_instance
)

# etc.
```

To register tokens manually run registration pipeline:

```python
from wcd_jwt.contrib.registry.services import pipeline

pipeline.run({
  # Token pairs: (child, parent)
  'pairs': [
    (AccessToken(''), RefreshToken('')),
  ],
  # Optional.
  'user': user or None,
  # Optional.
  'request': request,
})
```

Old tokens that are no longer active might be not useful anymore. For this case there is an **archiver** service:

```python
from wcd_jwt.contrib.registry.services import archiver
from rest_framework_simplejwt.utils import aware_utcnow

archiver.archive(
  # There is also optional `now` parameter.
  # Here, as an example, we deleting only tokens that expired more than
  # 10 days ago.
  # It will be `aware_utcnow()` by default.
  now=aware_utcnow() - timedelta(days=10)
)
```

## Token device registry

Also you may want to know what device was used to access site with registered token.

It depends on `wc-django-device-recognizer`. So it must be also added to installed apps.

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_device_recognizer',

  'wcd_jwt',
  'wcd_jwt.contrib.registry',
  'wcd_jwt.contrib.device_registry',
]

# To be able to register token interlocutors:
WCD_JWT_REGISTRY_TOKEN_REGISTRATION_PIPELINE = [
  'wcd_jwt.contrib.registry.services.pipeline.register_pairs',
  'wcd_jwt.contrib.registry.services.pipeline.connecting_user',
  # Add this to your registry pipeline
  'wcd_jwt.contrib.device_registry.services.pipeline.connect_interlocutor',
]
```

To connect tokens with some interlocutor manually just run connector service:

```python
from wcd_jwt.contrib.device_registry.services import connector

from wcd_device_recognizer.models import Interlocutor, InterlocutorNetwork
from wcd_jwt.contrib.registry.models import Token


connections: List[TokenInterlocutorConnection] = connector.connect(
  Interlocutor(),
  [
    Token(),
  ],
  # Optional.
  network=InterlocutorNetwork(),
)
```
