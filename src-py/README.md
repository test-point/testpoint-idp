# idp.testpoint.io
Our Python implementation of an e-business identity provider using Open ID Connect protocol.

Purpose of having our own IDP is so that we can quickly iterate authorisation scopes for testing and development. Target architecture will outsource IDP to alternate provider(s).

While doing local testing it's vital to have same domains for service and service configuration. For example. 0:7500 and 127.0.0.1:7500 and localhost:7500 are the different for OIDC, so auth most likely will fail if request from one domain has redirect_url to another.

Also www.idp.testpoint.io and idp.testpoint.io have the same problem (might need do forced 302 redirect from www. non-www)

Please use non-www version with any our installation.

## Start locally

To start it locally just create and activate the virtualenv, install requirements from requirements.txt file and run `./src/manage.py runserver 0:7500` (or any other port/host).
To prepare the valid database you need to run next steps (only first time for each database):

    ./manage.sh migrate
    ./manage.sh createsuperuser
    ./manage.sh creatersakey

It's handy to use manage.sh script, which will activate the virtualenv and start django project for you with desired parameters (check manage.sh.sample, rename it and update for your needs).


## Docker deployments

First copy env.example to idp-testpoint.env file and alter it. It assumes the remote Postgres installation, but you may alter the dockerfile to create some postgres container there and point to it instead.

Then:

`docker-compose up`

This will listen the port mentioned in the docker-compose.yml file (default is 8810) with the service started.
