curl -i http://127.0.0.1:8000/catalog/api/v1/movies \
-X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: Token '$MLME_REST_API_TOKEN \
-d @- << EOF
{
  "title": "Test: A Story of Floating Weeds",
  "title_original": "Test: Ukikusa monogatari",
  "director": "4",
  "year": "1934",
  "runtime": "86",
  "country": "JP",
  "language": "Japanese",
  "cast": "Takeshi Sakamoto, Chōko Iida, Kōji Mitsui, Rieko Yagumo, Yoshiko Tsubouchi"
}
EOF
