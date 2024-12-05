# Letter C

Execute `docker compose up app-production` and access the admin page at [http://localhost:3000/](http://localhost:3000) when the server is ready. It depends on Letter A or Letter B to run. To run Letter A for example, follow the instructions in the [Letter A project](../a/README.md). Observability tools are available at:

- Jaeger: http://0.0.0.0:16686
- Zipkin: http://0.0.0.0:9411
- Prometheus: http://0.0.0.0:9090

The React-Admin has custom Data Providers that support [NDjango Rest Framework](https://github.com/juntossomosmais/NDjango.RestFramework) and [Django Rest Framework](https://github.com/encode/django-rest-framework). Look at the [src/ra-data-ndjango-rest-framework-pagination/index.js](src/ra-data-ndjango-rest-framework-pagination/index.js) and [src/ra-data-django-rest-framework-pagination/index.js](src/ra-data-django-rest-framework-pagination/index.js).
