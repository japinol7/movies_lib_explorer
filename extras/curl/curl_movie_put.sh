curl -i http://127.0.0.1:8000/catalog/api/v1/movies/"$1" \
-X PUT \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
-d @- << EOF
{
  "title": "Test 2: A Story of Floating Weeds",
  "title_original": "Test 2: Ukikusa monogatari",
  "director": "4",
  "year": "1934",
  "runtime": "86",
  "country": "JP",
  "language": "Japanese",
  "cast": "Takeshi Sakamoto, Chōko Iida, Kōji Mitsui, Rieko Yagumo, Yoshiko Tsubouchi"
}
EOF
