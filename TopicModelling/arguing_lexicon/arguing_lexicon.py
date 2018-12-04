import os
import re

from spacy.tokens import Doc
from spacy_arguing_lexicon.arguments import ArgumentTexts
from spacy_arguing_lexicon.exceptions import LexiconMissingError


class ArguingLexiconParser(object):

    MACROS_PATH = os.path.join(os.path.dirname(__file__), "lexicon", "{}", "macros")
    PATTERNS_PATH = os.path.join(os.path.dirname(__file__), "lexicon", "{}", "patterns")

    MACRO_PATTERN = re.compile("(@[A-Z0-9]+)")

    MACROS = {}
    PATTERNS = {}

    def package_check(self, lang):
        if not os.path.exists(self.MACROS_PATH.format(lang)):
            raise LexiconMissingError(
                "Trying to load Arguing Lexicon without macros file for language {}".format(lang)
            )
        if not os.path.exists(self.PATTERNS_PATH.format(lang)):
            raise LexiconMissingError(
                "Trying to load Arguing Lexicon without patterns file for language {}".format(lang)
            )

    def load_macros(self, lang):
        for entry in os.listdir(self.MACROS_PATH.format(lang)):
            if not entry.endswith(".tff"):
                continue
            with open(os.path.join(self.MACROS_PATH.format(lang), entry)) as macro_file:
                for macro_line in macro_file.readlines():
                    # Skip empty lines, class definitions and comments
                    if not macro_line.strip():
                        continue
                    if macro_line.startswith("#"):
                        continue
                    # Add macros
                    macro_label, macro_definition = self.preprocess_pattern(macro_line).split("=")
                    macro = [mcr.strip() for mcr in macro_definition.strip().strip("{}").split(",")]
                    self.MACROS[macro_label] = macro

    def preprocess_pattern(self, pattern):
        stripped_pattern = pattern.replace("\\'", "'").strip()
        return "{}\\b".format(stripped_pattern)  # the \b makes sure that a match ends with a non-word token

    def compile_pattern(self, pattern):
        macro_match = self.MACRO_PATTERN.search(pattern)
        if macro_match is None:
            yield re.compile(self.preprocess_pattern(pattern), flags=re.IGNORECASE)
        else:
            macro = macro_match.group(0)
            macro_replacement = "|".join(self.MACROS[macro])
            replaced_pattern = pattern.replace(macro, macro_replacement)
            for preprocessed_pattern in self.compile_pattern(replaced_pattern):
                yield preprocessed_pattern

    def load_patterns(self, lang):
        for entry in os.listdir(self.PATTERNS_PATH.format(lang)):
            if not entry.endswith(".tff"):
                continue
            with open(os.path.join(self.PATTERNS_PATH.format(lang), entry)) as patterns_file:
                pattern_class = None
                for pattern_line in patterns_file.readlines():
                    # Skip empty lines and comments
                    if not pattern_line.strip():
                        continue
                    if pattern_line.startswith("#") and pattern_class:
                        continue
                    # Read pattern class
                    elif pattern_line.startswith("#"):
                        trash, pattern_class = pattern_line.replace('"', "").split("=")
                        pattern_class = pattern_class.strip()
                        self.PATTERNS[pattern_class] = []
                        continue
                    # Add patterns
                    for preprocessed_patterns in self.compile_pattern(pattern_line):
                        self.PATTERNS[pattern_class].append(preprocessed_patterns)

    def get_arguing_matches(self, doc):
        for arguing_label, arguing_patterns in self.PATTERNS.items():
            for arguing_pattern in arguing_patterns:
                match = arguing_pattern.search(doc.text)
                if match is not None:
                    yield arguing_label, match

    def get_lexicon_vocabulary(self):
        vocabulary = set()
        for label, patterns in self.PATTERNS.items():
            for compiled in patterns:
                words = "".join([char if char.isalnum() or char == "'" else " " for char in compiled.pattern])
                for word in words.split(" "):
                    if len(word) <= 1 and not word == "I":
                        continue
                    vocabulary.add(word)
        return vocabulary

    def __init__(self, lang="en"):
        super().__init__()
        self.package_check(lang)
        self.load_macros(lang)
        self.load_patterns(lang)
        if not Doc.has_extension('arguments'):
            Doc.set_extension('arguments', getter=ArgumentTexts(self), force=True)
        else:
            default, method, getter, setter = Doc.get_extension('arguments')
            assert isinstance(getter, ArgumentTexts), \
                "Expected 'arguments' extension to be of type ArgumentTexts " \
                "but found {}. Namespace clash?".format(type(Doc.get_extension('arguments')))

    def __call__(self, doc):
        # All parsing is lazy
        return doc
