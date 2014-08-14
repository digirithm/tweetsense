'use strict';

// Setting up route
angular.module('core').config(['$stateProvider', '$urlRouterProvider',
	function($stateProvider, $urlRouterProvider) {
		// Redirect to home view when route not found
		$urlRouterProvider.otherwise('/');

		// Home state routing
		$stateProvider.
		state('socketio', {
			url: '/socketio',
			templateUrl: 'modules/core/views/socketio.client.view.html'
		}).
		state('meanjs', {
			url: '/meanjs',
			templateUrl: 'modules/core/views/meanjs.client.view.html'
		}).
		state('d3-examples', {
			url: '/d3-examples',
			templateUrl: 'modules/core/views/d3-examples.client.view.html'
		}).
		state('home', {
			url: '/',
			templateUrl: 'modules/core/views/home.client.view.html'
		});
	}
]);