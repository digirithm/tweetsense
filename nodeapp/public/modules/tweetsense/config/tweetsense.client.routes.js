'use strict';

//Setting up route
angular.module('tweetsense').config(['$stateProvider',
	function($stateProvider) {
		// Tweetsense state routing
		$stateProvider.
		state('suggestions', {
			url: '/tweetsense/suggestions',
			templateUrl: 'modules/tweetsense/views/suggestions.client.view.html'
		}).
		state('trends', {
			url: '/tweetsense/trends',
			templateUrl: 'modules/tweetsense/views/trends.client.view.html'
		}).
		state('polls', {
			url: '/tweetsense/polls',
			templateUrl: 'modules/tweetsense/views/polls.client.view.html'
		}).
		state('demographics', {
			url: '/tweetsense/demographics',
			templateUrl: 'modules/tweetsense/views/demographics.client.view.html'
		}).
		state('demographics.form', {
			url: '/tweetsense/demographics/form',
			templateUrl: 'modules/tweetsense/views/demographics_form.client.view.html'
		}).
		state('main', {
			url: '/tweetsense',
			templateUrl: 'modules/tweetsense/views/main.client.view.html'
		});
	}
]);