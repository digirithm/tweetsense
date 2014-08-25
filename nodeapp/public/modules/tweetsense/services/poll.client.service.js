'use strict';

angular.module('tweetsense').factory('Poll', ['$resource',
	function($resource) {
		return $resource('/api/tweetsense/poll/:pollId', {
			pollId: '@_id'
		}, {
			update: {
				method: 'PUT'
			}
		});
	}
]);