from operator import methodcaller

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


DOI_REGEX = '(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)'
doi_validator = RegexValidator(
    DOI_REGEX,
    _("One (or more) DOI is not valid"),
    'invalid'
)

PMID_REGEX = '^-?\d+\Z'
pmid_validator = RegexValidator(
    PMID_REGEX,
    _("One (or more) PMID is not valid"),
    'invalid'
)


def text_to_list(raw):
    """Transform a raw text list to a python object list
    Supported separators: coma, space and carriage return
    """
    return list(set(
        id.strip()
        for r in map(methodcaller('split', ','), raw.split())
        for id in r
        if len(id)
    ))


class EntryBatchImportForm(forms.Form):

    pmids = forms.CharField(
        label=_("PubMed identifiers"),
        widget=forms.Textarea(
            attrs={
                'placeholder': "26588162\n19569182"
            }
        ),
        help_text=_("Comma separated or one per line"),
        required=False,
    )

    dois = forms.CharField(
        label=_("Digital object identifiers (DOIs)"),
        widget=forms.Textarea(
            attrs={
                'placeholder': "10.1093/nar/gks419\n10.1093/nar/gkp323"
            }
        ),
        help_text=_("Comma separated or one per line"),
        required=False,
    )

    def clean_pmids(self):
        """Transform raw data in a PMID list"""
        pmids = text_to_list(self.cleaned_data['pmids'])
        for pmid in pmids:
            pmid_validator(pmid)
        return pmids

    def clean_dois(self):
        """Transform raw data in a DOI list"""
        dois = text_to_list(self.cleaned_data['dois'])
        for doi in dois:
            doi_validator(doi)
        return dois
