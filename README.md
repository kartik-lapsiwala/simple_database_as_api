# simple_database_as_api
basic application of database as api service using docker.

This api can store any sentence a user enters.

To run this api you need to install docker and docker compose on your machine and run the following commands.

>sudo docker-compose build.

this command will install the required packages and libraries.

>docker-compose up

the api will be hosted on 0.0.0.0:5000 using this command.

This api has 3 end points.

1) /register
2) /store
3) /retrieve

register accepts username and passwords as arguments.

store accepts username, password and store as arguments.

retireve accepts username and passwords as arguments.
