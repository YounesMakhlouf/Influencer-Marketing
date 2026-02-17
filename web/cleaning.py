import logging
import re
import string

from unidecode import unidecode

logger = logging.getLogger(__name__)

_stopwords_en: set[str] | None = None
_nlp = None
_translator = None


def _get_stopwords() -> set[str]:
    global _stopwords_en
    if _stopwords_en is None:
        from nltk.corpus import stopwords

        _stopwords_en = set(stopwords.words("english"))
    return _stopwords_en


def _get_nlp():
    global _nlp
    if _nlp is None:
        import spacy

        _nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    return _nlp


def _get_translator():
    global _translator
    if _translator is None:
        from deep_translator import GoogleTranslator

        _translator = GoogleTranslator(source="auto", target="en")
    return _translator


def clean_and_process_content(content):
    """
    Clean and process text content through URL removal, special character cleaning,
    emoji removal, translation, stopword removal, and lemmatization.

    Args:
        content (str): The text content to be cleaned.

    Returns:
        str: The cleaned and lemmatized content.
    """

    try:
        # Removing URLs
        content = re.sub(r"http\S+", "", content)

        # Removing Special Characters
        content = re.sub(r"\W+", " ", content)

        # Removing Emojis
        content = unidecode(content)

        # Translating text (if not in English)
        content = _get_translator().translate(content)
    except Exception as e:
        logging.error(
            f"An exception occurred during cleaning or translation: {e}. Proceeding with original content without translation."
        )

    content = content.lower().translate(str.maketrans("", "", string.punctuation))

    # Removing Stopwords
    words = content.split()
    content = " ".join([word for word in words if word not in _get_stopwords()])

    # Lemmatizing Text
    try:
        doc = _get_nlp()(content)
        content = " ".join([token.lemma_ for token in doc])
    except Exception as e:
        logging.error(f"Lemmatization error: {e}.")

    return content
