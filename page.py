'''Kiosk main functions and classes'''


class Channels():
    """
    Holds dicts of pages
    Pages have a uuid name
    Pages have a list of urls, current position and refresh time
    """

    def __init__(self):
        self.channels = {
            '_standby': [10, 0, [
                'https://dutchsec.com',
                'https://opensource-academy.github.io'
            ]]
        }

    def position_update(self, name):
        """Position +1 or reset to 0 at end of list"""
        channels = self.channels[name][2]
        position = self.channels[name][1]
        if position < len(channels)-1:
            self.channels[name][1] += 1
        else:
            self.channels[name][1] = 0

    def add(self, name, pages, time):
        """
        Add a list of urls to pages
        pages = list of urls
        time = time before refresh in seconds
        """
        position = 0
        self.channels.update({name: [time, position, pages]})

    def remove(self, name):
        """Remove entry name from pages dict"""
        if name in self.channels:
            del self.channels[name]
