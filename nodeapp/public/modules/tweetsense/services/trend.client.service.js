'use strict';

angular.module('tweetsense').factory('Trend', ['$resource',
	function($resource) {
		return $resource('/api/tweetsense/trend/:trendId', {
			trendId: '@_id'
		}, {
			update: {
				method: 'PUT'
			}
		});
	}
]);