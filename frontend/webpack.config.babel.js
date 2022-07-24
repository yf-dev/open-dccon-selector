import path from 'path';
import fs from 'fs';
import webpack from 'webpack';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import { VueLoaderPlugin } from 'vue-loader';

module.exports = {
  entry: {
    video_overlay: './src/viewer.js',
    config: './src/config.js',
  },
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '',
    filename: 'static/[name].[fullhash].js',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader',
        ],
      },
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.sass$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader?indentedSyntax',
        ],
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
            // the "scss" and "sass" values for the lang attribute to the right configs here.
            // other preprocessors should work out of the box, no loader config like this necessary.
            scss: [
              'vue-style-loader',
              'css-loader',
              'sass-loader',
            ],
            sass: [
              'vue-style-loader',
              'css-loader',
              'sass-loader?indentedSyntax',
            ],
          },
          // other vue-loader options go here
        },
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[fullhash]',
        },
      },
    ],
  },
  resolve: {
    alias: {
      vue$: 'vue/dist/vue.esm.js',
    },
    extensions: ['*', '.js', '.vue', '.json'],
  },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      filename: 'video_overlay.html',
      chunks: ['video_overlay'],
      template: 'src/html/base.html',
    }),
    new HtmlWebpackPlugin({
      filename: 'config.html',
      chunks: ['config'],
      template: 'src/html/base.html',
    }),
    new CopyWebpackPlugin({
      patterns: [
        { from: "static", to: "static" },
      ],
    }),
  ],
  devServer: {
    historyApiFallback: true,
    server: {
      type: 'https',
      options: {
        key: fs.readFileSync('/cert/localhost-ssl.key'),
        cert: fs.readFileSync('/cert/localhost-ssl.crt'),
      },
    },
    host: '0.0.0.0',
    port: 8089,
  },
  performance: {
    hints: false,
  },
  devtool: 'eval',
};

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = false;
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"',
        API_HOSTNAME: `"${process.env.API_HOSTNAME}"`,
        TWITCH_EXTENSION_VERSION: `"${process.env.TWITCH_EXTENSION_VERSION}"`,
      },
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true,
    }),
  ]);
} else {
  module.exports.watchOptions = {
    aggregateTimeout: 300,
    poll: 1000,
  };
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"development"',
        API_HOSTNAME: `"${process.env.API_HOSTNAME}"`,
        // API_HOSTNAME: '"localhost:8088"',
        TWITCH_EXTENSION_VERSION: `"${process.env.TWITCH_EXTENSION_VERSION}"`,
      },
    }),
  ]);
}
