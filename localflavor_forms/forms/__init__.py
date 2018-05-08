from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy
from .local_fields import LocalField
from django_countries.fields import CountryField
from .widgets import CountrySelectWidget

class AddressForm(forms.Form):
    id = forms.fields.CharField(
        label = ugettext_lazy("ID"),
        required = False,
        widget = forms.widgets.HiddenInput
    )

    country = CountryField().formfield(widget=CountrySelectWidget())

    street_address = forms.fields.CharField(
        label = ugettext_lazy('Street Address'),
        required = False
    )

    post_office_box = forms.fields.CharField(
        required = False,
        label = ugettext_lazy('Post Office Box')
    )
    city = forms.fields.CharField(
        label = ugettext_lazy('City'),
        required = False
    )

    state = forms.fields.ChoiceField(
        label = ugettext_lazy('State')
    )

    department = forms.fields.ChoiceField(
        label = ugettext_lazy('Department')
    )

    district = forms.fields.ChoiceField(
        label = ugettext_lazy("District")
    )

    prefecture = forms.fields.ChoiceField(
        label = ugettext_lazy("Prefecture")
    )

    province = forms.fields.ChoiceField(
        label = ugettext_lazy("Province")
    )

    region = forms.fields.ChoiceField(
        label = ugettext_lazy("Region")
    )

    municipality = forms.fields.ChoiceField(
        label = ugettext_lazy("Municipality")
    )

    nation = forms.fields.ChoiceField(
        label = ugettext_lazy("Nation")
    )

    postal_code = forms.TextInput()

    phone1 = forms.fields.TextInput()
    phone2 = forms.fields.TextInput()
    fax = forms.fields.TextInput()

    class Meta:
        # model = models.Address
       
        fields = (
            'id',
            'country',
            'street_address',
            'post_office_box',
            'city',
            'state',
            'department',
            'district',
            'prefecture',
            'province',
            'region',
            'municipality',
            'nation',
            'county',
            'postal_code',
            'phone1',
            'phone2',
            'fax'
        )

    def __init__(self, *args, **kwargs):
        country_code = kwargs.pop('country_code', 'US')

        super(AddressForm, self).__init__(*args, **kwargs)
        
        # LocalField generator instance
        local_field = LocalField(country_code)

        # Override default fields with LocalFlavor Fields
        self.fields['country'].initial = country_code

        self.fields['state'] = local_field.state_field(
            required = False,
            label = ugettext_lazy('State')
        )

        # # To handle possible required state in LocationAddressForm
        # if type(self.fields['state']) != type(state_field):
        #     self.fields['state'] = state_field


        self.fields['department'] = local_field.department_field(
            required = False,
            label=ugettext_lazy('Department')
        )

        self.fields['district'] = local_field.district_field(
            required = False,
            label=ugettext_lazy('District')
        )

        self.fields['prefecture'] = local_field.prefecture_field(
            required = False,
            label=ugettext_lazy('Prefecture')
        )

        self.fields['province'] = local_field.province_field(
            required = False,
            label=ugettext_lazy('Province')
        )

        self.fields['region'] = local_field.region_field(
            required = False,
            label=ugettext_lazy('Region')
        )

        self.fields['municipality'] = local_field.municipality_field(
            required = False,
            label=ugettext_lazy('Municipality')
        )

        self.fields['county'] = local_field.county_field(
            required = False,
            label=ugettext_lazy('County')
        )

        self.fields['nation'] = local_field.nation_field(
            required = False,
            label=ugettext_lazy('Nation')
        )

        self.fields['postal_code'] = local_field.postal_code_field(
            required=False,
            label=ugettext_lazy('Postal Code / Zip Code')
        )

        self.fields['phone1'] = local_field.phone_number_field(
            required=False,
            label=ugettext_lazy('Phone Number')
        )

        if country_code in ['CN', 'IL', 'IN']:
            phone2_label = ugettext_lazy('Mobile/Cell Number')
        else:
            phone2_label = ugettext_lazy('Alternate Phone Number')

        self.fields['phone2'] = local_field.mobile_phone_number_field(
            required=False,
            label=phone2_label
        )

        self.fields['fax'] = local_field.phone_number_field(
            required = False,
            label=ugettext_lazy("Fax")
        )

        
