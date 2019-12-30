import math

DEFAULT_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class ShortLink:
    def __init__(self, alphabet=DEFAULT_ALPHABET):
        if len(alphabet) < 2:
            raise ValueError('alphabet must contain at least two characters.')
        self.alphabet = alphabet
        self.base = len(alphabet)

    def encode(self, num):
        if not isinstance(num, int) or num < 0:
            raise ValueError('num must be a zero or posative integer.')
        elif num == 0:
            return self.alphabet[0]

        l = []
        while num > 0:
            rem = num % self.base
            num = math.floor(num / self.base)
            l.append(self.alphabet[rem])
        l.reverse()
        return ''.join(l)

    def decode(self, string):
        if string == '' or string is None:
            raise ValueError('string cannot be a null or empty string.')

        n = 0
        for ch in list(string):
            pos = self.alphabet.find(ch)
            if pos == -1:
                raise ValueError(
                    'string contained characters not present in the alphabet.'
                )
            n = (n * self.base) + pos
        return n


class FlaskShortLink():
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('SHORTLINK_ALPHABET', DEFAULT_ALPHABET)
        self.shortlink = ShortLink(app.config['SHORTLINK_ALPHABET'])

    def encode(self, num):
        return self.shortlink.encode(num)

    def decode(self, string):
        return self.shortlink.decode(string)
