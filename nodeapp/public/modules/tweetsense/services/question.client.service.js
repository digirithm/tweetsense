'use strict';

angular.module('tweetsense').factory('Question', ['$resource',
	function($resource) {
		return $resource('/api/tweetsense/question/:questionId', {
			questionId: '@_id'
		}, {
			update: {
				method: 'PUT'
			}
		});
	}
]);