#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
set -eu -o pipefail

# Create out folder
npx parcel build --public-url "https://$BUCKET_NAME.s3.amazonaws.com/$BUCKET_ENVIRONMENT_PATH/"

# May create the bucket, and then it's going to upload the static files to it.
# After that, it's going to update the HTML file with the correct address for the assets, and finally upload it to Auth0.
python manage.py

