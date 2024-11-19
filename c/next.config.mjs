/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    // To enable OTLP instrumentation
    // https://github.com/vercel/next.js/issues/49897
    instrumentationHook: true,
  },
}

export default nextConfig
