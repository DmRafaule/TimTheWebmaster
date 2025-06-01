const path = require("path");
const webpack = require("webpack");


module.exports = {
  entry: "./static/RSSAggregator/js/index.js",
  output: {
    path: path.resolve(__dirname, "./static/RSSAggregator/js"),
    filename: "[name].js",
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
};
