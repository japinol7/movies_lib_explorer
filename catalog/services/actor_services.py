from catalog.services.resource_services import save_picture_to_resource


def set_actor_external_data_fields(actor, ext_actor_data):
    actor.ext_name = ext_actor_data.get('name', '')
    actor.ext_birth_date = ext_actor_data.get('mlde_birth_date', '')
    actor.ext_death_date = ext_actor_data.get('mlde_death_date', '')
    actor.ext_place_of_birth = ext_actor_data.get('mlde_birth_place', '')
    actor.ext_biography = ext_actor_data.get('mlde_biography', '')
    actor.ext_picture_uri = ext_actor_data.get('mlde_im_profile_uri', '')
    actor.ext_tmdb_id = ext_actor_data.get('id', '')
    actor.ext_imdb_id = ext_actor_data.get('mlde_imdb_id', '')

    actor_name = str(actor.first_name).strip() + ' ' + str(actor.last_name).strip()
    actor_name = actor_name.strip()

    if actor_name and actor.ext_picture_uri:
        save_picture_to_resource(actor, actor.ext_picture_uri, actor_name)

    actor.save()
