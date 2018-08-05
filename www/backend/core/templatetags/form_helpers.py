from django.template.library import Library

register = Library()


@register.inclusion_tag('partials/forms/non-field-errors.html')
def non_field_errors(form):
    return {'form': form}
