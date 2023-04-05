from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            "post",
            "text",
            #"user"
        )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = _("Escribe tu comentario")
        self.fields['post'].widget = forms.HiddenInput()
        #self.fields['user'].widget = forms.HiddenInput()
