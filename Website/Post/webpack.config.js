const path = require("path");
const webpack = require("webpack");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = [
  {
    entry: "./static/Post/js/index.article.js",
    output: {
      path: path.resolve(__dirname, "./static/Post/js"),
      filename: "index.article.min.js",
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
    entry: "./static/Post/css/index.article.css",
    output: {
      path: path.resolve(__dirname, "./static/Post/css"),
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
        filename: 'index.article.min.css',
      }),
    ],
    optimization: {
      minimize: true, // Enables minification
      minimizer: [
        new CssMinimizerPlugin(), // Adds the CSS minifier
      ],
    },
  },

  {
    entry: "./static/Post/js/index.tool.js",
    output: {
      path: path.resolve(__dirname, "./static/Post/js"),
      filename: "index.tool.min.js",
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
    entry: "./static/Post/css/index.tool.css",
    output: {
      path: path.resolve(__dirname, "./static/Post/css"),
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
        filename: 'index.tool.min.css',
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
