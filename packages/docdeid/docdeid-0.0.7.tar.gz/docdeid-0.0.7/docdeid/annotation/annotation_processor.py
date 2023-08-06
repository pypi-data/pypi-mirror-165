import re
from abc import ABC, abstractmethod

import numpy as np

from docdeid.annotation.annotation import Annotation


class BaseAnnotationProcessor(ABC):
    """An AnnotationProcessor performs operations on a list of annotations."""

    @abstractmethod
    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:
        """
        Process the annotations.

        Args:
            annotations: The input annotations.
            text: The input text.

        Returns: A set of annotations, processed.

        """


class LeftRightOverlapResolver(BaseAnnotationProcessor):
    """Does a pass from left to right, and only includes non-overlapping annotations."""

    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:

        annotations = sorted(list(annotations), key=lambda a: (a.start_char, a.end_char, a.category))

        result = set()
        last_end_char = -1

        for annotation in annotations:

            if annotation.start_char >= last_end_char:
                result.add(annotation)
                last_end_char = annotation.end_char

        return result


class LongestFirstOverlapResolver(BaseAnnotationProcessor):
    """Includes the longest annotation first. If a shorter annotation is a subset of a longer one, it is
    removed. If a shorter one overlaps a longer one, it is shortened accordingly."""

    @staticmethod
    def _zero_runs(a: np.array) -> list[tuple[int, int]]:
        """
        Finds al zero runs in an numpy array.
        From: https://stackoverflow.com/questions/24885092/finding-the-consecutive-zeros-in-a-numpy-array
        """

        iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
        absdiff = np.abs(np.diff(iszero))
        return np.where(absdiff == 1)[0].reshape(-1, 2)

    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:

        if len(annotations) == 0:
            return annotations

        mask = np.zeros(max(annotation.end_char for annotation in annotations))
        processed_annotations = set()

        for annotation in sorted(list(annotations), key=lambda a: (-len(a.text), a.end_char, a.category)):

            mask_annotation = mask[annotation.start_char : annotation.end_char]

            if sum(mask_annotation) == 0:  # no overlap
                processed_annotations.add(annotation)

            else:  # overlap

                for start_char_run, end_char_run in self._zero_runs(mask_annotation):

                    processed_annotations.add(
                        Annotation(
                            text=annotation.text[start_char_run:end_char_run],
                            start_char=annotation.start_char + start_char_run,
                            end_char=annotation.start_char + end_char_run,
                            category=annotation.category,
                        )
                    )

            mask[annotation.start_char : annotation.end_char] = 1

        return processed_annotations


class MergeAdjacentAnnotations(BaseAnnotationProcessor):
    """Merges adjacent annotations of the same category, possibly with some
    slack between them. Assumes no overlap in annotations."""

    def __init__(self, slack_regexp: str = None, check_overlap: bool = True):
        self.slack_regexp = slack_regexp
        self.check_overlap = check_overlap

    @staticmethod
    def has_overlapping_annotations(annotations: set[Annotation]) -> bool:
        """TODO: Make this a property of Annotation or AnnotationSet?"""

        annotations = sorted(list(annotations), key=lambda a: a.start_char)

        for annotation, next_annotation in zip(annotations, annotations[1:]):
            if annotation.end_char > next_annotation.start_char:
                return True

        return False

    def _are_adjacent_annotations(
        self, left_annotation: Annotation, right_annotation: Annotation, text: str
    ) -> bool:

        if left_annotation.category != right_annotation.category:
            return False

        between_text = text[left_annotation.end_char : right_annotation.start_char]

        if self.slack_regexp is None:
            return between_text == ""
        else:
            return re.fullmatch(self.slack_regexp, between_text) is not None

    @staticmethod
    def _adjacent_annotations_replacement(
        left_annotation: Annotation, right_annotation: Annotation, text: str
    ) -> Annotation:

        return Annotation(
            text=f"{left_annotation.text}"
            f"{text[left_annotation.end_char: right_annotation.start_char]}"
            f"{right_annotation.text}",
            start_char=left_annotation.start_char,
            end_char=right_annotation.end_char,
            category=left_annotation.category,
        )

    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:

        if self.check_overlap:
            if self.has_overlapping_annotations(annotations):
                raise ValueError(
                    f"{self.__class__} received input with overlapping annotations."
                )

        annotations = sorted(list(annotations), key=lambda a: (a.start_char, a.end_char, a.category))
        processed_annotations = set()

        for index in range(len(annotations) - 1):

            annotation, next_annotation = annotations[index], annotations[index + 1]

            if self._are_adjacent_annotations(annotation, next_annotation, text):
                annotations[index + 1] = self._adjacent_annotations_replacement(
                    annotation, next_annotation, text
                )
            else:
                processed_annotations.add(annotation)

        processed_annotations.add(annotations[-1])  # add last one

        return processed_annotations
