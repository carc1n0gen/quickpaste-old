from pygments.lexers import TextLexer
from app import util


class MockLexer:
    @staticmethod
    def analyse_text(text):
        if text == 'Hello world!':
            return 0.5
        elif text == 'quack quack':
            return 0.2
        return 0.9


class MockLexer2:
    @staticmethod
    def analyse_text(text):
        if text == 'Hello world!':
            return 0.0
        elif text == 'quack quack':
            return 1.0
        return 0.3


def test_should_return_text_lexer_when_min_no_good_confidence_found(monkeypatch):
    def mock__iter_lexerclasses():
        return [MockLexer, MockLexer2]
    monkeypatch.setattr(util, '_iter_lexerclasses', mock__iter_lexerclasses)

    lexer = util.find_best_lexer('Hello world!')
    assert isinstance(lexer, TextLexer)


def test_should_return_mock2_when_confidence_1_0(monkeypatch):
    def mock__iter_lexerclasses():
        return [MockLexer, MockLexer2]
    monkeypatch.setattr(util, '_iter_lexerclasses', mock__iter_lexerclasses)

    lexer = util.find_best_lexer('quack quack')
    assert isinstance(lexer, MockLexer2)


def test_should_return_mock_when_min_confidence_met(monkeypatch):
    def mock__iter_lexerclasses():
        return [MockLexer, MockLexer2]
    monkeypatch.setattr(util, '_iter_lexerclasses', mock__iter_lexerclasses)

    lexer = util.find_best_lexer('the quick brown fox jumps over the lazy dog')
    assert isinstance(lexer, MockLexer)
