import hackchat
import random
import igraph


class TuringBot(hackchat.HackChat):
    """
    A basic TuringBot class.
    It has the capacity of reading and interpreting the emotion of last message that the user sent
    and replying with a random response which fits that emotion group.
    Inheriting from this class will allow one to customize emotion interpretation process.

    Basic emotion groups:
    - Positive
     * Funny
     * Happy
    - Negative
     * Sad
     * Angry
    - Confused
    """
    def __init__(self, screen_name: str, channel: str, responses: dict, triggers=None):
        super().__init__(screen_name, channel)
        self.emotion_groups = self._default_emotion_group_graph()
        self.responses = responses
        self.triggers = triggers if triggers else {}
        self.on_message.append(self.process_message)

    def process_message(self, message, sender):
        # ???
        # Call appropriate methods
        pass

    def response(self, emotion_group):
        if emotion_group in self.responses.keys():
            return random.choice(self.responses[emotion_group])
        else:

    def _traverse_dict(self, dictionary, list_of_targets):
        for key in dictionary:
            if key in list_of_targets:
                return key
            return self._traverse_dict(dictionary[key], list_of_targets)

    def _default_emotion_group_graph(self):
        emotion_names = ('positive', 'happy', 'funny', 'negative', 'sad', 'angry', 'confused')
        graph = igraph.Graph()
        graph.add_vertices(len(emotion_names), {'name': emotion_names})
        graph.add_edges([(0, 1), (0, 2), (3, 4), (3, 5)])
        return graph