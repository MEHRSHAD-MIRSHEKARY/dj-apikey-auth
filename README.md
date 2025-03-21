# Welcome to the Django APIKey Authentication Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-apikey-auth)](https://github.com/lazarus-org/dj-apikey-auth/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-apikey-auth)](https://pypi.org/project/dj-apikey-auth/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-apikey-auth)](https://pypi.org/project/dj-apikey-auth/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-apikey-auth)](https://pypi.org/project/dj-apikey-auth/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-apikey-auth)](https://github.com/lazarus-org/dj-apikey-auth/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-apikey-auth)](https://github.com/lazarus-org/dj-apikey-auth/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-apikey-auth)](https://github.com/lazarus-org/dj-apikey-auth)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-apikey-auth/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-apikey-auth)

[`dj-apikey-auth`](https://github.com/lazarus-org/dj-apikey-auth/) is a Django package developed by Lazarus that provides robust API key authentication and management for Django and Django REST Framework (DRF) applications.

Designed for simplicity and flexibility, it enables developers to secure API endpoints with API keys, enforce rate limiting, and manage key expiration. The package integrates seamlessly with DRF’s authentication and permission systems while offering optional caching for performance optimization.

Key features include a customizable header-based authentication mechanism, user-associated API keys, and a modern class-based view for displaying keys in a sleek, animated template.

Whether you’re building a public API or an internal service, dj-apikey-auth offers a lightweight yet powerful solution for API security and access control.

## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2
- Django REST Framework: >= 3.14

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[Authentication and Permissions](#authentication-and-permissions)**: Learn how to secure your API using API key authentication and manage access control with the APIKeyAuthentication class and HasAPIKey permission (Optional use case) in Django REST Framework (DRF).
- **[API Guide](#api-guide)**: Detailed information on available APIs and endpoints.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[Settings](#settings)**: Configuration options and settings you can customize.

---

# Quick Start

This section provides a fast and easy guide to getting the `dj-apikey-auth` package up and running in your Django
project.
Follow the steps below to quickly set up the package and start using the package.

## 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-apikey-auth
```

**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-apikey-auth
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-apikey-auth
```

## 2. Install Django REST Framework

You need to install Django REST Framework for API support. If it's not already installed in your project, you can
install it via pip:

**Using pip:**

```bash
$ pip install djangorestframework
```

## 3. Add to Installed Apps

After installing the necessary packages, ensure that both `rest_framework` and `apikey_auth` are added to
the `INSTALLED_APPS` in your Django `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",

    "apikey_auth",
    # ...
]
```

### 4. (Optional) Configure API Filters

To enable filtering through the API, install ``django-filter``, include ``django_filters`` in your ``INSTALLED_APPS``.

Install ``django-filter`` using one of the above methods:

**Using pip:**

```bash
$ pip install django-filter
```

Add `django_filters` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
   # ...
   "django_filters",
   # ...
]
```

You can also define your custom `FilterClass` and reference it in here if needed. This allows you to customize the filtering behavior according to your requirements. for more detailed info, refer to the [Settings](#settings) section.

```python
APIKEY_AUTH_API_FILTERSET_CLASS = "path/to/CustomFilterSetClass"
```


## 5. Apply Migrations

Run the following command to apply the necessary migrations:

```shell
python manage.py migrate
```

## 6. Add project URL routes

You can use the API or the Django Template View for Dashboard by Including them in your project’s `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("apikey_auth/", include("apikey_auth.urls")),
    # ...
]
```

----

# Authentication and Permissions

This section explains how to leverage the `APIKeyAuthentication` class and the `HasAPIKey` custom permission class in `dj-apikey-auth` to secure your APIs. These components provide flexible and powerful mechanisms for API key-based authentication and access control.

## Using `APIKeyAuthentication`

The `APIKeyAuthentication` class enables API key-based authentication for your Django REST Framework (DRF) application. It validates API keys passed in HTTP headers, checks their status (e.g., active, not expired), enforces rate limits, and optionally associates them with a user.

### Setting as Default Authentication

To apply `APIKeyAuthentication` globally across all your APIs, configure it as the default authentication class in your Django settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apikey_auth.api.authentication.APIKeyAuthentication',
    ]
}
```

This ensures that every API endpoint in your project uses API key authentication by default, unless overridden.

### Applying to Specific Views

For more granular control, you can apply `APIKeyAuthentication` to specific API views by setting the `authentication_classes` attribute. This works with any DRF view type, such as `APIView`, `GenericAPIView`, `ViewSet`, or `GenericViewSet`. Here’s an example:

```python
from rest_framework.response import Response
from rest_framework.views import APIView
from apikey_auth.api.authentication import APIKeyAuthentication

class MySecureView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def get(self, request):
        return Response({"message": "This view requires an API key"})
```

In this case, only `MySecureView` will require API key authentication, while other views follow the project’s default authentication settings.

### How It Works

- **Header Extraction**: Extracts the API key from the header specified by `APIKEY_AUTH_HEADER_NAME` (default: `Authorization`) with an optional prefix from `APIKEY_AUTH_HEADER_TYPE` (default: `None`), e.g., `header_type <key>`.
- **Validation**: Checks the key against the `APIKey` model, ensuring it is active (`is_active=True`) and not expired (`expires_at`).
- **Rate Limiting**: Enforces `APIKEY_AUTH_MAX_REQUESTS` (if set), incrementing `requests_count` and raising `Throttled` if exceeded.
- **Caching**: Optionally caches key lookups using `APIKEY_AUTH_USE_CACHING` and `APIKEY_AUTH_CACHE_TIMEOUT_SECONDS` for performance.
- **User Association**: Returns a tuple of `(user, api_key_instance)` where `user` is the associated user (if any) and `api_key_instance` is the `APIKey` object, attached to `request.auth`.

> **Important Note**:
>
> The `user` field in the `APIKey` model is nullable. If a valid API key is provided but not linked to a user:
> - `request.user` will be `None`.
> - `request.auth` will still contain the `APIKey` instance.
>
> This allows authentication of "anonymous" API keys, which is useful for public or shared access scenarios.

### Example Usage

Send a request with an API key in the header:

```bash
curl -X GET http://your-api.com/endpoint/ -H "Authorization: header_type test-key-123"
```

- If `test-key-123` is valid and linked to a user, `request.user` is that user, and `request.auth` is the `APIKey` instance.
- If `test-key-123` is valid but not linked to a user, `request.user` is `None`, and `request.auth` is the `APIKey` instance.
- If invalid or expired, an `AuthenticationFailed` error is returned.

## Using `HasAPIKey`

The `HasAPIKey` class is a custom DRF permission designed to ensure that an API request is authenticated with a valid API key. It complements `APIKeyAuthentication` by explicitly checking `request.auth` that is an `APIKey` instance or not.

### Implementation

This is how it is implemented:

```python
from rest_framework.permissions import BasePermission
from apikey_auth.models import APIKey

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "auth") and isinstance(request.auth, APIKey)
```

- **Check**: Verifies that `request.auth` exists and is an `APIKey` instance.
- **Purpose**: Grants access only if the request was authenticated with a valid API key via `APIKeyAuthentication`.

### Applying to Views

Add `HasAPIKey` to a view’s `permission_classes` to restrict access to requests with a valid API key:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from apikey_auth.api.authentication import APIKeyAuthentication
from apikey_auth.api.permissions import HasAPIKey

class MyAPIKeyOnlyView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [HasAPIKey]

    def get(self, request):
        return Response({"message": "Access granted with API key"})
```

### Critical Insight

`HasAPIKey` ensures that an API key is present, regardless of whether it’s linked to a user. This is distinct from `IsAuthenticated`, which requires `request.user` to be a valid user. Use both together for APIs requiring a user-linked API key:

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apikey_auth.api.authentication import APIKeyAuthentication
from apikey_auth.api.permissions import HasAPIKey

class MyUserAPIKeyView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated, HasAPIKey]

    def get(self, request):
        return Response({"message": f"Welcome, {request.user.username}"})
```

- `IsAuthenticated`: Ensures `request.user` is not `None` or `AnonymousUser`.
- `HasAPIKey`: Ensures `request.auth` is an `APIKey`.

### Key Considerations

- **Nullable User**: Since `APIKey.user` is nullable, `APIKeyAuthentication` authenticates requests even without a user. `HasAPIKey` allows these "anonymous" API keys, while `IsAuthenticated` does not.
- **Flexibility**: Use `HasAPIKey` for APIs where only an API key is needed (e.g., public APIs), and combine with `IsAuthenticated` for user-specific APIs if needed.
- **Rate Limit Headers**: When `max_requests` is set, `APIKeyAuthentication` adds `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers to responses, which can be checked regardless of user association.

### Example Scenarios

- **API Key Only**:
  - View requires any valid API key.
  - Use `HasAPIKey` alone.
  - `request.user` may be `None`.

- **User + API Key**:
  - View requires a valid user authenticated via an API key.
  - Use `IsAuthenticated` and `HasAPIKey`.
  - `request.user` is a `User` instance, and `request.auth` is an `APIKey`.

This dual approach provides maximum flexibility for securing your APIs.

----

# API Guide

This section provides a detailed overview of the `dj-apikey-auth` API, enabling administrators and users to manage API keys securely within Django and Django REST Framework (DRF) applications. The API exposes two primary endpoints:

- **`/apikey/`** - Admin API for managing all API keys (requires admin permissions).
- **`/my-apikey/`** - User API for viewing their own API keys (authenticated users only).

---

## Admin API Key Management (`/apikey/`)

The `apikey/` endpoint allows administrators (staff or superusers) to fully manage API keys. The available operations include:

- **List API keys**:

  Fetches all API keys in the system. Controlled by the `APIKEY_AUTH_API_ALLOW_LIST` setting.

- **Retrieve an API key**:

  Retrieves a specific API key by its ID. Controlled by the `APIKEY_AUTH_API_ALLOW_RETRIEVE` setting.

- **Create an API key**:

  Creates a new API key and with an associated user (Optional) with an auto-generated key. Controlled by the `APIKEY_AUTH_API_ALLOW_CREATE` setting.

- **Update an API key**:

  Updates an existing API key (e.g., toggling `is_active` or modifying `expires_at`). Controlled by the `APIKEY_AUTH_API_ALLOW_UPDATE` setting.

- **Delete an API key**:

  Deletes an existing API key. Controlled by the `APIKEY_AUTH_API_ALLOW_DELETE` setting.


### Example Responses

**List API keys**:
```text
GET /apikey/

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
    "results": [
        {
            "id": 1,
            "user": {
                "username": "user",
                "email": "example@domain.com"
            },
            "key": "test-key-123",
            "created_at": "2025-03-19T12:00:00+00:00",
            "expires_at": "2026-03-19T12:00:00+00:00",
            "is_active": true,
            "requests_count": 5,
            "max_requests": 100,
            "reset_at": "2025-03-20T12:00:00+00:00"
        }
    ]
}
```

**Create an API Key**:
```text
POST /apikey/
Content-Type: application/json

{
    "user_id": 2 (Optional)
    "expires_at": "2025-04-19T13:00:00+00:00"
}

Response:
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 3,
    "user": {
        "username": "user",
        "email": "example@domain.com"
    },
    "key": "auto-generated-key-789",
    "created_at": "2025-03-19T13:00:00+00:00",
    "expires_at": null,
    "is_active": true,
    "requests_count": 0,
    "max_requests": null,
    "reset_at": null
}
```

**Update an API Key:**
```text
PATCH /api-key/1/
Content-Type: application/json

{
    "is_active": false,
    "expires_at": "2025-06-01T00:00:00+00:00"
}

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "user": {
        "username": "user",
        "email": "example@domain.com"
    },
    "key": "test-key-123",
    "created_at": "2025-03-19T12:00:00+00:00",
    "expires_at": "2025-06-01T00:00:00+00:00",
    "is_active": false,
    "requests_count": 5,
    "max_requests": 100,
    "reset_at": "2025-03-20T12:00:00+00:00"
}
```

**Delete an API Key:**
```text
DELETE /api-key/1/

Response:
HTTP/1.1 204 No Content
Content-Type: application/json

{}
```

---

## User API Key Management (`/my-apikey/`)

The `my-apikey/` endpoint allows authenticated users to **view** their own API keys.
Users can **list** and **retrieve** API keys, but cannot create, update, or delete them.

### Example Responses

**List User API Keys**:
```text
GET /my-apikey/

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
    "results": [
        {
            "id": 1,
            "user": {
                "username": "user",
                "email": "example@domain.com"
            },
            "key": "test-key-123",
            "created_at": "2025-03-19T12:00:00+00:00",
            "expires_at": "2026-03-19T12:00:00+00:00",
            "is_active": true,
            "requests_count": 5,
            "max_requests": 100,
            "reset_at": "2025-03-20T12:00:00+00:00"
        }
    ]
}
```

**Retrieve a User's API Key**:
```text
GET /my-apikey/1/

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "user": {
        "username": "user",
        "email": "example@domain.com"
    },
    "key": "test-key-123",
    "created_at": "2025-03-19T12:00:00+00:00",
    "expires_at": "2026-03-19T12:00:00+00:00",
    "is_active": true,
    "requests_count": 5,
    "max_requests": 100,
    "reset_at": "2025-03-20T12:00:00+00:00"
}
```

---

## Response Fields

- `id`: Unique identifier of the API key.
- `user`: The ID of the user associated with the API key.
- `key`: The API key string (auto-generated on creation).
- `created_at`: Timestamp when the key was created.
- `expires_at`: Timestamp when the key expires (nullable).
- `is_active`: Boolean indicating if the key is active.
- `requests_count`: Number of requests made with the key.
- `max_requests`: Maximum allowed requests (nullable).
- `reset_at`: Timestamp when the request count resets (nullable).

---

## Throttling

The API includes a built-in throttling mechanism that limits the number of requests a user can make based on their role.
You can customize these throttle limits in the settings file.

To specify the throttle rates for regular users (maybe authenticated or not) and staff members, add the following in your settings:

```ini
APIKEY_AUTH_AUTHENTICATED_USER_THROTTLE_RATE = "100/day"
APIKEY_AUTH_STAFF_USER_THROTTLE_RATE = "60/minute"
```

These settings define the request limits for regular and admin users.

---

## Filtering, Ordering, and Search

The API supports advanced query options:

- **Ordering**: Results can be ordered by `reset_at`, `requests_count`, `max_requests`, `created_at`, `expires_at`, etc.
- **Search**: Users can search for API keys by `id` or other fields.

These configurations can be customized in the Django settings.

---

## Pagination

The API uses limit-offset pagination, allowing customization of minimum, maximum, and default page size limits.

---

## Permissions

- **Admin API (`/apikey/`)**: Restricted to staff and superusers (`IsAdminUser`).
- **User API (`/my-apikey/`)**: Available to authenticated users (`IsAuthenticated`).

---

## Parser Classes

The API supports multiple parser classes that control how data is processed. The default parsers include:

- ``JSONParser``
- ``MultiPartParser``
- ``FormParser``

You can modify parser classes by updating the API settings to include additional parsers or customize the existing ones
to suit your project.

---

Each feature can be configured through Django settings. For further details, refer to the [Settings](#settings) section.

----

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of
the Django admin panels for managing api keys.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your
Django settings. Otherwise, Django may raise the following error during checks or the ModelAdmin will not accessible in
the Admin panel.

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class
instance.

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
APIKEY_AUTH_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-apikey-auth` to use your custom admin site for its Admin interface, preventing any errors and
ensuring a smooth integration with the custom admin interface.

# APIKey Admin Panel

The `APIKeyAdmin` class provides a comprehensive admin interface for managing API keys in the Django admin panel. Below are the features and functionality of this admin interface, designed to help administrators efficiently oversee API key records.

---

## Features

### List Display

The list view for API key records includes the following fields:

- **ID**: The unique identifier for the API key record.
- **User Display**: The username of the associated user, or "Anonymous" if no user is linked.
- **Is Active**: A boolean indicating whether the API key is currently active (editable directly in the list view).
- **Requests Count**: The number of requests made using the API key.
- **Max Requests**: The maximum number of requests allowed for the API key (nullable).
- **Status**: A colored indicator showing "Active" (green) or "Inactive" (red) based on `is_active` and expiration status.

### List Display Links

The following fields are clickable links to the detailed view of each record:

- **ID**: Links to the detailed view of the API key record.
- **User Display**: Links to the detailed view of the API key record, showing the associated user or "Anonymous".

### Filtering

Admins can filter the list of API key records based on:

- **Is Active**: Filter by whether the API key is active or inactive.
- **Expires At**: Filter by the expiration date of the API key.
- **Reset At**: Filter by the date when the request count resets.

### Search Functionality

Admins can search for API key records using:

- **Key**: Search by the API key string (e.g., "test-key-123").

### Date Hierarchy

The admin interface provides a date-based navigation hierarchy using:

- **Expires At**: Allows admins to drill down into records by expiration date.

### Editable Fields

The following field can be edited directly in the list view:

- **Is Active**: Toggle the active status of API keys without entering the detailed view.

### Read-Only Fields

The following fields are marked as read-only in the detailed view:

- **Key**: The auto-generated API key string (cannot be edited).
- **Created At**: The timestamp when the API key was created (cannot be edited).
- **Reset At**: The timestamp when the request count resets (cannot be edited).

### Fieldsets

The detailed view organizes fields into the following sections:

- **General**:
  - `user`: The associated user (editable with autocomplete).
  - `key`: The API key string (read-only).
  - `created_at`: Creation timestamp (read-only).
- **Status**:
  - `is_active`: Active status toggle.
  - `expires_at`: Expiration date (editable).
  - `requests_count`: Number of requests made (read-only).
  - `max_requests`: Maximum allowed requests (editable).
  - `reset_at`: Request count reset timestamp (read-only).

### Actions

Admins can perform the following bulk actions on selected API key records:

- **Activate Keys**: Sets `is_active` to `True` for the selected API keys, with a confirmation message (e.g., "3 API keys activated.").
- **Deactivate Keys**: Sets `is_active` to `False` for the selected API keys, with a confirmation message (e.g., "2 API keys deactivated.").

### Autocomplete Fields

The following field uses an autocomplete widget for easier selection:

- **User**: Allows admins to quickly select a user from the database when editing an API key.

----

# API Keys List View

## Overview
The `APIKeyListView` provides a user-friendly interface for displaying a list of all API keys in the application. This class-based view renders API keys in a modern, animated template, offering a sleek and interactive experience for administrators or users with appropriate permissions.

## Access Control
- Access is restricted based on permissions defined in the `APIKEY_AUTH_VIEW_PERMISSION_CLASS` setting. the default is set to `IsAdminUser`.
- The view leverages Django REST Framework (DRF)-style permission classes, requiring each class to implement a `has_permission(request, view)` method that returns a boolean indicating whether access is granted.
- If any permission check fails (e.g., `has_permission` is missing or returns `False`), a `PermissionDenied` exception is raised, resulting in a 403 Forbidden response.

## Features
- **Comprehensive API Key List**: Displays all API keys in the system, regardless of user association, with efficient database queries using `select_related("user")`.
- **Customizable Ordering**: Keys are ordered according to the `APIKEY_AUTH_VIEW_ORDERING_FIELDS` setting, allowing flexible sorting.
- **Modern UI**: Rendered in the `api_keys.html` template with smooth animations and a responsive design.
- **Permission Flexibility**: Supports dynamic permission class configured via settings, compatible with DRF’s permission structure.

## Usage
1. Navigate to the API keys list URL in your application (e.g., `/apikey_auth/api-keys/` if configured in `urls.py`).
2. Ensure you meet the permission requirements specified in `APIKEY_AUTH_VIEW_PERMISSION_CLASS`.
3. View the complete list of API keys, styled in a modern table with status indicators and copy functionality.

----

# Settings

This section outlines the available settings for configuring the `dj-apikey-auth` package. You can customize these
settings in your Django project's `settings.py` file to tailor the behavior of the system monitor to your
needs.

## Example Settings

Below is an example configuration with default values:

```python
# Admin Settings
APIKEY_AUTH_ADMIN_HAS_ADD_PERMISSION = True
APIKEY_AUTH_ADMIN_HAS_CHANGE_PERMISSION = True
APIKEY_AUTH_ADMIN_HAS_DELETE_PERMISSION = True
APIKEY_AUTH_ADMIN_HAS_MODULE_PERMISSION = True
APIKEY_AUTH_ADMIN_SITE_CLASS = None

# APIKey Settings
APIKEY_AUTH_RESET_REQUEST_INTERVAL = None
APIKEY_AUTH_MAX_REQUESTS = None

# Authentication Settings
APIKEY_AUTH_HEADER_NAME = "Authorization"
APIKEY_AUTH_HEADER_TYPE = None
APIKEY_AUTH_USE_CACHING = False
APIKEY_AUTH_CACHE_TIMEOUT_SECONDS = 300

# Global API Settings
APIKEY_AUTH_API_ALLOW_LIST = True
APIKEY_AUTH_API_ALLOW_RETRIEVE = True
APIKEY_AUTH_API_ALLOW_CREATE = True
APIKEY_AUTH_API_ALLOW_UPDATE = True
APIKEY_AUTH_API_ALLOW_DELETE = True
APIKEY_AUTH_BASE_USER_THROTTLE_RATE = "100/day"
APIKEY_AUTH_STAFF_USER_THROTTLE_RATE = "1000/day"
APIKEY_AUTH_API_THROTTLE_CLASS = "apikey_auth.api.throttlings.RoleBasedUserRateThrottle"
APIKEY_AUTH_API_PAGINATION_CLASS = (
    "apikey_auth.api.paginations.DefaultLimitOffSetPagination"
)
APIKEY_AUTH_API_EXTRA_PERMISSION_CLASS = None
APIKEY_AUTH_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
APIKEY_AUTH_API_APIKEY_SERIALIZER_CLASS = (
    "apikey_auth.api.serializers.apikey_serializer.APIKeySerializer"
)
APIKEY_AUTH_USER_SERIALIZER_CLASS = "apikey_auth.api.serializers.user.UserSerializer"
# APIKEY_AUTH_USER_SERIALIZER_FIELDS = [if not provided, gets USERNAME_FIELD and REQUIRED_FIELDS from user model]
APIKEY_AUTH_API_ORDERING_FIELDS = [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
APIKEY_AUTH_API_SEARCH_FIELDS = ["id"]
APIKEY_AUTH_API_FILTERSET_CLASS = None
APIKEY_AUTH_VIEW_PERMISSION_CLASS = "rest_framework.permissions.IsAdminUser"
APIKEY_AUTH_VIEW_ORDERING_FIELDS = ["expires_at", "-created_at"]

```

# Settings Overview

Below is a detailed description of each setting in `dj-apikey-auth`, so you can better understand and tweak them to fit your project's needs.

### `APIKEY_AUTH_ADMIN_SITE_CLASS`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Optionally specifies a custom `AdminSite` class to apply to the API key admin interface. This allows for greater customization of the admin panel, enabling you to integrate your own `AdminSite` subclass with `dj-apikey-auth`’s admin features.

---

### `APIKEY_AUTH_ADMIN_HAS_ADD_PERMISSION`

**Type**: `bool`

**Default**: `True`

**Description**: Controls whether administrators can add new API keys via the admin interface. Set to `False` to disable this capability.

---

### `APIKEY_AUTH_ADMIN_HAS_CHANGE_PERMISSION`

**Type**: `bool`

**Default**: `True`

**Description**: Controls whether administrators can modify existing API keys via the admin interface. Set to `False` to disable this capability.

---

### `APIKEY_AUTH_ADMIN_HAS_DELETE_PERMISSION`

**Type**: `bool`

**Default**: `True`

**Description**: Controls whether administrators can delete API keys via the admin interface. Set to `False` to disable this capability.

---

### `APIKEY_AUTH_ADMIN_HAS_MODULE_PERMISSION`

**Type**: `bool`

**Default**: `True`

**Description**: Controls whether administrators have module-level access to the API key admin interface. Set to `False` to restrict access to the entire module.

---

### `APIKEY_AUTH_RESET_REQUEST_INTERVAL`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the interval after which the request count for API keys resets. Must be one of `minutely`, `hourly`, `daily`, or `monthly`. Set to `None` to disable automatic reset.

---

### `APIKEY_AUTH_MAX_REQUESTS`

**Type**: `Optional[int]`

**Default**: `None`

**Description**: Sets the maximum number of requests allowed per API key before throttling is enforced. Set to `None` for unlimited requests.

---

### `APIKEY_AUTH_HEADER_NAME`

**Type**: `str`

**Default**: `"Authorization"`

**Description**: Specifies the HTTP header name used to pass the API key (e.g., `"Authorization"` or `"X-API-Key"`). Customize this to match your authentication setup.

---

### `APIKEY_AUTH_HEADER_TYPE`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the prefix expected in the API key header (e.g., `"Bearer"` in `"Bearer <key>"`). Customize this to align with your authentication format.

---

### `APIKEY_AUTH_USE_CACHING`

**Type**: `bool`

**Default**: `False`

**Description**: Enables caching of API key lookups to improve performance. Set to `True` to enable caching and fetch keys from the database on every request.

---

### `APIKEY_AUTH_CACHE_TIMEOUT_SECONDS`

**Type**: `int`

**Default**: `300`

**Description**: Sets the duration (in seconds) that API key data is cached when caching is enabled. Adjust this to balance performance and freshness of data.

---

### `APIKEY_AUTH_API_ALLOW_LIST`

**Type**: `bool`

**Default**: `True`

**Description**: Allows the API to list all API keys for the authenticated user. Set to `False` to disable this feature.

---

### `APIKEY_AUTH_API_ALLOW_RETRIEVE`

**Type**: `bool`

**Default**: `True`

**Description**: Allows retrieving individual API keys by ID via the API. Set to `False` to disable this feature.

---

### `APIKEY_AUTH_API_ALLOW_CREATE`

**Type**: `bool`

**Default**: `True`

**Description**: Allows creating new API keys via the API. Set to `False` to disable this feature.

---

### `APIKEY_AUTH_API_ALLOW_UPDATE`

**Type**: `bool`

**Default**: `True`

**Description**: Allows updating existing API keys via the API (e.g., toggling `is_active`). Set to `False` to disable this feature.

---

### `APIKEY_AUTH_API_ALLOW_DELETE`

**Type**: `bool`

**Default**: `False`

**Description**: Allows deleting API keys via the API. Set to `True` to enable this feature.

---

### `APIKEY_AUTH_BASE_USER_THROTTLE_RATE`

**Type**: `str`

**Default**: `"100/day"`

**Description**: Sets the throttle rate (e.g., `"100/day"`) for regular authenticated users in the API. Adjust this to limit request frequency.

---

### `APIKEY_AUTH_STAFF_USER_THROTTLE_RATE`

**Type**: `str`

**Default**: `"1000/day"`

**Description**: Sets the throttle rate (e.g., `"1000/day"`) for staff (admin) users in the API. Adjust this to provide higher limits for privileged users.

---

### `APIKEY_AUTH_API_THROTTLE_CLASS`

**Type**: `Optional[str]`

**Default**: `"apikey_auth.api.throttlings.RoleBasedUserRateThrottle"`

**Description**: Specifies the throttle class used to limit API requests (e.g., a DRF throttle class path). Set to `None` to disable custom throttling or use DRF’s `DEFAULT_THROTTLE_CLASSES`.

---

### `APIKEY_AUTH_API_PAGINATION_CLASS`

**Type**: `Optional[str]`

**Default**: `"apikey_auth.api.paginations.DefaultLimitOffSetPagination"`

**Description**: Defines the pagination class used in API responses (e.g., a DRF pagination class path). Set to `None` to disable pagination or use a custom style.

---

### `APIKEY_AUTH_API_EXTRA_PERMISSION_CLASS`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Optionally specifies an additional DRF permission class to extend the base permissions for the API (e.g., `"path.to.HasAPIKeyPermission"`). This allows for fine-grained access control beyond authentication.

---

### `APIKEY_AUTH_API_PARSER_CLASSES`

**Type**: `List[str]`

**Default**:

```python
apikey_auth_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
```

**Description**: Specifies the parsers used to handle API request data formats. You can modify this list to add your
parsers or set ``None`` if no parser needed.

---

### `APIKEY_AUTH_USER_SERIALIZER_FIELDS`

**Type**: `List[str]`

**Default**: `USERNAME_FIELD` and `REQUIRED_FIELDS` from user model

**Description**: Defines the fields to be included in the user serializer in API.

---

### `APIKEY_AUTH_APIKEY_SERIALIZER_CLASS`

**Type**: `str`

**Default**: `"apikey_auth.api.serializers.apikey.APIKeySerializer"`

**Description**: Specifies the serializer class used for APIKey objects in the API. Customize this if you need a different serializer.

---

### `APIKEY_AUTH_USER_SERIALIZER_CLASS`

**Type**: `str`

**Default**: `"apikey_auth.api.serializers.user.UserSerializer"`

**Description**: Specifies the path to the serializer class used for user objects in the API. Customize this if you need a different user serializer.

---

### `APIKEY_AUTH_API_ORDERING_FIELDS`

**Type**: `List[str]`

**Default**: `["max_requests", "requests_count", "created_at", "expires_at", "max_requests", "reset_at"]`

**Description**: Specifies the fields available for ordering in API queries, allowing responses to be sorted by these fields. See all available fields below.

---

### `APIKEY_AUTH_API_SEARCH_FIELDS`

**Type**: `List[str]`

**Default**: `["id"]`

**Description**: Specifies the fields that are searchable in the API, allowing users to filter results based on these fields. See all available fields below.

---

### `APIKEY_AUTH_API_FILTERSET_CLASS`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Specifies a custom filterset class for API filtering (e.g., a `django-filter` class path). Set to `None` to disable custom filtering.

---

### `APIKEY_AUTH_VIEW_PERMISSION_CLASS`

**Type**: `Optional[str]`

**Default**: `"rest_framework.permissions.IsAdminUser"`

**Description**: Specifies the DRF permission class for the `APIKeyListView`. Customize this to change access requirements for the view.

---

### `APIKEY_AUTH_VIEW_ORDERING_FIELDS`

**Type**: `List[str]`

**Default**: `["expires_at", "-created_at"]`

**Description**: Specifies the fields that the `APIKeyListView` can be ordered by. Adjust this to sort the displayed API key list differently.

---

### All Available Fields

These are all fields available for searching and ordering in API key records:

- `id`: Unique identifier of the API key (orderable, searchable).
- `user`: ID of the associated user (orderable).
- `key`: The API key string (searchable).
- `created_at`: Timestamp when the key was created (orderable).
- `expires_at`: Timestamp when the key expires (orderable).
- `is_active`: Boolean indicating if the key is active (orderable).
- `requests_count`: Number of requests made with the key (orderable).
- `max_requests`: Maximum allowed requests (orderable).
- `reset_at`: Timestamp when the request count resets (orderable).
----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-apikey-auth`.

### Final Notes:

- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python
  versions.
- **API Integration**: The package is designed for flexibility, allowing you to customize many features based on your
  application's needs.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for
  more details.

If you encounter any issues or have feedback, please reach out via
our [GitHub Issues page](https://github.com/lazarus-org/dj-apikey-auth/issues).
