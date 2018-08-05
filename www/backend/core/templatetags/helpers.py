from django.template.library import Library

register = Library()


@register.inclusion_tag('partials/small-space.html')
def small_space(**kwargs):
    return kwargs


@register.inclusion_tag('partials/message_alerts.html')
def message_alerts(messages):
    return {'messages': messages}
