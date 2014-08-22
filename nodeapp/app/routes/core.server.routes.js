'use strict';

module.exports = function(app) {
	// Root routing
	var core = require('../../app/controllers/core');
	app.route('/').get(core.index);
    app.route('/tweetsense').get(core.tweetsense);
};