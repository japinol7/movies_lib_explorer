# To put in static/js directory

wget -O bootstrap-5.3.8.bundle.min.js \
  https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js

## htmx downloaded manually from
# https://htmx.org/
# https://cdn.jsdelivr.net/npm/htmx.org/dist/
#
# Check in the future when it is a good moment to make the major htmx upgrade to v. 4.x
# $ grep -RniE 'hx-|htmx|HX-' templates/
#
#wget -O htmx-2.0.11.min.js \
#  https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.js
#
#wget -O htmx-2.0.11.min.js \
#  https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js
#
#wget -O htmx-4.0.0.min.js \
#  https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/htmx.js
#
#wget -O htmx-4.0.0.min.js \
#  https://cdn.jsdelivr.net/npm/htmx.org@4.0.0/dist/htmx.min.js

# jquery is not needed in new MLME versions
#wget -O jquery-3.7.1.slim.min.js \
#  https://code.jquery.com/jquery-3.7.1.slim.min.js

# To put in static/css directory
wget -O bootstrap-5.3.8.min.css \
  https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css
