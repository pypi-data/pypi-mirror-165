from dataclasses import dataclass


@dataclass(frozen=True)
class Annotation:
    """
    An annotation is a matched entity in a text, with a text, a start- and end index (character),
    and a category.
    """

    text: str
    start_char: int
    end_char: int
    category: str

    def __post_init__(self):

        if len(self.text) != (self.end_char - self.start_char):
            raise ValueError("The length of the span does not match the text.")

