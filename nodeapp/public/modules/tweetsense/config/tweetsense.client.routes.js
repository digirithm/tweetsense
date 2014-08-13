'use strict';

// Setting up route
angular.module('tweetsense').config(['$stateProvider',
    function($stateProvider) {
        // Articles state routing
        $stateProvider.
        state('tweetsense', {
            url: '/tweetsense',
            templateUrl: 'modules/tweetsense/views/tweetsense.view.html'
        })
    }
]);