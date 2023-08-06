from docdeid.datastructures.lookup import LookupList
from docdeid.document.document import Document
from docdeid.tokenizer.tokenizer import SpaceSplitTokenizer


def main1():

    from docdeid import Annotation
    from docdeid.annotation.annotation_processor import MergeAdjacentAnnotations
    from docdeid.annotation.annotator import LookupAnnotator

    text = "Pieter en Maria"

    annotator = LookupAnnotator(
        lookup_values=["Pieter", "Maria"], category="VOORNAAMONBEKEND"
    )
    doc = Document(text=text, tokenizer=SpaceSplitTokenizer())

    annotator.annotate(doc)

    m = MergeAdjacentAnnotations(slack_regexp="[\.\s\-,]?[\.\s]?")
    processed_annotations = m.process(doc.annotations, doc.text)

    print(doc.annotations)
    print(processed_annotations)


if __name__ == "__main__":
    main1()
