'use strict';

angular.module('tweetsense').factory('Demographic', ['$resource',
	function($resource) {
		return $resource('/api/tweetsense/demographic/:demographicId', {
			demographicId: '@_id'
		}, {
			update: {
				method: 'PUT'
			}
		});
	}
]);