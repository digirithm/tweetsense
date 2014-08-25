'use strict';
var devRest = require('dev-rest-proxy');

module.exports = function(app) {

    /*app.get('/api/tweetsense/*', function(req, res) {
        devRest.proxy(req,res, 'localhost', 8080);
    });

    app.post('/api/tweetsense/*', function(req, res) {
        devRest.proxy(req,res, 'localhost', 8080);
    });
*/
    app.get('/api/tweetsense/demographic', function(req,res){ 
        var demographics = [{
                            name: 'Lebowski',
                            specs: {
                                   age: '19, 40',
                                   gender: ['male'],
                                   location: [],
                                   keywords: ['whatisthedude', 'awesome', 'movie'],
                                   n_followers: '>100',
                                   n_friends: '>10'
                                   }
                            }, 
                            {
                            name: 'Friends',
                            specs: {
                                   age: '30, 50',
                                   gender: ['male', 'female'],
                                   location: ['New York, NY'],
                                   keywords: ['friends', 'tv show'],
                                   n_followers: '>1000',
                                   n_friends: ''
                                   }
                            },
                            {
                            name: 'Sex & The City',
                            specs: {
                                   age: '19, 60',
                                   gender: ['female'],
                                   location: [],
                                   keywords: ['cary', 'sex and the city', 'mr. big'],
                                   n_followers: '>100',
                                   n_friends: ''
                                   }
                            }];

        res.json(demographics)
    });
app.get('/api/tweetsense/demographic/lebowski', function(req,res){ 
        var demographics = {
                            name: 'Lebowski',
                            specs: {
                                   age: '19, 40',
                                   gender: ['male'],
                                   location: [],
                                   keywords: ['whatisthedude', 'awesome', 'movie'],
                                   n_followers: '>100',
                                   n_friends: '>10'
                                   }
                            };

        res.json(demographics)
    })

    app.get('/api/tweetsense/question/lebowski', function(req,res){

            var question = {'label': 'Who is the favorite friend',
                    'exemplars': [('Ross is the best', 1),
                                  ('I hate the show', 0),
                                  ('Monica rocks', 0),
                                  ('I love Ross', 1),
                                  ('Chandler is better than Ross', 0),
                                  ('David Schwimmer is so sexy', 1),
                                  ('Ross, please have my babies', 1),
                                  ('Rachel is hotter than Phoebe', 0),
                                  ('Joey is not as cool as Ross', 1),
                                  ('Joey is hot', 0)]
                    };
            res.json(question);
    });

    app.get('/api/tweetsense/polls', function(req, res){
        res.json({'id': 1, 'result': 0.75});
    });
};