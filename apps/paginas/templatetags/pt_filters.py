from django import template

register = template.Library()


@register.filter
def pesos(value):
    """Formatea un numero como precio CLP: $10.590"""
    try:
        v = int(round(float(str(value).replace(',', ''))))
        return f"${v:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
