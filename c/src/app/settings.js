/**
 * @fileoverview This file contains all ENV variables for the app.
 */

class EnvironmentError extends Error {
  constructor(message) {
    super(message)
    this.name = this.constructor.name
  }
}

function getEnvOrRaiseException(envName, envValue) {
  if (!envValue) throw new EnvironmentError(`Environment variable ${envName} is not set!`)

  return envValue
}

function findValue(v1, v2) {
  return [v1, v2].filter((v) => v)[0]
}

const PUBLIC_LETTER_A_API = getEnvOrRaiseException('NEXT_PUBLIC_LETTER_A_API', process.env.NEXT_PUBLIC_LETTER_A_API)
const LETTER_A_API = process.env.LETTER_A_API
const LETTER_B_API = process.env.LETTER_B_API
const PUBLIC_OTEL_RESOURCE_ATTRIBUTES = getEnvOrRaiseException(
  'NEXT_PUBLIC_OTEL_RESOURCE_ATTRIBUTES',
  process.env.NEXT_PUBLIC_OTEL_RESOURCE_ATTRIBUTES
)

const PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT = getEnvOrRaiseException(
  'NEXT_PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT',
  process.env.NEXT_PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT
)

export {
  LETTER_A_API,
  PUBLIC_LETTER_A_API,
  LETTER_B_API,
  PUBLIC_OTEL_RESOURCE_ATTRIBUTES,
  PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT,
}
