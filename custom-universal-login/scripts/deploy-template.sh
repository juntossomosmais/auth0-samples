#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

# Create out folder
npx parcel build --no-source-maps --dist-dir out --public-url "https://$BUCKET_NAME.s3.amazonaws.com/$BUCKET_ENVIRONMENT_PATH/"

# May create the bucket, and then it's going to upload the static files to it.
# After that, it's going to update the HTML file with the correct address for the assets, and finally upload it to Auth0.
python manage.py

