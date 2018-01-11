require('./check-versions')()

var webpackConfig = null;
var isDevWatch = process.argv.length >= 3 && process.argv[2] === 'dev-watch';
if (isDevWatch) {
  console.log('Trying to build for development')
  process.env.NODE_ENV = 'development'
  webpackConfig = require('./webpack.dev-watch.conf')
} else {
  console.log('Trying to build for production')
  process.env.NODE_ENV = 'production'
  webpackConfig = require('./webpack.prod.conf')
}

var ora = require('ora')
var rm = require('rimraf')
var path = require('path')
var chalk = require('chalk')
var webpack = require('webpack')
var config = require('../config')

var spinner = ora('building...')
spinner.start()

rm(path.join(config.build.assetsRoot, config.build.assetsSubDirectory), err => {
  if (err) throw err
  webpack(webpackConfig, function (err, stats) {
    spinner.stop()
    if (err) throw err
    process.stdout.write(stats.toString({
      colors: true,
      modules: false,
      children: false,
      chunks: false,
      chunkModules: false
    }) + '\n\n')

    if (stats.hasErrors() && !isDevWatch) {
      console.log(chalk.red('  Build failed with errors.\n'))
      process.exit(1)
    }

    console.log(chalk.cyan('  Build complete.\n'))
    console.log(chalk.yellow(
      '  Tip: built files are meant to be served over an HTTP server.\n' +
      '  Opening *.html over file:// won\'t work.\n'
    ))
  })
})
