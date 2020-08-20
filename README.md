# Movie List

## Prerequisite to run the application

* Docker & Docker Compose

## To start the apps 

* Build the docker images

```sh
docker-compose build
```

* Start the application 

```sh
docker-compose up 
```

Now the app is available at [`localhost:8000`](http://localhost:8000)

## General Functionning

The application is connected to a `memcached` server from which the data to be displayed on the web page is fetched anytime the `localhost:8000/movies` endpoint is hit

On startup of the application a request is sent to the Studio Ghibli movie API. The data retrieved from that first API call is used to warmup the cache. If that request fails, our application will also fail to start as there is no data to be served on the page and this may denote an issue with the Studio Ghibli movie API. A retry policy can be implemented to mitigate possible network issues.

The cache is continuously updated by a background thread that periodically - 1 minute interval - accesses the Studio Ghibli movie API and retrieves updated data ensuring that the information shown to users is not older than a minute.

The data fetched from the cache is fed to a `jinja` template that renders the `html` displayed to the user