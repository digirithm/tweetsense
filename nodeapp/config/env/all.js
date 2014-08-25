'use strict';

module.exports = {
	app: {
		title: 'MEAN',
		description: 'Full-Stack JavaScript with MongoDB, Express, AngularJS, and Node.js',
		keywords: 'MongoDB, Express, AngularJS, Node.js'
	},
	port: process.env.PORT || 3000,
	templateEngine: 'swig',
	sessionSecret: 'MEAN',
	sessionCollection: 'sessions',
	assets: {
		lib: {
			css: [
				'public/lib/bootstrap/dist/css/bootstrap.css',
				'public/lib/bootstrap/dist/css/bootstrap-theme.css',
				'public/spacelabs/assets/css/font-awesome.min.css',
				'public/lib/seiyria-bootstrap-slider/dist/css/bootstrap-slider.min.css'

			],
			js: [
			'//maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization',
			   	'public/spacelabs/assets/js/jquery-1.10.2.min.js',
       			'public/spacelabs/assets/plugins/countTo/jquery.countTo.js',
				'public/lib/angular/angular.js',
				'public/lib/angular-resource/angular-resource.js', 
				'public/lib/angular-cookies/angular-cookies.js', 
				'public/lib/angular-animate/angular-animate.js', 
				'public/lib/angular-touch/angular-touch.js', 
				'public/lib/angular-sanitize/angular-sanitize.js', 
				'public/lib/angular-ui-router/release/angular-ui-router.js',
				'public/lib/angular-ui-utils/ui-utils.js',
				'public/lib/angular-bootstrap/ui-bootstrap-tpls.js',
				'public/lib/seiyria-bootstrap-slider/dist/bootstrap-slider.min.js',
				 'public/lib/angular-socket-io/socket.js',
       			 'public/lib/socket.io-client/socket.io.js',
       			 'public/spacelabs/assets/js/modernizr-2.6.2.min.js',
       			'public/spacelabs/assets/plugins/weather/js/skycons.js',
       			
       			'public/lib/lodash/dist/lodash.underscore.min.js',
       			'public/lib/angular-google-maps/dist/angular-google-maps.min.js'
				
			]
		},
		css: [
		
			'public/spacelabs/assets/css/animate.css',
       		'public/spacelabs/assets/css/main.css',
       		'public/modules/**/css/*.css',
		],
		js: [
			'public/config.js',
			'public/application.js',
			'public/modules/*/*.js',
			'public/modules/*/*[!tests]*/*.js'
		],
		tests: [
			'public/lib/angular-mocks/angular-mocks.js',
			'public/modules/*/tests/*.js'
		]
	}
};