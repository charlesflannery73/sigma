from django import forms


class TypeSearchForm(forms.Form):
    search_name = forms.CharField(
        required=False,
        label='Search sig type name',
        widget=forms.TextInput(attrs={'placeholder': 'search here'}),
    )

    search_comment = forms.CharField(
        required=False,
        label='comment'
    )


class SigSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Search sig text',
        widget=forms.TextInput(attrs={'placeholder': 'search here'}),
    )

    search_status = forms.CharField(
        required=False,
        label='status'
    )
    search_expiry = forms.CharField(
        required=False,
        label='expiry'
    )
    search_reference = forms.CharField(
        required=False,
        label='reference'
    )

    search_type = forms.CharField(
        required=False,
        label='type'
    )

    search_comment = forms.CharField(
        required=False,
        label='comment'
    )
