# Eazy Django User

Eazy Django User is a django package that provides a user model with user email as the identifier.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install eazy-django-user
```

## Usage
1. Add "eazy_user" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
        ...
        'eazy_user',
    ]
```
2. set AUTH_USER_MODEL in setting.py to "eazy_user.EmailUser" like this:
**Note:** Add this setting before initial migration else there will be clashes with the default user model.
```python
AUTH_USER_MODEL = 'eazy_user.EmailUser'
```
3. Run ``python manage.py migrate`` to apply the migrations to the database.

```bash
python manage.py migrate
```
4. You can access the user foreign key like this:
```python
from django.conf import settings

User = settings.AUTH_USER_MODEL

class YourModel(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
```
5. Or by using the get_user_model method.
```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

But you would most likely want to extend the ```python EmailUser ``` model you can do that easily:

```python
from eazy_user.models import EmailUser

class YourCustomUser(EmailUser):
    ....
```

Whatever you choose, make sure to set the resulting user model as the ```python AUTH_USER_MODEL``` in the settings.py file

```python
AUTH_USER_MODEL = '<your_app_name>.<YourCustomUser>' """<your_app_name> refers to the app that contains your custom user model, while <YourCustomUser> is the custom user model."""
```

Now you can proceed to creating a super user ```bash python manage.py createsuperuser``` like you normaly would, and enjoy :)

## License
[MIT](https://choosealicense.com/licenses/mit/)