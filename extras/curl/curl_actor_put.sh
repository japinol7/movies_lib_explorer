curl -i http://127.0.0.1:8000/catalog/api/v1/actors/"$1" \
-X PUT \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
-d @- << EOF
{
  "last_name": "Test-Actor-Last_Name Updated",
  "first_name": "Test-Actor-First_Name Updated"
}
EOF
