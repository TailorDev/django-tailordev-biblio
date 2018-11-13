from operator import methodcaller

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from td_biblio.models import Author

DOI_REGEX = r"(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&'<>])\S)+)"
doi_validator = RegexValidator(
    DOI_REGEX, _("One (or more) DOI is not valid"), "invalid"
)

PMID_REGEX = r"^-?\d+\Z"
pmid_validator = RegexValidator(
    PMID_REGEX, _("One (or more) PMID is not valid"), "invalid"
)


def text_to_list(raw):
    """Transform a raw text list to a python sorted object list
    Supported separators: coma, space and carriage return
    """
    return sorted(
        list(
            set(
                id.strip()
                for r in map(methodcaller("split", ","), raw.split())
                for id in r
                if len(id)
            )
        )
    )


class EntryBatchImportForm(forms.Form):

    pmids = forms.CharField(
        label=_("PMID"),
        widget=forms.Textarea(attrs={"placeholder": "ex: 26588162, 19569182"}),
        help_text=_(
            "Paste a list of PubMed Identifiers " "(comma separated or one per line)"
        ),
        required=False,
    )

    dois = forms.CharField(
        label=_("DOI"),
        widget=forms.Textarea(
            attrs={"placeholder": "ex: 10.1093/nar/gks419, 10.1093/nar/gkp323"}
        ),
        help_text=_(
            "Paste a list of Digital Object Identifiers "
            "(comma separated or one per line)"
        ),
        required=False,
    )

    def clean_pmids(self):
        """Transform raw data in a PMID list"""
        pmids = text_to_list(self.cleaned_data["pmids"])
        for pmid in pmids:
            pmid_validator(pmid)
        return pmids

    def clean_dois(self):
        """Transform raw data in a DOI list"""
        dois = text_to_list(self.cleaned_data["dois"])
        for doi in dois:
            doi_validator(doi)
        return dois

    def clean(self):
        super(EntryBatchImportForm, self).clean()

        dois = self.cleaned_data.get("dois", [])
        pmids = self.cleaned_data.get("pmids", [])

        if not len(dois) and not len(pmids):
            raise forms.ValidationError(
                _("You need to submit at least one valid DOI or PMID")
            )


class AuthorDuplicatesForm(forms.Form):
    def get_authors_choices():
        return Author.objects.values_list("id", "last_name")

    authors = forms.MultipleChoiceField(
        label=_("Authors pool"),
        help_text=_("Authors to merge"),
        choices=get_authors_choices,
    )

    alias = forms.ChoiceField(
        label=_("Target author"),
        help_text=_("Reference author for which we will define aliases"),
        choices=get_authors_choices,
    )

    def clean_authors(self):
        authors = self.cleaned_data["authors"]
        return Author.objects.filter(id__in=authors)

    def clean_alias(self):
        alias = self.cleaned_data["alias"]
        return Author.objects.get(id=alias)

    def clean(self):
        super(AuthorDuplicatesForm, self).clean()

        authors = self.cleaned_data.get("authors", [])
        alias = self.cleaned_data.get("alias", None)

        if alias in authors:
            raise forms.ValidationError(
                _("Target author cannot be part of the selection")
            )
