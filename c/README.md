# Letter C

Execute `docker compose up app-production` and access the admin page at [http://localhost:3000/admin](http://localhost:3000) when the server is ready. It depends on Letter A to run. Please, follow the instructions in the [Letter A project](../a/README.md). Observability tools are available at:

- Jaeger: http://0.0.0.0:16686
- Zipkin: http://0.0.0.0:9411
- Prometheus: http://0.0.0.0:9090

The React-Admin has a custom Data Provider that supports [NDjango Rest Framework](https://github.com/juntossomosmais/NDjango.RestFramework). Look at the [index.js](src/ra-data-ndjango-rest-framework-pagination/index.js) in `ra-data-drf-page-number-pagination` folder.
