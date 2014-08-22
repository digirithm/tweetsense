'use strict';
var devRest = require('dev-rest-proxy');

module.exports = function(app) {

    app.get('/api/tweetsense/*', function(req, res) {
        devRest.proxy(req,res, 'localhost', 8080);
    });

    app.post('/api/tweetsense/*', function(req, res) {
        devRest.proxy(req,res, 'localhost', 8080);
    });
};