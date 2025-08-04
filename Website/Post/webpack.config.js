const path = require("path");
const webpack = require("webpack");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = [
  {
    entry: "./static/Post/js/index.js",
    output: {
      path: path.resolve(__dirname, "./static/Post/js"),
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
    entry: "./static/Post/css/index.css",
    output: {
      path: path.resolve(__dirname, "./static/Post/css"),
    },
    module: {
      rules: [
        {
          test: /\.s?css$/,
          exclude: /node_modules/,
          use: [MiniCssExtractPlugin.loader, "css-loader"],
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: 'index.min.css', // Extracts CSS into separate files
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
