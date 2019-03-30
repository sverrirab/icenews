# -*- encoding: utf-8 -*-
from .concepts import Concepts

_TOO_FREQUENT_NAMES = {
    "Íslendingur",
    "Ísland",
}
_DEBUG = False


def _filter_weights(weights, limit_percent=50):
    total = sum(weights.values())
    limit = (limit_percent / 100.0) * total
    result = set()
    added = 0
    for text in sorted(weights, key=weights.get, reverse=True):
        result.add(text)
        added += weights[text]
        if added > limit:
            break
    return result


def _debug_weights(weights):
    for text in sorted(weights, key=weights.get, reverse=True):
        print("{}\t{}".format(weights[text], text))
    total = sum(weights.values())
    print("sum total:", total)
    print("most important: ", sorted(_filter_weights(weights)))


def important_words(text, title=None):
    c = Concepts()
    if title:
        # Add multiplication factor?
        c.extract(title)
    c.extract(text)
    return c.important()


def _almost(n, a, b):
    if _DEBUG:
        print("almost", n, a, b, n >= ((min(a, b) + 1) // 2))
    return n >= ((min(a, b) + 1) // 2)


def similar(a, b):
    """
    Checks if wordlists are *very* similar in a *very naive* way.
    :param a: set of words
    :param b: set of words
    :return: True if the word lists are similar
    """
    count = 0
    for w in a:
        if w in b:
            count += 1

    return _almost(count, len(a), len(b))


def similar_articles(a, b):
    """
    Checks if wordlists sound like they are from similar articles
    :param a: set of words from article A
    :param b: set of words from article B
    :return: True if the wordlists are from similar articles
    """
    # Use the longer list as a reference.
    if len(a) < len(b):
        t = a
        a = b
        b = t

    # Filter out "names" (capitalized words).  Start with the longest words so we can merge partial names.
    # e.g. "Donald Trump", "Trump"
    names = set()
    unique_names = 0
    words = set()
    for w in sorted(a, key=len, reverse=True):
        if w.istitle():
            if w not in names:
                unique_names += 1
                names.add(w)
            names.update(w.split())
        else:
            words.add(w)
    if _DEBUG:
        print("names", names)
        print("unique_names", unique_names)
        print("words", words)

    matching_names = 0
    non_matching_names = 0
    matching_words = 0
    weak_matches = 0
    strong_matches = 0
    for i, w in enumerate(b):
        if w.istitle():
            if w in _TOO_FREQUENT_NAMES:
                weak_matches += 1
            elif w in names:
                if i < 5:
                    strong_matches += 1
                matching_names += 1
            else:
                non_matching_names += 1
        else:
            if w in words:
                if i < 5:
                    strong_matches += 1
                matching_words += 1

    if _DEBUG:
        print("matching_names", matching_names)
        print("non_matching_names", non_matching_names)
        print("matching_words", matching_words)
        print("weak_matches", weak_matches)
        print("strong_matches", strong_matches)

    # If two of the five first words match - strong indication of a match (most important words first)
    if strong_matches > 2:
        if _DEBUG:
            print("many strong matches!")
        return True

    # Most of the names are matching.
    if non_matching_names <= (unique_names // 4) and matching_names >= max(2, unique_names // 2):
        if _DEBUG:
            print("many matching names!")
        return True

    # Take into account all words/names
    return _almost((weak_matches // 2) + strong_matches + matching_names + matching_words, unique_names + len(words), len(b))


def similar_article_wordlists(a, b):
    """
    Takes a semicolon seperated list of words and calls 'similar_articles'
    """
    return similar_articles(a.split(";"), b.split(";"))
