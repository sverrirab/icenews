import os
import logging

from reynir import Reynir
from reynir.bintokenizer import tokenize, TOK
from collections import defaultdict

logger = logging.getLogger(__name__)

_NLP = Reynir()
_INDENT = " " * 8
_VERBOSE = int(os.environ.get("ICENEWS_VERBOSE", "0"))


_DEFAULT_IMPORTANT_THRESHOLD = 0.7
_DEFAULT_MAX_TOKENS = 100
_DEFAULT_MAX_WORDS = 30
_MIN_WORD_COUNT = 10

_UNCLASSIFIED_WEIGHT = 0.25
_UNCLASSIFIED_NAME = 2.5
_NORMAL_WEIGHT = 0.5
_KVKHK_WEIGHT = 0.75
_NUMBER_WEIGHT = 1.5
_URL_WEIGHT = 2.0
_DATE_WEIGHT = 3.0
_TITLE_WEIGHT = 3.0
_LOCATION_WEIGHT = 4.0
_ENTITY_WEIGHT = 5.0

_IGNORED_CONCEPTS = {"sem/so/alm/", "var/lo/alm", "vera/so/alm", "hafa/so/alm"}


def _output_log(*args):
    logger.info(" C: " + " ".join([str(a) for a in args]))


def get_lemma(token):
    result = set()
    for val in token.val:
        result.add(val.stofn)
    return result


def simplify_val(vals):
    """
    Remove stopwords, personal pronouns etc
    Reduce the number of results to the first in each "class" - e.g. one ao, one lo etc
    :param vals:
    :return:
    """
    result = {}
    suspected_small_word = False
    lo_or_no = False
    abbreviation = None
    ignored_concept = False
    if _VERBOSE > 2:
        _output_log("vals:", repr(vals))
    for val in vals:
        unique = "{}/{}".format(val.ordfl, val.fl)
        full = "{}/{}".format(val.stofn, unique)
        if _VERBOSE > 2:
            _output_log("full:", full)
        if full in _IGNORED_CONCEPTS:
            if _VERBOSE > 2:
                _output_log("This is on the ignored list!")
            ignored_concept = True
            continue
        if unique in result:
            if _VERBOSE > 2:
                _output_log("simplify_val - ignoring:", val)
            continue
        if val.ordfl in ["fs", "ao", "st", "uh", "nhm", "fn", "pfn", "abfn"]:
            if _VERBOSE > 2:
                _output_log("simplify_val - type:", val.ordfl, " ignoring:", val)
            suspected_small_word = True
            continue
        if val.fl == "skst":
            abbreviation = val
            continue
        if val.ordfl in ["lo", "no"]:
            lo_or_no = True
        result[unique] = val

    if ignored_concept or (suspected_small_word and not lo_or_no):
        if _VERBOSE > 1:
            _output_log("simplify_val - skipping:", result.values())
        return {}
    if abbreviation is not None:
        if _VERBOSE > 1:
            _output_log("simplify_val - abbreviation:", abbreviation)
        return [abbreviation]
    if _VERBOSE > 1:
        _output_log(
            "simplify_val - result:", result.values(), "out of previous", len(vals)
        )
    return result.values()


def remove_hyphen(text):
    return text.replace("-", "")


def is_name(text):
    """
    Checks if text sounds like a name or abbreviation (title or upper case).
    :param text: the text to check.
    :return: True if it might be a name.
    """
    return text.istitle() or text.isupper()


class Concept(object):
    def __init__(self, concept, weight=1.0):
        self.concept = concept
        self.weight = weight


class Concepts(object):
    def __init__(self):
        self._concepts = defaultdict(int)
        self._count = 0

    def extract(self, text, max_tokens=_DEFAULT_MAX_TOKENS):
        tokens = 0
        for sent in text.split("\n"):
            if _VERBOSE > 1:
                _output_log("Parsing sentence:", sent)

            first_token_in_sentence = True
            unclassified_names = []
            for t in tokenize(sent):
                add_unclassified_name = False
                if _VERBOSE > 2:
                    _output_log("Parsing token:", t)
                if t.kind in [TOK.S_BEGIN, TOK.P_BEGIN]:
                    first_token_in_sentence = True
                elif t.kind >= TOK.P_BEGIN:
                    pass
                elif t.kind == TOK.PUNCTUATION:
                    pass
                elif t.kind in [
                    TOK.DATE,
                    TOK.YEAR,
                    TOK.TIME,
                    TOK.DATEABS,
                    TOK.DATEREL,
                    TOK.TIMESTAMPABS,
                    TOK.TIMESTAMPREL,
                ]:
                    if _VERBOSE > 1:
                        _output_log(_INDENT, "DATE:", t)
                    self.add(t.txt, _DATE_WEIGHT)
                elif t.kind in [
                    TOK.NUMBER,
                    TOK.ORDINAL,
                    TOK.AMOUNT,
                    TOK.PERCENT,
                    TOK.MEASUREMENT,
                ]:
                    if _VERBOSE > 1:
                        _output_log(_INDENT, "NUMBER:", t)
                    self.add(t.txt, _NUMBER_WEIGHT)
                elif t.kind in [TOK.URL, 24]:
                    if _VERBOSE > 1:
                        _output_log(_INDENT, "URL:", t)
                    self.add(t.txt.lower(), _URL_WEIGHT)
                elif t.kind == TOK.PERSON:
                    if _VERBOSE > 1:
                        _output_log(_INDENT, "PERSON:", t)
                    self.add(t.val[0].name, _ENTITY_WEIGHT)
                elif t.kind == TOK.WORD:
                    if _VERBOSE > 1:
                        _output_log(_INDENT, "WORD:", t.txt)

                    if not t.val:
                        if is_name(t.txt):
                            add_unclassified_name = True
                        else:
                            if _VERBOSE > 1:
                                _output_log(_INDENT, "UNCLASSIFIED:", t.txt)
                            self.add(t.txt, _UNCLASSIFIED_WEIGHT)
                    else:
                        if first_token_in_sentence and t.txt in {"Á", "Í"}:
                            # Í or Á in the beginning of sentence.
                            pass
                        else:
                            self._add_token_concepts(t)
                else:
                    if _VERBOSE > -1:
                        _output_log(_INDENT, "IGNORING:", t)

                if t.kind < TOK.P_BEGIN:
                    first_token_in_sentence = False

                if add_unclassified_name:
                    unclassified_names.append(t.txt)
                else:
                    self._handle_unclassified_names(unclassified_names)
                tokens += 1
                if tokens > max_tokens:
                    break

            # If the sentence ends with unclassified names.
            self._handle_unclassified_names(unclassified_names)

    def _handle_unclassified_names(self, names):
        if len(names) > 0:
            full = " ".join(names)
            if _VERBOSE > 1:
                _output_log(_INDENT, "UNCLASSIFIED NAMES:", full)

            self.add(full, _UNCLASSIFIED_NAME)
            names.clear()

    def _add_token_concepts(self, t):
        if _VERBOSE > 2:
            for val in t.val:
                _output_log("   VAL:", val.fl, val)
        simplified = simplify_val(t.val)

        if len(simplified) == 0:
            if _VERBOSE > 1:
                _output_log(_INDENT * 2, "Ignored", t.txt)
            return

        for val in simplified:
            if t.txt.count("-") != val.stofn.count("-"):
                # Prenvent removal of hyhpens e.g. NBA-Deildin
                stofn = remove_hyphen(val.stofn)
            else:
                stofn = val.stofn

            if val.fl == "lönd":
                weight = _LOCATION_WEIGHT
            elif val.fl == "skst":
                stofn = val.ordmynd
                weight = _ENTITY_WEIGHT
            elif is_name(stofn):
                weight = _TITLE_WEIGHT
            elif val.ordfl in ["kk", "hk", "kvk"]:
                if val.fl in ["fyr"]:
                    weight = _ENTITY_WEIGHT
                else:
                    weight = _KVKHK_WEIGHT
            else:
                weight = _NORMAL_WEIGHT
            self.add(stofn, weight / len(simplified))

    def add(self, concept, weight=1.0):
        self._count += 1
        if _VERBOSE > 1:
            _output_log("adding weight", concept, weight)
        self._concepts[concept] += weight

    def count(self):
        self._count += 1

    def important(
        self, max_count=_DEFAULT_MAX_WORDS, threshold=_DEFAULT_IMPORTANT_THRESHOLD
    ):
        result = []
        total = sum(self._concepts.values())
        cap = total * threshold
        running = 0.0
        for c in sorted(self._concepts, key=self._concepts.get, reverse=True)[
            :max_count
        ]:
            w = self._concepts[c]
            if running > cap:
                if len(result) > _MIN_WORD_COUNT:
                    break
            running += w
            result.append(c)
        return result

    def report(
        self, max_count=_DEFAULT_MAX_WORDS, threshold=_DEFAULT_IMPORTANT_THRESHOLD
    ):
        _output_log("Concepts report for {} items:".format(self._count))
        _output_log("Sum:", sum(self._concepts.values()))
        _output_log("Len:", len(self._concepts))
        _output_log(self._concepts)
        for c in self.important(max_count, threshold):
            w = self._concepts[c]
            _output_log("  {:.2f} {}".format(w, c))
        _output_log(" -" * 20)
