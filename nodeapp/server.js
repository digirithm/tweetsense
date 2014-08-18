'use strict';
/**
 * Module dependencies.
 */
var init = require('./config/init')(),
	config = require('./config/config'),
	mongoose = require('mongoose');

/**
 * Main application entry file.
 * Please note that the order of loading is important.
 */

// Bootstrap db connection
var db = mongoose.connect(config.db, function(err) {
	if (err) {
		console.error('\x1b[31m', 'Could not connect to MongoDB!');
		console.log(err);
	}
});

// Init the express application
var app = require('./config/express')(db);


// Bootstrap passport config
require('./config/passport')();

//Setup Socket.IO
var http = require('http');
var server = http.createServer(app);
var io = require('socket.io').listen(server);

io.on('connection', function(socket){
  console.log('Client Connected');


  console.log('send client pings');
  socket.emit('ping','ping from server.  pong?');
  socket.broadcast.emit('broadcasting ping');

  socket.emit('notification','server saiz connected! yay');

  socket.on('broadcast', function(data){
    console.log('server broadcast');
    socket.emit('broadcast_message',data);
  });

  socket.on('message', function(data){
    console.log('server answer message');
    socket.emit('return_message',data);
  });

  socket.on('disconnect', function(){
    console.log('Client Disconnected.');
  });

  socket.on('ping', function(data){
    console.log('server ping success!');
    socket.emit('pong',data);
  });

  socket.on('pong', function(data){
    console.log('server pong!');
    socket.emit('pong',data);
  });

});



// Start the app by listening on <port>
//app.listen(config.port);
server.listen(config.port);
  
// Expose app
exports = module.exports = app;

// Logging initialization
console.log('MEAN.JS application started on port ' + config.port);


