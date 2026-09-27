from catalog.services.resource_services import save_picture_to_resource


def set_director_external_data_fields(director, ext_director_data):
    director.ext_name = ext_director_data.get('name', '')
    director.ext_birth_date = ext_director_data.get('mlde_birth_date', '')
    director.ext_death_date = ext_director_data.get('mlde_death_date', '')
    director.ext_place_of_birth = ext_director_data.get('mlde_birth_place', '')
    director.ext_biography = ext_director_data.get('mlde_biography', '')
    director.ext_picture_uri = ext_director_data.get('mlde_im_profile_uri', '')
    director.ext_tmdb_id = ext_director_data.get('id', '')
    director.ext_imdb_id = ext_director_data.get('mlde_imdb_id', '')

    director_name = str(director.first_name).strip() + ' ' + str(director.last_name).strip()
    director_name = director_name.strip()

    if director_name and director.ext_picture_uri:
        save_picture_to_resource(director, director.ext_picture_uri, director_name)

    director.save()
