from mad_notifications.models import get_email_template_model
from mad_notifications.notification import Notification


def newNotification(user, title, content, template_slug = None, data = {}, actions = {}):
    """
    Shorthand method to create and send notification
    """
    # get email template from db
    try:
        if template_slug is not None:
            email_template = get_email_template_model().objects.get(slug=template_slug)
            email_template = email_template
        else:
            raise
    except:
        email_template = None

    # create a notification for user
    notification = Notification(
        user = user,
        title = title,
        content = str(content),
        template = email_template,
        data = data,
        actions = actions,
    )

    return notification.notify()