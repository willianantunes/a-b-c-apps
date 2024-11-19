import { LETTER_A_API, LETTER_B_API } from '@/app/settings'

export async function GET(request) {
  const hosts = [
    {
      name: 'Letter A',
      url: LETTER_A_API,
    },
    {
      name: 'Letter B',
      url: LETTER_B_API,
    },
  ]

  const checkHealth = async (name, url) => {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(5 * 1000) })
      if (!response.ok) {
        return { name, status: 'down' }
      }
      return { name, status: 'up' }
    } catch (e) {
      return { name, status: 'down', details: e.cause.message }
    }
  }
  const healthChecks = await Promise.all(hosts.map((host) => checkHealth(host.name, host.url)))

  return Response.json(healthChecks)
}
