curl -i "http://127.0.0.1:8000/catalog/api/v1/movies?year="$1"&ordering=director__last_name,director__first_name" \
-H 'Authorization: Token '$MLME_REST_API_TOKEN
