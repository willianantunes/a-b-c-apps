import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { SimpleSpanProcessor, ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base'
import { NodeSDK } from '@opentelemetry/sdk-node'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'

const spanProcessors = [new BatchSpanProcessor(new OTLPTraceExporter())]
if (process.env.NODE_ENV === 'development') {
  spanProcessors.push(new SimpleSpanProcessor(new ConsoleSpanExporter()))
}

const sdk = new NodeSDK({
  instrumentations: [
    // https://github.com/open-telemetry/opentelemetry-js-contrib/tree/d0fb13557fac651424b095b0a48a5116407875b1/plugins/node
    // https://github.com/open-telemetry/opentelemetry-js-contrib/tree/d0fb13557fac651424b095b0a48a5116407875b1/metapackages/auto-instrumentations-node
    getNodeAutoInstrumentations(),
  ],
  spanProcessors,
})
sdk.start()
