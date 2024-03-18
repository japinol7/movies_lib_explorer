curl -i http://127.0.0.1:8000/catalog/api/v1/directors/"$1" \
-X PUT \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
-d @- << EOF
{
  "last_name": "Test-Director-Last_Name Updated",
  "first_name": "Test-Director-First_Name Updated"
}
EOF
