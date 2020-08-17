# Movie List

## Prerequisite to run the application

* Docker

## To start the apps 

* Build the docker image

```sh
docker build -t movie-list .
```
* Start the application 

```sh
docker run -it -p 8000:8000 --rm movie-list
```