curl -i http://127.0.0.1:8000/catalog/api/v1/directors/"$1" \
-X DELETE \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
