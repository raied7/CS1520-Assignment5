import datetime


def clean(s):
    """Return a string w/ angle brackets, endlines, & tab characters removed."""

    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.strip()
    if len(s) > 100:
        s = s[:100]

    return s


class Message():
    """An object representing a single chat message."""

    def __init__(self, user, text, time=None):
        """Initialize a message for named user."""

        self.user = user
        self.text = text

        if time:
            self.time = time
        else:
            self.time = datetime.datetime.now()


    def get_formatted_time(self):
        """Return this messages's time as a 'YYYYMMDD HH:MM:SS' string."""

        return self.time.strftime('%Y%m%d %H:%M:%S')


    def to_html(self):
        """Convert this message to an HTML div."""
        
        outputDiv = '<div class="Message">%s (%s): %s</div>'
        span = '<span class="%s">%s</span>'
        timeSpan = span % ('Time', self.get_formatted_time())
        userSpan = span % ('User', self.user)
        textSpan = span % ('Text', self.text)
        return outputDiv % (timeSpan, userSpan, textSpan)


    def __str__(self):
        """Return a simple formatted string with the message contents."""

        return '%s (%s): %s' % (self.get_formatted_time(), self.user, self.text)
    

    def __lt__(self, other):
        return self.time < other.time


    def __gt__(self, other):
        return self.time > other.time
    

    def __eq__(self, other):
        return self.time == other.time
    

    def __ne__(self, other):
        return self.time != other.time
    

    def __le__(self, other):
        return self.time <= other.time
    

    def __ge__(self, other):
        return self.time >= other.time


class ChatManager():
    """A class for managing chat messages."""

    def __init__(self):
        """Initialize the ChatManager with a new list of messages."""

        self.messages = []


    def add_message(self, msg):
        """Add a message to our messages list."""

        self.messages.append(msg)        
        self.messages.sort()


    def create_message(self, user, text):
        """Create a new message with the current timestamp."""

        self.add_message(Message(clean(user), clean(text)))


    def get_messages_output(self):
        """Return the current message contents as a plain text string."""

        result = ''
        for msg in self.messages:
            result += str(msg)
            result += '\n'
        return result


    def get_messages_html(self):
        """Return the current message contents as HTML."""

        result = ''
        for msg in self.messages:
            result += msg.to_html()
            result += '\n'
        return result


    def clear_messages_before(self, time):
        """Remove all messages prior to a given time."""
        
        while len(self.messages) > 0 and self.messages[0].time < time:
            self.messages.pop(0)

