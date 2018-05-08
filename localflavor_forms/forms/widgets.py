from django_countries.widgets import LazySelect
from django.utils.safestring import mark_safe
from django_countries import settings
from urllib import parse as urlparse
from django.utils.html import escape

COUNTRY_CHANGE_HANDLER = (
    "var e=document.getElementById('flag_' + this.id); "
    "if (e) e.src = '%s'"
    ".replace('{code}', this.value.toLowerCase() || '__')"
    ".replace('{code_upper}', this.value.toUpperCase() || '__');"
    "this.options[this.selectedIndex].value && (window.location = window.location.origin + '/' + this.options[this.selectedIndex].value) +'/';"
)

class CountrySelectWidget(LazySelect):
    def __init__(self, *args, **kwargs):
        self.layout = kwargs.pop('layout', None) or (
            '{widget}<img class="country-select-flag" id="{flag_id}" '
            'style="margin: 6px 4px 0" '
            'src="{country.flag}">'
        )
        super(CountrySelectWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):

        from django_countries.fields import Country
        attrs = attrs or {}
        widget_id = attrs and attrs.get('id')
        if widget_id:
            flag_id = 'flag_{id}'.format(id=widget_id)
            attrs['onchange'] = COUNTRY_CHANGE_HANDLER % urlparse.urljoin(
                settings.STATIC_URL, settings.COUNTRIES_FLAG_URL)
        else:
            flag_id = ''
        # Renderer argument only added in 1.11, keeping backwards compat.
        kwargs = {'renderer': renderer} if renderer else {}
        widget_render = super(CountrySelectWidget, self).render(
            name, value, attrs, **kwargs)
        if isinstance(value, Country):
            country = value
        else:
            country = Country(value or '__')
        with country.escape:
            return mark_safe(self.layout.format(
                widget=widget_render, country=country,
                flag_id=escape(flag_id)))