// Karma configuration
// Generated on Wed Apr 15 2015 15:37:42 GMT-0300 (BRT)

module.exports = function(config) {
    config.set({
        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '../',


        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine'],


        // list of files / patterns to load in the browser
        files: [
            './node_modules/angular/angular.min.js',
            './node_modules/angular/angular-route.min.js',
            './node_modules/angular/angular-resource.min.js',
            './node_modules/angular/angular-aria.min.js',
            './node_modules/angular/angular-animate.min.js',
            './node_modules/material/angular-material.min.js',
            './node_modules/jasmine-core/lib/jasmine-core/jasmine.js',
            './node_modules/jasmine-core/lib/jasmine-core/jasmine-html.js',
            './node_modules/jasmine-core/lib/jasmine-core/boot.js',
            './app/app.js',
            './app/**/*.js',
            './node_modules/angular/angular-mocks.js',
            './tests/**/*.js'
        ],


        // list of files to exclude
        exclude: [
        ],


        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            './app/**/*.js': ['coverage']
        },


        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['dots', 'coverage'],

        // optionally, configure the reporter
        coverageReporter: {
            type : 'html',
            dir : '../report/frontend/coverage/',
            subdir: function (browser) {
                return browser.toLowerCase().split(/[ /-]/)[0];
            }
        },


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['PhantomJS'],

        
        plugins : [
            'karma-jasmine',
            'karma-coverage',
            'karma-phantomjs-launcher'
            ],


        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true
    });
};
