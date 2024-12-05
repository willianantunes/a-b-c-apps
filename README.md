# A, B, and C applications

Sample applications fully integrated with OTel. Access each application's README for more information.

Use the images:

- [willianantunes/a-b-c-apps-letter-a](https://hub.docker.com/r/willianantunes/a-b-c-apps-letter-a)
- [willianantunes/a-b-c-apps-letter-b](https://hub.docker.com/r/willianantunes/a-b-c-apps-letter-b)
- [willianantunes/a-b-c-apps-letter-c](https://hub.docker.com/r/willianantunes/a-b-c-apps-letter-c)

## Running the applications

Just run the following command:

```bash
docker compose up
```

Applications will be available at:

- Letter A (C# with NDjango Rest Framework): http://localhost:8000/swagger
- Letter B (Python with Django and DRF): http://localhost:8080/api/v1/
- Letter C (JavaScript with Next.js and React Admin): http://localhost:3000

Observability tools are available at:

- Jaeger: http://0.0.0.0:16686
- Zipkin: http://0.0.0.0:9411
- Prometheus: http://0.0.0.0:9090
- HyperDX: http://localhost:8090
