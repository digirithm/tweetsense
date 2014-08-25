'use strict';

/**
 * Module dependencies.
 */
var mongoose = require('mongoose'),
	errorHandler = require('./errors'),
	Demographic = mongoose.model('Demographic'),
	_ = require('lodash');

/**
 * Create a Demographic
 */
exports.create = function(req, res) {
	var demographic = new Demographic(req.body);
	demographic.user = req.user;

	demographic.save(function(err) {
		if (err) {
			return res.status(400).send({
				message: errorHandler.getErrorMessage(err)
			});
		} else {
			res.jsonp(demographic);
		}
	});
};

/**
 * Show the current Demographic
 */
exports.read = function(req, res) {
	res.jsonp(req.demographic);
};

/**
 * Update a Demographic
 */
exports.update = function(req, res) {
	var demographic = req.demographic ;

	demographic = _.extend(demographic , req.body);

	demographic.save(function(err) {
		if (err) {
			return res.status(400).send({
				message: errorHandler.getErrorMessage(err)
			});
		} else {
			res.jsonp(demographic);
		}
	});
};

/**
 * Delete an Demographic
 */
exports.delete = function(req, res) {
	var demographic = req.demographic ;

	demographic.remove(function(err) {
		if (err) {
			return res.status(400).send({
				message: errorHandler.getErrorMessage(err)
			});
		} else {
			res.jsonp(demographic);
		}
	});
};

/**
 * List of Demographics
 */
exports.list = function(req, res) { Demographic.find().sort('-created').populate('user', 'displayName').exec(function(err, demographics) {
		if (err) {
			return res.status(400).send({
				message: errorHandler.getErrorMessage(err)
			});
		} else {
			res.jsonp(demographics);
		}
	});
};

/**
 * Demographic middleware
 */
exports.demographicByID = function(req, res, next, id) { Demographic.findById(id).populate('user', 'displayName').exec(function(err, demographic) {
		if (err) return next(err);
		if (! demographic) return next(new Error('Failed to load Demographic ' + id));
		req.demographic = demographic ;
		next();
	});
};

/**
 * Demographic authorization middleware
 */
exports.hasAuthorization = function(req, res, next) {
	if (req.demographic.user.id !== req.user.id) {
		return res.status(403).send('User is not authorized');
	}
	next();
};