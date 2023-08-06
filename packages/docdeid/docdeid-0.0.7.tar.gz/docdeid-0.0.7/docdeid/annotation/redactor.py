from abc import ABC, abstractmethod

from docdeid.annotation.annotation import Annotation


class BaseRedactor(ABC):
    """
    A redactor takes as input a text and a list of annotations, and redacts the text, for example by repacing the
    entity by XXXXXX, or by [REDACTED], or by <CATEGORY>.
    """

    @abstractmethod
    def redact(self, text: str, annotations: list[Annotation]) -> str:
        """Redact the text."""


class SimpleRedactor(BaseRedactor):
    """
    A simple redactor that replaces an annotation by [CATEGORY-n], with n being a counter.
    """

    def __init__(self, open_char: str = "[", close_char: str = "]"):
        self.open_char = open_char
        self.close_char = close_char

    def redact(self, text: str, annotations: list[Annotation]):

        annotations = sorted(annotations, key=lambda x: x.end_char)

        annotation_text_to_counter = {}

        for annotation in annotations:

            if annotation.text not in annotation_text_to_counter:
                annotation_text_to_counter[annotation.text] = (
                    len(annotation_text_to_counter) + 1
                )

        for annotation in annotations[::-1]:  # back to front
            text = (
                text[: annotation.start_char] + f"{self.open_char}"
                f"{annotation.category.upper()}"
                f"-"
                f"{annotation_text_to_counter[annotation.text]}"
                f"{self.close_char}" + text[annotation.end_char :]
            )

        return text


class RedactAllText(BaseRedactor):
    """Redacts entire text."""

    def redact(self, text: str, annotations: list[Annotation]):
        """
        Redact the text.

        Args:
            text: The input text (unused).
            annotations: The input annotations (unused).

        Returns: [REDACTED]

        """
        return "[REDACTED]"
