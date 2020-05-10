const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const vendorPath = "resources/vendor/";

module.exports = {
  entry: {
    vender: [
      path.resolve(__dirname, vendorPath + "jquery-2.2.4.min.js"),
      path.resolve(__dirname, vendorPath + "jquery.easing.1.3.js"),
    ],
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static/js"),
  },
  mode: "none",
  module: {
    rules: [
      {
        test: /\.css$/,
        include: [path.resolve(__dirname, "resources/vendor/bootstrap")],
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "vendor.css",
    }),
  ],
};
