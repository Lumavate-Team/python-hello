


@echo off
REM for /f %%i in ('docker-machine ip') do set DOCKER_IP=%%i

REM @echo Current Docker IP is: %DOCKER_IP%

@echo Welcome to the Lumavate WidgetToolkit!

@echo --------------------------------------
@echo:
@echo: 
set /p DOCKER_IP="Please enter your Machine's Base IP Address:"
@echo:
@echo: 
set /p WIDGET_IMAGENAME="Enter your Widget Image name:"
@echo:
@echo:
set /p WIDGET_PORT="Enter the widget's port (4200, 5000, etc):"

@echo:
@echo:
@echo:
REM for /f %%j in ('docker ps -q -f name=thor') do set THOR=%%j


REM if THOR (
	
	@echo Stopping Thor....
	
	docker stop thor

REM )


REM for /f %%h in ('docker ps -q -f name=widget') do set WIDGET=%%h


REM if WIDGET (	
	@echo Stopping Widget....

	docker stop widget

REM )

@echo:
@echo:
@echo Running your Widget Container

@echo ---------------------------------------
docker run --rm -d -e "PRIVATE_KEY=LXycaMpw5BzgfhsS4ydNxGzJ36qMnPrQHI8u2x3wQCZCZyGtZ4sOQbkEWnHmVchZEa79a0Y3xK7IKCymSLkugyabbJUGuXfyuoKL" -e "PUBLIC_KEY=mIhuoMJh0jbA5W4pUUNK" -e "APP_SETTINGS=./config/dev.cfg" -e "BASE_URL=http://%DOCKER_IP%" -e "PROTO=http://" --name=widget -p %WIDGET_PORT%:%WIDGET_PORT% %WIDGET_IMAGENAME%
@echo:
@echo:

@echo Running the Widget Toolkit
@echo ---------------------------------------
docker run --rm -d -e "PUBLIC_KEY=mIhuoMJh0jbA5W4pUUNK" -e "PRIVATE_KEY=LXycaMpw5BzgfhsS4ydNxGzJ36qMnPrQHI8u2x3wQCZCZyGtZ4sOQbkEWnHmVchZEa79a0Y3xK7IKCymSLkugyabbJUGuXfyuoKL" -e "HOST_IP=%DOCKER_IP%" -e "WIDGET_PORT=%WIDGET_PORT%" --name=thor -p 80:4201 quay.io/lumavate/thor:latest

@echo:

@echo ----------------------------------------------------------------------------------

@echo:

@echo Open a browser and navigate to http://%DOCKER_IP%/admin to test your widget

@echo *NOTE: It might take some time for the containers to fully load*
@echo Use the command 'docker logs widget -f' to view the current widget logs

@echo:
