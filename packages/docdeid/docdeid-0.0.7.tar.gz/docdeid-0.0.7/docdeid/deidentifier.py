from typing import Optional, Union

from docdeid.annotation.annotation_processor import BaseAnnotationProcessor
from docdeid.annotation.annotator import BaseAnnotator
from docdeid.annotation.redactor import BaseRedactor, SimpleRedactor
from docdeid.document.document import Document
from docdeid.tokenizer.tokenizer import BaseTokenizer


class DocDeid:
    """Main class. Needs more docs."""

    def __init__(
        self,
        tokenizer: Optional[BaseTokenizer] = None,
        redactor: Optional[BaseRedactor] = None,
    ):
        """Initialize the deidentifier."""
        self._tokenizer = tokenizer
        self._annotators = {}
        self._annotation_postprocessors = {}
        self._redactor = redactor or SimpleRedactor()

    def add_annotator(self, name: str, annotator: BaseAnnotator):
        """Add annotator to the annotation pipeline"""
        self._annotators[name] = annotator

    def remove_annotator(self, name: str):
        """Remove annotator from the annotation pipeline"""

        try:
            del self._annotators[name]
        except KeyError as ex:
            raise KeyError(f"Trying to remove non-existing annotator {name}.") from ex

    def add_annotation_postprocessor(
        self, name: str, annotation_postprocessor: BaseAnnotationProcessor
    ):
        """Add annotation processor to the post-processing pipeline"""
        self._annotation_postprocessors[name] = annotation_postprocessor

    def remove_annotation_postprocessor(self, name: str):
        """Remove annotation processor from the post-processing pipeline"""

        try:
            del self._annotation_postprocessors[name]
        except KeyError as ex:
            raise KeyError(
                f"Trying to remove non-existing annotation postprocessor {name}."
            ) from ex

    def _annotate(
        self, document: Document, annotators_enabled: list[str] = None
    ) -> Document:
        """Annotate document, and then return it."""

        if annotators_enabled is None:
            annotators_enabled = self._annotators.keys()

        for annotator_name in annotators_enabled:
            self._annotators[annotator_name].annotate(document)

        return document

    def _postprocess_annotations(self, document: Document) -> Document:
        """Applies the annotation_postprocessors in the pipeline."""

        for annotation_processor in self._annotation_postprocessors.values():
            document.apply_annotation_processor(annotation_processor)

        return document

    def _redact(self, annotated_document: Document) -> Document:
        """Deidentify a previously annotated document."""

        annotated_document.apply_redactor(self._redactor)

        return annotated_document

    def deidentify(
        self,
        text: str,
        annotators_enabled: list[str] = None,
        meta_data: Optional[dict] = None,
        return_only_deidentified_text: Optional[bool] = False,
    ) -> Union[Document, str]:
        """Deidentify a single text, by wrapping it in a Document and returning that."""

        document = Document(text, tokenizer=self._tokenizer, meta_data=meta_data)

        self._annotate(document, annotators_enabled)
        self._postprocess_annotations(document)
        self._redact(document)

        if return_only_deidentified_text:
            return document.deidentified_text

        return document
