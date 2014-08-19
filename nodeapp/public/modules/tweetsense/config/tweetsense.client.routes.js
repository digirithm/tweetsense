'use strict';

//Setting up route
angular.module('tweetsense').config(['$stateProvider',
	function($stateProvider) {
		// Tweetsense state routing
		$stateProvider.
		state('main', {
			url: '/main',
			templateUrl: 'modules/tweetsense/views/main.client.view.html'
		});
	}
]);