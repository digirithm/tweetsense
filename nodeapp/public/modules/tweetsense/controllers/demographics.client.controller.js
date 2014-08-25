'use strict';

angular.module('tweetsense').controller('DemographicsController', ['$scope', '$http', 'Demographic',
	function($scope, $http, Demographic) {
		var demographics = Demographic.query( function(data) { 
            $scope.demographics = data;
        });

        $("#ex2").slider({});
	}
]);