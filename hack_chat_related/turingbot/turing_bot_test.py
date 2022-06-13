import nltk
nltk.set_proxy('127.0.0.1:7890')

import turing_bot_implemented

new_bot = turing_bot_implemented.EnglishTuringBot('Cynthia', 'turingbot', {
    'funny': ['lmao', 'lmaoo', 'hahaha', 'lol', 'LOL', 'XD', 'xD', 'hhhhhhh', 'hahahaha', 'hhhh', 'hhh', 'LMAO', 'loll'],
    'positive': ['sounds great!', 'wow', 'wow!', 'that\'s p nice', 'perfect!', 'cool', 'niiiceee',
                 'that\'s so coool!!', 'fabulous!', 'actually that\'s rly nice', 'great!', 'pog', 'pog!', 'POG',
                 'pogchamp!', 'pro gamers move', 'really??', 'wtf that\'s so cool', 'poggers', 'nicee :D'],
    'negative': ['oop', 'sorry to hear that', 'that\'s horrible', 'that\'s terrible', 'welp', 'not poggers',
                 'what in the world', 'oop.', 'copium', 'sadge', 'not so cool', 'not pog', 'D:', ':\')', 'bruh moment'],
    'confused': ['excuse me???', 'what??', '?', 'seriously?', 'wtf?', '??', '???', '????'],
    'neutral': ['k', 'ok', 'I see', 'cool', 'that makes sense', 'makes sense', 'sure', 'hmm', 'uh huh', 'yep', 'yup'],
    'greeting': ['hey', 'sup', 'hi', 'hello', 'mornin lol', 'gudday'],
})

new_bot.run()
