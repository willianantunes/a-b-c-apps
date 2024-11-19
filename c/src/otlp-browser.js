import { WebTracerProvider } from '@opentelemetry/sdk-trace-web'
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web'
import { SimpleSpanProcessor, BatchSpanProcessor, ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { ZoneContextManager } from '@opentelemetry/context-zone'
import { Resource } from '@opentelemetry/resources'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { PUBLIC_OTEL_RESOURCE_ATTRIBUTES, PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT } from '@/app/settings'
import { CompositePropagator, W3CBaggagePropagator, W3CTraceContextPropagator } from '@opentelemetry/core'

const parseEnvVariable = (envVariable) => {
  return envVariable.split(',').reduce((acc, pair) => {
    const [key, value] = pair.split('=')
    acc[key] = value
    return acc
  }, {})
}

const resourceAttributes = parseEnvVariable(PUBLIC_OTEL_RESOURCE_ATTRIBUTES)
// https://opentelemetry.io/docs/languages/js/exporters/#usage-in-the-browser
const exporter = new OTLPTraceExporter({
  url: PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT,
  headers: {},
  concurrencyLimit: 10,
  timeoutMillis: 15 * 1000,
})

const providerWithZone = new WebTracerProvider({
  resource: new Resource({ ...resourceAttributes }),
  spanProcessors: [
    new SimpleSpanProcessor(new ConsoleSpanExporter()),
    new BatchSpanProcessor(exporter, {
      maxQueueSize: 10,
      maxExportBatchSize: 3,
      scheduledDelayMillis: 500,
      exportTimeoutMillis: 10 * 1000,
    }),
  ],
})

providerWithZone.register({
  contextManager: new ZoneContextManager(),
  propagator: new CompositePropagator({
    propagators: [new W3CBaggagePropagator(), new W3CTraceContextPropagator()],
  }),
})

const startOtelInstrumentation = () => {
  registerInstrumentations({
    tracerProvider: providerWithZone,
    instrumentations: [getWebAutoInstrumentations()],
  })
}

export { startOtelInstrumentation }
