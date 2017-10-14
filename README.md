Flask-url-shortener
================

### Requirements

Before running the URL shortener, make sure you have installed in your system:

- **Docker**
- **Docker-compose**

### How to run it

1. Clone this repository
```
$ git clone https://github.com/jmartinm/flask-url-shortener.git
```

2. Enter the directory
```
$ cd flask-url-shortener
``` 

3. Start the service
```
$ docker-compose up
```

> **Note:**

> The first time you run `docker-compose up`, an error may appear because the web service cannot connect to the database. Just rerun the command again. The first time you run the command, the database is created, so it can take a bit more time to start.
> - This can be fixed in future versions by using the `depends_on` and `condition` features of docker-compose.

### Running tests

```
$ docker-compose run --rm web python setup.py test
```

### Features

- POST endpoint to generate a new short URL in `/shorten_url`
- Validation of max length in URLs, validity of URLs and other basic sanity checks
- GET endpoint that resolves a short URL, e.g `localhost:5000/abc`
- PostgreSQL backend ensures safe transactions when multiple processes create URLs simultaneously
- Retry mechanism when concurrent processes insert the same URL
- Base62 encoding of the ID in PostgreSQL is used as short URL hash, ensuring short URLs with readable characters
- Caching with Redis. Once a short URL is queried, the result is cached, ensuring that popular URLs will not access the database
- Tests for all parts of the application

### Future Development

- Functionality can be extended to support counter of number of accesses for a certain link
- Add timestamp of creation of a certain link
- API needs to be secured with e.g OAUTH2 in order to avoid SPAM and enforce access restrictions, rate limiting, etc
- Add Web UI, admin pages


Deployment
-------------

The deployment of the application in production can be done either with a system to manage containers, such as Kubernetes, or directly over bare metal/virtual machines.

In the case of Kubernetes, a tool can be used to convert from `docker-compose.yml` file to a Kubernetes compatible file.


> **Notes on scalability:**

> - The web machines/containers should be behind a Load Balancer, such as HaProxy. This allows to scale the number of web workers if the number of requests exceeded the capacity.
> - A redis cluster can be created - see https://redis.io/topics/cluster-tutorial for high availability of the cache.
> - If the space in the database became a bottleneck and we don't want to expire old URLs, a PostgreSQL sharded approach can be taken.
> - If instead the performance of the database reads/writes wants to be improved a master-slave setup could be put in place or a multimaster setup (if more write throughput is needed). Note that PostgreSQL should handle at least ~1000 writes/s (depending on the hardware) with a single machine.

