from django import template
from django.utils.safestring import mark_safe
import hashlib

register = template.Library()
PALETTE = [
    '#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e',
    '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#2c3e50',
    '#f39c12', '#d35400', '#c0392b'
]
@register.simple_tag
def avatar_svg(user, size=64):
# Si el usuario tiene imagen, la plantilla mostrará la imagen. Esta tag devuelve SVG para fallback.
    source = (user.email or user.username or 'user').encode('utf-8') 
    h = hashlib.md5(source).hexdigest()
    color = PALETTE[int(h, 16) % len(PALETTE)]
    letter = (user.get_initial() if hasattr(user, 'get_initial') else (user.username[0].upper()))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}"> <rect width="100%" height="100%" rx="{int(size*0.15)}" fill="{color}" /><text x="50%" y="50%" dy="0.35em" text-anchor="middle" fontfamily="Arial, Helvetica, sans-serif" font-size="{int(size*0.45)}" fill="#ffffff">{letter}</text></svg>'''
    return mark_safe(svg)