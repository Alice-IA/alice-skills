import re
from os.path import dirname, join

from adapt.intent import IntentBuilder
from alice import AliceSkill, intent_handler


# TODO - Localization

class SpeakSkill(AliceSkill):
    @intent_handler(IntentBuilder("").require("Speak").require("Words"))
    def speak_back(self, message):
        """
            Repeat the utterance back to the user.

            TODO: The method is very english centric and will need
                  localization.
        """
        # Remove everything up to the speak keyword and repeat that
        utterance = message.data.get('utterance')
        repeat = re.sub('^.*?' + message.data['Speak'], '', utterance)
        self.speak(repeat.strip())

    def stop(self):
        pass


def create_skill():
    return SpeakSkill()
