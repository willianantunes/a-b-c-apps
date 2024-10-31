const http = require('http')

const options = {
  hostname: 'localhost',
  port: parseInt(process.env.PORT || '3000', 10),
  path: '/api/healthcheck/liveness',
  method: 'GET',
}

const req = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0)
  } else {
    process.exit(1)
  }
})

req.on('error', () => {
  process.exit(1)
})

req.end()
