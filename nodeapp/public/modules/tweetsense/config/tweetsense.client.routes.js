'use strict';

//Setting up route
angular.module('tweetsense').config(['$stateProvider',
	function($stateProvider) {
		// Tweetsense state routing
		$stateProvider.
		state('main', {
			url: '/tweetsense',
			templateUrl: 'modules/tweetsense/views/main.client.view.html'
		});
	}
]);