'use strict';

angular.module('core').controller('SocketioController', ['$scope',
	function($scope) {

    var socket = io.connect();
    console.log(socket);  

    $scope.messages = [];


    // todo: clean this up to have 3-5 functions..  could consolidate message + broadcast into one uniform message signal
    
    // -- send generic message w/ a type, timestamp, payload
    // -- get generic message w/ a type, timestamp, payload
    // -- receive broadcast 
    // -- send broadcast
    // -- ping / pong

    $scope.sendSocket = function(){
      var message = 'Message Sent on ' + new Date(); 
      socket.emit('message', message);  
      $scope.messages.push(message);  
    };

    $scope.pingSocket = function(){ 
      socket.emit('ping', 'Ping Sent on ' + new Date());    
    };

    $scope.returnSocket = function(){ 
      socket.emit('return_message', 'return a message after the beeep ' + new Date());    
    };

    $scope.broadcastSocket = function(){ 
      socket.emit('broadcast_message', 'here ye, here ye, i broadcasted to all peers ' + new Date());    
    };

    $scope.pingSocket = function(){ 
      socket.emit('ping', 'Ping Sent on ' + new Date());    
    };

    $scope.notificationSocket = function(){
      socket.emit('notification', 'Notification Sent on ' + new Date());
    }

    socket.on('ping', function (data) {
        $scope.messages.push('ping:' + data)
    });

    socket.on('pong', function (data) {
      $scope.messages.push('pong' + data);
    });

     socket.on('message', function (data) {
      $scope.messages.push('message:' + data)
    });

    socket.on('return_message', function (data) {
     $scope.messages.push('return_message:' + data)
    });
    
    socket.on('broadcast_message:', function (data) {
      $scope.messages.push('broadcast_message:' + data)
    });
    
    socket.on('notification', function (data) {
      $scope.messages.push('notification: ' + data);
    });
	}
]);