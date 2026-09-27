from catalog.services.resource_services import save_picture_to_resource


def set_movie_external_data_fields(movie, ext_movie_data):
    movie.ext_title = ext_movie_data.get('title', '')
    movie.ext_orig_title = ext_movie_data.get('original_title', '')
    movie.ext_is_orig_title_diff = ext_movie_data.get('mlde_is_orig_title_diff', True)
    movie.ext_release_date = ext_movie_data.get('release_date', '')
    movie.ext_runtime = ext_movie_data.get('mlde_runtime', '')
    movie.ext_orig_lang = ext_movie_data.get('original_language', '')
    movie.ext_genres = ext_movie_data.get('mlde_genres', '')
    movie.ext_overview = ext_movie_data.get('overview', '')
    movie.ext_picture_uri = ext_movie_data.get('mlde_im_poster_uri', '')
    movie.ext_tmdb_id = ext_movie_data.get('id', '')
    movie.ext_imdb_id = ext_movie_data.get('mlde_imdb_id', '')

    if movie.ext_picture_uri:
        save_picture_to_resource(movie, movie.ext_picture_uri, movie.title)

    movie.save()
