from django.template import Engine, Context
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import EmailTemplate


def send_templated_email(template_name, context, recipient_list, from_email, **kwargs):
    # Get template from database, render it using the provided context
    template_engine = Engine()
    email_template = EmailTemplate.objects.get(name=template_name)
    subject_template = template_engine.from_string(email_template.subject)
    body_template = template_engine.from_string(email_template.body)
    email_context = Context(context)
    email_subject = subject_template.render(email_context)
    email_body = body_template.render(email_context)
    email_body_full = render_to_string(
        'emails/default.html',
        context = {'rendered_email_body': email_body}
    )

    # Send the email
    text_message = strip_tags(email_body_full)
    send_mail(
        recipient_list = recipient_list,
        from_email = from_email,
        subject=email_subject,
        message = text_message,
        html_message = email_body_full,
        **kwargs
    )
