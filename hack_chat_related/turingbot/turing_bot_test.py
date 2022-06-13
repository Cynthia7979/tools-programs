import nltk
nltk.set_proxy('127.0.0.1:7890')

import turing_bot_implemented

new_bot = turing_bot_implemented.EnglishTuringBot('Cynthia', 'turingbot', {
    'funny': ['lmao', 'lmaoo', 'hahaha', 'that\'s actually so funny', 'lol', 'LOL', 'XD', 'xD', 'I\'m laughing so hard',
              'hhhhhhh', 'hahahaha what the hell'],
    'positive': ['sounds great!', 'wow', 'wow!', 'that\'s pretty nice', 'perfect!', 'cool', 'niiiceee',
                 'that\'s so coool!!', 'fabulous!', 'actually that\'s really nice', 'great!', 'pog', 'pog!',
                 'pogchamp!', 'pro gamers move', 'really??', 'wtf that\'s so cool', 'poggers', 'nicee :D'],
    'negative': ['oop', 'sorry to hear that', 'that\'s horrible', 'that\'s terrible', 'welp', 'not poggers',
                 'what in the world', 'oop.', 'copium', 'sadge', 'not so cool', 'not pog', 'D:', ':\')'],
    'confused': ['excuse me???', 'what??', '?', 'seriously?', 'wtf?', 'huhh??', 'really??'],
    'neutral': ['k', 'ok', 'I see', 'cool', 'that makes sense', 'makes sense', 'sure', 'hmm', 'well ok', 'uh huh', 'yep'],
    'greeting': ['hey', 'sup', 'hi', 'hello', 'mornin lol', 'goodday']
})

new_bot.run()
