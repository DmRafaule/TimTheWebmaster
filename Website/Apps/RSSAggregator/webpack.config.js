const path = require("path");
const webpack = require("webpack");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = [
  {
    entry: "./static/RSSAggregator/js/index.js",
    output: {
      path: path.resolve(__dirname, "./static/RSSAggregator/js"),
      filename: "index.min.js",
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
          },
        },
      ],
    },
    optimization: {
      minimize: true,
    },
    plugins: [
      new webpack.DefinePlugin({
        "process.env": {
          // This has effect on the react lib size
          NODE_ENV: JSON.stringify("production"),
        },
      }),
    ],
  },
  {
    entry: "./static/RSSAggregator/css/index.css",
    output: {
      path: path.resolve(__dirname, "./static/RSSAggregator/css"),
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            MiniCssExtractPlugin.loader, 
            "css-loader",
            "postcss-loader"
          ],
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: 'index.min.css',
      }),
    ],
    optimization: {
      minimize: true, // Enables minification
      minimizer: [
        new CssMinimizerPlugin(), // Adds the CSS minifier
      ],
    },
  },

];
