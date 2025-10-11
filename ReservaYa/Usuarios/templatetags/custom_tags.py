import random
from django import template

register = template.Library()

@register.filter
def random_color(value):
    random.seed(value)
    colors = ['#f87171', '#fbbf24', '#34d399', '#60a5fa', '#a78bfa', '#f472b6', '#facc15']
    return random.choice(colors)