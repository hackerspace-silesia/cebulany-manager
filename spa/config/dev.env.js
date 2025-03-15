var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge.merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"http://localhost:5000/api"'
})
