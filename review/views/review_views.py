from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from catalog.models.movie import Movie
from review.forms import ReviewForm
from review.models.review import Review


@login_required
def review_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        try:
            review = Review.objects.get(movie=movie, user=request.user)
            form = ReviewForm(request.POST, instance=review)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('catalog:movie', movie_id=movie.id)

        # Form not valid, re-render with errors
        data = {
            'movie': movie,
            'form': form,
        }
        return render(request, 'review/review.html', data)

    # GET method
    try:
        review = Review.objects.get(movie=movie, user=request.user)
        form = ReviewForm(instance=review)
    except Review.DoesNotExist:
        form = ReviewForm()

    data = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'review/review.html', data)
