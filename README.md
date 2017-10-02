# iot-project-scaffolding

Use this project as a starting point for creating a new iot angular2/python microservice.

## Setup

#### Cloning the Repo

* Clone it.  `git clone git@github.com:LabelNexus/iot-project-scaffolding.git <PROJECT_NAME>`
* Switch to dir.  `cd <PROJECT_NAME>`
* Remove remote origin. `git remote remove origin`
* Create new <PROJECT_NAME> repository in github.
* Add the new origin pointing to <PROJECT_NAME>.  `git remote add origin git@github.com:LabelNexus/<PROJECT_NAME>.git`
* Push everything to <PROJECT_NAME> repository.  `git push -u origin master`

#### Adding Shared Projects

From <PROJECT_NAME> root directory.

* Add python iot_api_core - `git subtree add --prefix=app/iot_api_core git@github.com:LabelNexus/iot_api_core.git master --squash`
* Add angular2 iot-core - `git subtree add --prefix=src/iot-core git@github.com:LabelNexus/iot-core.git master --squash`

#### Replace <PROEJCT_NAME> References With Your Project Name

* Dockerfile
* supervisor.dev.conf
* app/config/(dev.cfg|staging.cfg)
* app/behavior/instance_version.py
* src/app/index.html
* .angular-cli.json

#### NPM Install

Run `npm install` in your projects working directory.

#### Build <PROJECT_NAME> Docker Image

* Naviagte to <PROJECT_NAME> root directory
* Build your docker image by running the following command. `docker build -t deathstar.labelnexusdev.com/iot-<PROJECT_NAME>:develop .`

#### Add docker-compose Configuration

Copy an existing iot-<PROJECT_NAME> configuration from callisto/docker-compose.yml and make the appropriate changes.

#### HAProxy Configuration

###### Dev Configuration

* Open haproxy.cfg from reverse_flash
* All of the end user iot projects configuration should be identical with a varying <PROJECT_NAME> so copying any should work.
* Add new acl, use_backend check, and backend from a copy of another iot end user project
* Replace <PROJECT_NAME> with your project.

###### Staging/Production Consul Template Configuration

* Open haproxy.cfg.ctmpl.j2 from reverse_flash
* All of the end user iot projects configuration should be identical with a varying <PROJECT_NAME> so copying any should work.
* Add a new service entry to the services list (e.g.
	`{ "name": "iot_<PROJECT_NAME>", "acl": "path_sub /iot/<PROJECT_NAME>", "port": 4200, "rewrite": "reqrep ^([^\ ]*\ /[^/]*)\/?iot\/<PROJECT_NAME>(\/.*)? \\1\\2"}`)
* Replace <PROJECT_NAME> with your project.

###### HAProxy Docker Image

* Navigate to reverse-flash root directory
* Rebuild reverse-flash docker image to pickup config file changes. `docker build -t deathstar.labelnexusdev.com/reverse-flash:develop .`
* Run `docker-compose rm reverse-flash` to always make sure you have the latest config changes.

## Trying it Out

At this point you should be able to switch over the the callisto directory and run a `docker-compose up`.  Then naviage to your project's url and receive the
"Welcome to the app page".

Example url: [http://toyota-test.sites.sean.labelnexusdev.com:8083/1550ef7f71de/iot/<PROJECT_NAME>/1/]

## Making iot-core Project Changes - Performing Subtree Pull/Push Steps

Any changes made to the iot-core project subtree under src/iot-core needs to be pushed/pulled following these steps.

* ALWAYS make sure you perform these actions on the develop branch. DO NOT perform subtree actions on a feature or short lived branch. It can cause bad things
to happen.
* Commit and push all of your normal iot project changes up to origin/develop. `git push`
* Now make sure you have the latest commits from iot-core subtree. `git subtree pull --squash --prefix=src/iot-core
git@github.com:LabelNexus/iot-core.git master`
* Resolve any merge conflicts that may have occurred (it normally goes smoothly)
* Next push all changes from the iot-core subtree up to iot-core/master. `git subtree push --prefix=src/iot-core
git@github.com:LabelNexus/iot-core.git master`
* Then turn around and pull the commit hash you just created by pulling into our local iot-core subtree instance. `git subtree pull --squash --prefix=src/iot-core
git@github.com:LabelNexus/iot-core.git master`
* Add any additional commit message you see fit (the default is normally fine)
* Finally push the local subtree commit changes up to origin/develop. `git push`

After that process has completed you need to go to each of the projects below (or any iot based project not listed) and pull the latest subtree changes.

iot-support, iot-items, iot-gallery, iot-content, iot-apps, iot-page, iot-location

* Run this command at the project root. `git subtree pull --squash --prefix=src/iot-core git@github.com:LabelNexus/iot-core.git master`
* Add any additional commit message you see fit (the default is normally fine)
* Push the local subtree commit changes up to origin/develop.

