curl -i http://127.0.0.1:8000/catalog/api/v1/actors \
-X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
-d @- << EOF
{
  "last_name": "Test-Actor-Last_Name",
  "first_name": "Test-Actor-First_Name"
}
EOF
