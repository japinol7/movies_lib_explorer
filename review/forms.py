from django.forms import ModelForm

from review.models.review import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'text')
