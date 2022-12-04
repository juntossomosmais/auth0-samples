#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# -e  Exit immediately if a command exits with a non-zero status.
# -x Print commands and their arguments as they are executed.
set -e

# You should run the command at the root folder of `auth0-infrastructure` project
npm run deploy:sandbox

# When running through Compose, you'll be able to configure `.env.development` variable of `apiview_django_rest_framework` project
python scripts/env_setter.py
