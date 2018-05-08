import re

# from dojango import forms
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

class INMobilePhoneNumberField(forms.CharField):
    """
    INMobilePhoneNumberField validates that the data is a valid Indian mobile
    phone number. All mobile numbers in India are 10 digits long and have the
    prefix 9, 8 or 7.
    """
    default_error_messages = {
        'invalid': _('Mobile Phone numbers must be 10 digits long and have the prefix 9, 8 or 7.'),
    }

    def clean(self, value):
        value = super(INMobilePhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''

        phone_digits_re = re.compile(r"(?P<phone_no>^[7-9]\d{9})$", re.VERBOSE)

        value = smart_text(value)
        m = phone_digits_re.match(value)
        if m:
            return '%s' % (value)
        raise ValidationError(self.error_messages['invalid'])

class LocalField(object):

    def __init__(self, country='US'):
        self.country = country

        self.country_lower = country.lower()
        self.country_upper = country.upper()

        # Import localflavor module
        try:
            self.localflavor = __import__("localflavor." + self.country_lower + '.forms')
        except ImportError:
            # Retry with underscore prefixed country_lower
            self.country_lower += '_'
            try:
                self.localflavor = __import__("localflavor." + self.country_lower + '.forms')
            except ImportError:
                # If no local flavor module found for country, return regular forms module
                self.forms_module = forms
                return


        self.country_module = getattr(self.localflavor, self.country_lower)
        self.forms_module = getattr(self.country_module, 'forms')

    def get(self, field_name, default_field=forms.CharField, auto_hide=True, *args,
            **kwargs):
        """
        Returns localflavor.<country>.forms.<field_name> if found, else returns
        default_field
        """
        try:
            return getattr(self.forms_module, self.country_upper + field_name)(*args, **kwargs)
        except AttributeError:
            if auto_hide and not 'widget' in kwargs:
                # if no widget is defined, assign HiddenInput widget
                kwargs['widget'] = HiddenInput
            return default_field(*args, **kwargs)

    def select_field(self, name, auto_hide=True, *args, **kwargs):
        """
        When a localflavor.<country>.forms.<name>Select widget is found returns
        a FilteringSelect field with the Select widgets choices, else returns
        a CharField.
        """
        try:
            select_widget = getattr(self.forms_module, self.country_upper + name + 'Select')()
            #kwargs['widget'] = forms.FilteringSelect
            choices = list(select_widget.choices)
            choices.insert(0, ('', '')) # Adding blank option
            kwargs['choices'] = choices
            return forms.ChoiceField(**kwargs)
        except AttributeError:
            pass

        return self.get(name + 'Field', auto_hide=auto_hide, *args, **kwargs)

    # Shortcut methods
    def state_field(self, *args, **kwargs):
        # Austria(AT), Australia(AU), Brazil(BR), Switzerland(CH), Germany(DE),
        # India(IN), Mexico(MX), USA(US)
        return self.select_field('State', *args, auto_hide=True, **kwargs)

    def department_field(self, *args, **kwargs):
        # Columbia(CO), France(FR), Paraguay(PY), Urguay(UY)

        return self.select_field('Department', *args, auto_hide=True, **kwargs)

    def district_field(self, *args, **kwargs):
        # Slovakia(SK)
        return self.select_field('District', *args, auto_hide=True, **kwargs)

    def prefecture_field(self, *args, **kwargs):
        # Japan(JP)
        return self.select_field('Prefecture', *args, auto_hide=True, **kwargs)

    def province_field(self, *args, **kwargs):
        # Argentina(AR), Belgium(BE), Canada(CA), China(CN), Ecuador(EC),
        # Spain(ES), Indonesia(ID), Italy(IT), Netherlands(NL), Poland(PL),
        # Turkey(TR), South Africa(ZA)
        return self.select_field('Province', *args, auto_hide=True, **kwargs)

    def region_field(self, *args, **kwargs):
        # Belgium(BE), Chile(CL), Czech Republic(CZ), Spain(ES), France(FR),
        # Italy(IT), Peru(PE), Portugal(PT), Russia(RU), Slovakia(SK)
        return self.select_field('Region', *args, auto_hide=True, **kwargs)

    def municipality_field(self, *args, **kwargs):
        # Finnland(FI), Lithuania(LT), Macedonia(MK), Norway(NO)
        return self.select_field('Municipality', *args, auto_hide=True, **kwargs)

    def county_field(self, *args, **kwargs):
        # Great Britain(GB), Croatia(HR), Ireland(IE), Lithuania(LT),
        # Poland(PL), Romania(RO), Russia(RU), Sweden(SE)

        return self.select_field('County', *args, auto_hide=True, **kwargs)

    def nation_field(self, *args, **kwargs):
        # Great Britain(GB),
        return self.select_field('Nation', *args, auto_hide=True, **kwargs)

    def postal_code_field(self, *args, **kwargs):

        # Austria(AT), Brazil(BR), Switzerland(CH), Germany(DE), Finnland(FI),
        # France(FR), India(IN), Italy(IT), Mexico(MX), Netherlands(NL),
        # Norway(NO), Portugal(PT), USA(US)

        zip_code_countries = ['AT', 'BR', 'CH', 'DE', 'FI', 'FR', 'IN', 'IT',
                              'MX', 'NL', 'NO', 'PT', 'US']

        # Argentina(AR), Belgium(BE), Canada(CA), Czech Republic(CZ), Spain(ES),
        # Croatia(HR), Israel(IL), Japan(JP), Lithuania(LT), Poland(PL),
        # Romania(RO), Russia(RU), Sweden(SE), Slovenia(SI), Slovakia(SK),
        # Turkey(TR)
        postal_code_countries = ['AR', 'BE', 'CA', 'CZ', 'ES', 'HR', 'IL', 'JP',
                                 'LT', 'PL', 'RO', 'RU', 'SE', 'SI', 'SK', 'TR']

        # Australia(AU), China(CN), Indonesia(ID), South Africa(ZA)
        post_code_countries = ['AU', 'CN', 'ID', 'ZA']

        # Great Britain(GB)
        postcode_countries = ['GB']

        # Iceland(IS), Slovenia(SI)
        postal_code_select_countries = ['IS', 'SI']

        kwargs["widget"] = forms.widgets.TextInput#forms.ValidationTextInput

        if self.country_upper in postal_code_select_countries:
            return self.get('PostalCodeSelect', *args, **kwargs)

        if self.country_upper in zip_code_countries:
            return self.get('ZipCodeField', *args, **kwargs)

        if self.country_upper in postal_code_countries:
            return self.get('PostalCodeField', *args, **kwargs)

        if self.country_upper in post_code_countries:
            return self.get('PostCodeField', *args, **kwargs)

        if self.country_upper in postcode_countries:
            return self.get('PostcodeField', *args, **kwargs)

        #default
        return forms.CharField(*args, **kwargs)

    def phone_number_field(self, *args, **kwargs):
        kwargs["widget"] = forms.widgets.TextInput#forms.ValidationTextInput

        if self.country_upper == 'LT':# Lithuania(LT)
            return self.get('PhoneField', auto_hide=False, *args, **kwargs)

        # Australia(AU), Belgium(BE), Brazil(BR), Canada(CA), Switzerland(CH),
        # China(CN), Spain(ES), France(FR), Hong Kong(HK), Croatia(HR),
        # Indonesia(ID), India(IN), Iceland(IS), Netherlands(NL), Norway(NO),
        # Portugal(PT), Romania(RO), Slovenia(SI), Turkey(TR), USA(US)
        return self.get('PhoneNumberField',  *args, **kwargs)

    def mobile_phone_number_field(self, *args, **kwargs):
        kwargs["widget"] = forms.widgets.TextInput#forms.ValidationTextInput
        if self.country_upper == 'CN': # China(CN)
            return self.get('CellNumberField', auto_hide=False, *args, **kwargs)
        # Israel(IL),
        if self.country_upper == 'IL': # Israel(IL)
            return self.get('MobilePhoneNumberField', auto_hide=False, *args,
                            **kwargs)
        # India(IN),
        if self.country_upper == 'IN': # India(IN)
            return INMobilePhoneNumberField(*args, **kwargs)

        return self.phone_number_field(*args, **kwargs)












