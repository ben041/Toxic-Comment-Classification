from django import forms

class ToxicCommentForm(forms.Form):
    comment = forms.CharField(
        label="Enter a comment",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 50}),
        max_length=500,
    )
