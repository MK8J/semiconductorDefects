1. Install act https://github.com/nektos/act

> Note: the default environment installed by act does not match the one used in gihub actions. To emulate it more accurately you will need to pull one of the images at: https://hub.docker.com/r/nektos/act-environments-ubuntu/tags eg. `docker pull nektos/act-environments-ubuntu:18.04`

2. Set the environment variables defects_username and defects_password

3. Run act in this repository referencing the image pulled in the previous step eg. `act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --secret defects_username --secret defects_password`

> (Optional - use a .env file in .github/workflows to define the environment variables and run `export $(xargs < .github/workflows/.env)` to load them   )