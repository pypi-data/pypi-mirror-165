# Django notifications

## Install
```sh
pip install django-transactional-notifications
```

```python
# settings.py
INSTALLED_APPS += ["txn_notifications"]

DJANGO_NOTIFICATIONS = {
  "email": {
    "enabled": True,
  }
}
```

## Features
Template based notifications. You can use markdown

* Edit messages from django admin
  * Template based message
  * Rich html message format using markdown
* Customizable and extensible handler
  * Add your own handler for the services you use
* User settings (allow/disallow notification by handler or category)
* Check message status (`is_sent`)
  * Update message status (using callbacks)

## Wrappers
* `NotificationWrapper`

## Handlers 
* `DjangoHandler`
* `EmailHandler` (`generic`)
  * `MailgunHandler` with `webhooks`
  * `Sendgrid`
* `TwilioHandler` with `callbacks`
  * `SMS`
  * `Whatsapp`

## Models
Notification structure
* `Category`
* `Template`
* `Notification`

User preferences
* `UserCategorySettings`
* `UserHandlerSettings`

## Settings
Optional. Override the models.

```python
# settings.py
NOTIFICATIONS_CATEGORY_MODEL = "notifications.Category"
NOTIFICATIONS_TEMPLATE_MODEL = "notifications.Template"
NOTIFICATIONS_NOTIFICATION_MODEL = "notifications.Notification"
NOTIFICATIONS_USERHANDLERSETTINGS_MODEL = "notifications.UserHandlerSettings"
NOTIFICATIONS_USERCATEGORYSETTINGS_MODEL = "notifications.UserCategorySettings"
```

```python
# your custom_module.py
import swapper
from django.db import models

from txn_notifications.base.models import AbstractNotification

class MyNotification(AbstractNotification):
  # `get_model_name` is required if you want to override a ForeignKey 
  # related to any override notification.model.
  template = models.ForeignKey( 
    swapper.get_model_name("txn_notifications", "Template"),
    on_delete=models.CASCADE,
    related_name="notifications",
  )
  
  class Meta(AbstractNotification.Meta):
    swappable = swapper.swappable_setting("txn_notifications", "Notification")
    abstract = False
```

```python
# email
DEFAULT_FROM_EMAIL = "Test <test@test.com>"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DJANGO_NOTIFICATIONS = {
  "email": {
    "enabled": False,
    # user model attribute
    "recipient_attr": "email",
    # templates
    "html_template": "notifications/templates/email.html",
    "txt_template": "notifications/templates/email.txt",
  },
  "twilio": {
    "enabled": False,
    "recipient_attr": None,
    # account settings
    "account_sid": None,
    "auth_token": None,
    "sms_sender": None,
  },
}
```

## Email
### settings
You can override it in the settings or in the `data` payload in the notification.

Using configurations:
```python
DJANGO_NOTIFICATIONS = {
    "email": {
        "enabled": False,
        "html_template": "notifications/templates/email.html",
        "txt_template": "notifications/templates/email.txt",
        "recipient_attr": "email",
    },
}
```

Using notification data:
```python
data = {
  # tempalte data (created by the template)
  "title": "",
  "body": "",
  "url": "",  # button url
  "url_msg": "",  # button copy
  # template data (optional)
  "prehead": "",  # optional
  "image": "url to the image",  # optional
  "image_alt": "",  # optional
  "intro": "",  # optional (before body)
  "outro": "",  # optional (after body)
  "footer": "",  # optional (outside the box)
  # or you can chage the email template
  "txt_template": "path/to/template.txt",
  "html_template": "path/to/template.html",
  # other options related to the email
  "bcc": [],
  "connection": None,
  "attachments": [],
  "headers": [],
  "alternatives": [],
  "cc": [],
  "reply_to": []
}
```

### Getting the recipient attr
You can chage the `recipient_attr` in the settings. This will try to get 
the attribute from the `User` model.

If that attribute comes from another model, or it must be calculated by a 
function, then you can override the `get_reecipient` function by extending 
from the `EmailHandler` or any other handler inherit from it.

```python
from txn_notifications.handlers.email import EmailHandler

class MyEmailHandler(EmailHandler):
  def get_recipient(self) -> list[str]:
    return self.user.settings.any_other_attribute
```

### Templates
If you want to use your own templates ...

1. Change `html_template` and `txt_template` in the settings or in the `data` 
   payload.
2. Set the django template tags `{{ title }}`, `{{ body }}`, etc.
3. Remember to validate inline your html/css.

**Inliners:**
https://templates.mailchimp.com/resources/inline-css/


## Check/update message status
### Callbacks
`notifications/callbacks/{callback_id}/`

* (`mailgun`) https://documentation.mailgun.com/en/latest/quickstart-events.html#events
  * https://www.mailgun.com/blog/product/a-guide-to-using-mailguns-webhooks/
* (`twillio`) https://www.twilio.com/docs/sms/tutorials/how-to-confirm-delivery-python

## Testing
1. Install pipenv
```sh
pip install pipenv
```
2. Install dependencies
```sh
pipenv install --dev
```
3. Run tests
```sh
pipenv run pytest --cov=txn_notifications .
```

### Runing Django
1. Run migrations
```sh
pipenv run python manage.py migrate
```
2. Create Super User
```sh
pipenv run python manage.py createsuperuser
```
3. Run server
```sh
pipenv run python manage.py runserver
```
4. Open admin
http://localhost:8000/admin/