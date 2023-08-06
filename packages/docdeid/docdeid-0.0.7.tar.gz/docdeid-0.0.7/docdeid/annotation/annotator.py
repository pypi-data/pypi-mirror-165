import re
from abc import ABC, abstractmethod

from docdeid.annotation.annotation import Annotation
from docdeid.document.document import Document
from docdeid.datastructures import LookupTrie
from docdeid.string.processor import BaseStringProcessor

from typing import Optional


class BaseAnnotator(ABC):
    """
    An annotator annotates a text based on its internal logic and rules, and outputs a list of annotations.
    """

    @abstractmethod
    def annotate(self, document: Document):
        """Annotate the document."""


class LookupAnnotator(BaseAnnotator):
    """Annotate tokens based on a list of lookup values"""

    def __init__(self, lookup_values: list[str], category: str):
        self.lookup_values = lookup_values
        self.category = category
        super().__init__()

    def annotate(self, document: Document):
        tokens = document.tokens

        document.add_annotations(
            [
                Annotation(
                    text=token.text,
                    start_char=token.start_char,
                    end_char=token.end_char,
                    category=self.category,
                )
                for token in tokens
                if token.text in self.lookup_values
            ]
        )


class RegexpAnnotator(BaseAnnotator):
    """Annotate text based on regular expressions"""

    def __init__(self, regexp_patterns: list[re.Pattern], category: str, capturing_group: int = 0, ):
        self.regexp_patterns = regexp_patterns
        self.category = category
        self.capturing_group = capturing_group
        super().__init__()

    def annotate(self, document: Document):

        for regexp_pattern in self.regexp_patterns:

            for match in regexp_pattern.finditer(document.text):

                text = match.group(self.capturing_group)
                start, end = match.span(self.capturing_group)

                document.add_annotation(Annotation(text, start, end, self.category))


class MetaDataAnnotator(BaseAnnotator):
    """A simple annotator that check the metadata (mainly testing)."""

    def __init__(self, category: str):
        self.category = category
        super().__init__()

    def annotate(self, document: Document):

        for token in document.tokens:
            if token.text == document.get_meta_data_item("forbidden_string"):
                document.add_annotation(
                    Annotation(
                        token.text, token.start_char, token.end_char, self.category
                    )
                )


class TrieAnnotator(BaseAnnotator):

    def __init__(self, trie: LookupTrie, category: str, string_processors: Optional[list[BaseStringProcessor]] = None):
        self._trie = trie
        self._category = category
        self._string_processors = string_processors

    @staticmethod
    def apply_string_processors(text: str, string_processors: list[BaseStringProcessor]) -> str:
        """ TODO: This should be a StringProcessingPipeline. Also now we have no guarantee there are no filters. """
        for string_processor in string_processors:
            text = string_processor.process_item(text)

        return text

    def annotate(self, document: Document):

        tokens = list(document.tokens)
        tokens_text = [token.text for token in tokens]

        if self._string_processors is not None:
            tokens_text = [self.apply_string_processors(text, self._string_processors) for text in tokens_text]

        for i in range(len(tokens_text)):

            longest_matching_prefix = self._trie.longest_matching_prefix(tokens_text[i:])

            if longest_matching_prefix is None:
                continue

            matched_tokens = tokens[i: i + len(longest_matching_prefix)]
            start_char = matched_tokens[0].start_char
            end_char = matched_tokens[-1].end_char

            document.add_annotation(
                Annotation(
                    text=document.text[start_char:end_char],
                    start_char=start_char,
                    end_char=end_char,
                    category=self._category
                )
            )

            i += len(longest_matching_prefix)

