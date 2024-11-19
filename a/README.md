# Letter A

Execute `docker compose up app-production` to start API server in production mode. When the server is running, you can access the API documentation at `http://localhost:8000/swagger`. Other links:

- http://localhost:8000/api/healthcheck/liveness
- http://localhost:8000/api/healthcheck/readiness
- http://localhost:8000/api/healthcheck/integrations
- http://localhost:8000/api/healthcheck/integrations
- http://localhost:8000/debug/routes

Observability tools are available at:

- Jaeger: http://0.0.0.0:16686
- Zipkin: http://0.0.0.0:9411
- Prometheus: http://0.0.0.0:9090
- HyperDX: http://localhost:8090

This project uses [NDjango Rest Framework](https://github.com/juntossomosmais/NDjango.RestFramework) to expose CRUD operations without generating boilerplate code.

