from django.shortcuts import render
from . import forms
from django.http import HttpResponseRedirect

# Create your views here.
def get_address_form(request, country_code='US'):
    # if this is a POST request we need to process the form data

    # country_code = request.GET.get("country_code", 'US')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.AddressForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.AddressForm(country_code=country_code)

    return render(request, 'address_form.html', {'form': form})
