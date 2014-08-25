LEBOWSKI_DEMOGRAPHIC = {
    name: 'Lebowski'
    specs: {
           age: range(19, 40),
           gender: ['male'],
           location: [],
           keywords: ['whatisthedude', 'awesome', 'movie'],
           n_followers: '>100',
           n_friends: '>10'
           },
    }

FRIENDS_DEMOGRAPHIC = {
    name: 'Friends'
    specs: {
           age: range(30, 50),
           gender: ['male', 'female'],
           location: ['New York, NY'],
           keywords: ['friends', 'tv show'],
           n_followers: '>1000',
           n_friends: ''
           },
    }

SEX_AND_THE_CITY_DEMOGRAPHIC = {
    name: 'Sex & The City'
    specs: {
           age: range(19, 60),
           gender: ['female'],
           location: [],
           keywords: ['cary', 'sex and the city', 'mr. big'],
           n_followers: '>100',
           n_friends: ''
           },
    }

ENTERTAINMENT_DEMOGRAPHIC = {'demographics': [LEBOWSKI_DEMOGRAPHIC, FRIENDS_DEMOGRAPHIC, SEX_AND_THE_CITY_DEMOGRAPHIC]}

FRIENDS_QUESTION = {'label': 'Who is the favorite friend',
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
                    }

FRIENDS_POLL = {'id': 1, 'result': 0.75}  # made up
