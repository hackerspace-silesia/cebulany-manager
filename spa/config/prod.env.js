var process = require('process')

module.exports = {
  NODE_ENV: '"production"',
  API_URL: '"/' + (process.env.URL_PREFIX || '') + '/api"',
}
