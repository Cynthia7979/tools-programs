import hackchat
import random
import igraph
import abc


class ABCTuringBot(metaclass=abc.ABCMeta):
    """
    An abstract TuringBot class.
    It should be overridden with the method for reading and interpreting the emotion of last message that the user sent
    and replying with a random respond which fits that emotion group.
    This is an abstract base class. Any instances should be instantiated from a child of this class.
    """
    def __init__(self, screen_name: str, channel: str, responses: dict, triggers=None):
        self.hc = hackchat.HackChat(screen_name, channel)
        self.emotion_groups = self._generate_emotion_graph()
        self.responses = responses
        self.triggers = triggers if triggers else {}
        self.hc.on_message = [self.process_message]

    @abc.abstractmethod
    def process_message(self, _chat, message, _sender):
        if self._check_triggers(_chat, message, _sender): return
        pass

    def respond(self, emotion_group):
        if emotion_group in self.responses.keys():
            self.hc.send_message(random.choice(self.responses[emotion_group]))
            return
        else:
            for neighbor in self.emotion_groups.vs[self.emotion_groups.neighbors(emotion_group)]['name']:
                if neighbor in self.responses.keys():
                    self.hc.send_message(random.choice(self.responses[neighbor]))
                    return
        print('No appropriate response found, skipping this message.')

    def _check_triggers(self, _chat, message, _sender):
        existing_triggers = []
        for trigger in self.triggers.keys():
            if trigger in message:
                existing_triggers.append(self.triggers[trigger])
        if existing_triggers:
            self.respond(random.choice(existing_triggers))
            return True
        else:
            return False

    @abc.abstractmethod
    def _generate_emotion_graph(self):
        return igraph.Graph()

    def run(self):
        print(f'Starting {type(self).__name__} "{self.hc.nick}" in hack.chat/?{self.hc.channel}...')
        self.hc.run()
