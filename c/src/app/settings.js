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

export { PUBLIC_LETTER_A_API }
