import datetime
from google.cloud import datastore

# declare and initialize datastore client
messages_stored = datastore.Client() 

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


class Message(datastore.Entity):
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

    """ method to convert Message object to entity with 'message' kind and a datastore generated ID
        sets user, text, and time of the Entity
        returns the Entity
    """
    def to_Entity(self):
        kind = 'message'
        m_key = messages_stored.key(kind)
        m = datastore.Entity(key=m_key)
        m['user'] = self.user
        m['text'] = self.text
        m['time'] = self.time
        return m


class ChatManager():
    """A class for managing chat messages."""

    def __init__(self):
        """Initialize the ChatManager with a new list of messages."""

        self.messages = []    

    def add_message(self, msg):
        """Add a message to the datastore client after converting it to an datastore Entity""" 

        messages_stored.put(msg.to_Entity())


    def create_message(self, user, text):
        """Create a new message with the current timestamp."""
        
        self.add_message(Message(clean(user), clean(text)))

    """ method to convert Entity to a Message object
        gets the user, text, and time from the Entity
        returns the Message object
    """
    def to_Message(self, enti):
        user = enti['user']
        text = enti['text']
        time = enti['time']
        m = Message(user, text, time)
        return m

    def get_messages_output(self):
        """ Return the current message contents as a plain text string.
            Converts entity in the query to a Message object first before appending to result string
        """

        result = ''
        query = messages_stored.query(kind='message')
        for entity in query.fetch():
            msg = self.to_Message(entity)
            result += str(msg)
            result += '\n'
        return result

    def get_messages_html(self):
        """ Return the current message contents as HTML.
            Converts entity in the query to a Message object first...
            ...before converting to HTML and appending to result string
        """

        result = ''
        query = messages_stored.query(kind='message')
        # Order query by earliest time
        query.order = ['time']
        for entity in query.fetch():
            msg = self.to_Message(entity)
            result += msg.to_html()
            result += '\n'
        return result


    def clear_messages_before(self, time):
        """ Remove all messages prior to a given time.
            Converts entity in the query to a Message object to compare time
            Deletes entity from datasore client
        """
        
        query = messages_stored.query(kind='message')
        for entity in query.fetch():
            msg = self.to_Message(entity)
            if(msg.time.replace(tzinfo=None) < time.replace(tzinfo=None)):
                messages_stored.delete(entity)


  