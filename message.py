"""Message class for ;; bot."""


class Message:
    """Define a message to send."""

    PLAIN = 0           # text
    LINE = 1            # `text`
    BLOCK = 2           # ```text```

    def __init__(self, text, style=LINE, private=False, tts=False, channel=None):
        """Initialize Message."""
        self.text = text
        if style == self.LINE:
            self.text = '`' + text + '`'
        elif style == self.BLOCK:
            self.text = '`' * 3 + '\n' + text + '`' * 3
        self.private = private
        self.tts = tts
        self.channel = channel

    def get_channel(self, author, channel):
        """Return destination channel."""
        if self.private:
            return author
        elif self.channel is not None:
            return self.channel
        else:
            return channel
