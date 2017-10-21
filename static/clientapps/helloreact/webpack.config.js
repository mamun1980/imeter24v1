var webpack = require('webpack');
var path = require('path');

var DIST_DIR = path.normalize(__dirname +"/..");
var SRC_DIR = path.resolve(__dirname, "src");

var config = {
    entry: {
        'dashboard': SRC_DIR + "/app/dashboard.js",
        'location': SRC_DIR + "/app/location.js",
    },
    output: {
        path: DIST_DIR + "/apps",
        filename: "[name].bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                include: SRC_DIR,
                loader: "babel-loader",
                query: {
                  presets: ["react", "es2015", "stage-2"]
                }
            }
        ]
    }
}

module.exports = config;
