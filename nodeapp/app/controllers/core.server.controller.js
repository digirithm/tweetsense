'use strict';

/**
 * Module dependencies.
 */
exports.index = function(req, res) {
	res.render('index', {
		user: req.user || null
	});
};
exports.tweetsense = function(req, res) {
    res.render('tweetsense', {
        user: req.user || null
    });
};
