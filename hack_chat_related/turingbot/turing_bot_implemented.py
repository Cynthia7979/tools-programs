import turing_bot_base
import text2emotion as te
import igraph
import random


class EnglishTuringBot(turing_bot_base.ABCTuringBot):
    """
    A TuringBot class designated to process basic English messages. It uses text2emotion for emotion recognition,
    and has a few triggers by default.
    """
    def __init__(self, screen_name: str, channel: str, responses: dict, triggers=None):
        super().__init__(screen_name, channel, responses)
        self.triggers = triggers if triggers else {
            '??': 'confused',
            'lmao': 'funny',
            'lol': 'funny',
            'haha': 'funny',
            'xd': 'funny',
            'hhh': 'funny',
            ':(': 'sad',
            '>:(': 'angry',
            'hi': 'greeting',
            'hello': 'greeting',
            'hey': 'greeting',
            'sup': 'greeting',
            'what\'s up': 'greeting'
        }

    def process_message(self, _chat, message, _sender):
        if self._check_triggers(_chat, message, _sender): return
        emotion_weights = te.get_emotion(message)
        if sum(emotion_weights.values()) == 0:  # Not English or neutral message
            self.respond('neutral')
            return
        else:
            current_max = 0
            weights_emotions = {}
            for emo, we in emotion_weights.items():
                if we > current_max:
                    current_max = we
                if we not in weights_emotions.keys():
                    weights_emotions[we] = [emo]
                else:
                    weights_emotions[we].append(emo)
            selected_emotions = weights_emotions[current_max]
            self.respond(random.choice(selected_emotions).lower())

    def _generate_emotion_graph(self):
        emotion_names = ('positive', 'happy', 'funny', 'surprise', 'negative', 'sad', 'angry', 'fear', 'confused', 'neutral', 'greeting')
        graph = igraph.Graph()
        graph.add_vertices(len(emotion_names), {'name': emotion_names})
        graph.add_edges([(0, 1), (0, 2), (0, 3), (4, 5), (4, 6), (4, 7)])
        return graph
