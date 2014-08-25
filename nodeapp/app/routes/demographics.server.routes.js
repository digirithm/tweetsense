'use strict';

module.exports = function(app) {
	var users = require('../../app/controllers/users');
	var demographics = require('../../app/controllers/demographics');

	// Demographics Routes
	app.route('/demographics')
		.get(demographics.list)
		.post(users.requiresLogin, demographics.create);

	app.route('/demographics/:demographicId')
		.get(demographics.read)
		.put(users.requiresLogin, demographics.hasAuthorization, demographics.update)
		.delete(users.requiresLogin, demographics.hasAuthorization, demographics.delete);

	// Finish by binding the Demographic middleware
	app.param('demographicId', demographics.demographicByID);
};