curl -i http://127.0.0.1:8000/catalog/api/v1/directors \
-X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
--data-binary @- << EOF
{
  "last_name": "Test-Director-Last_Name", 
  "first_name": "Test-Director-First_Name"
}
EOF
