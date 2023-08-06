"""
Manage word list for phonology analysis.
"""
from phontext.word import Word

class Corpus:

    def __init__(self, vowels = None, consonants = None):

        if vowels is None:
            vowels = ['a', 'e', 'i', 'o', 'u']

        if consonants is None:
            consonants = []

        self._vowels = vowels
        self._consonants = consonants

        self._data = []

    def __len__(self):
        return self._data.__len__()

    def __iter__(self):
        return self._data.__iter__()

    @property
    def word_list(self):
        return self._data

    @property
    def vowels(self):
        return self._vowels

    @property
    def consonants(self):
        return self._consonants

    def append(self, new_word):
        """
        Add a new word to the Corpus.

        new_word : str, tuple or :class:`Word`
            An item to be added to the corpus.
        """
        if isinstance(new_word, (str, list, tuple)):
            config = {
                'vowels':self._vowels,
                'consonants':self._consonants
            }
            new_word_ = Word(new_word, **config)
        elif isinstance(new_word, Word):
            new_word_ = new_word
        else:
            raise ValueError('Add only str, list, tuple or Word obects.')
        self._data.append(new_word_)

    def get_segment_frequency(self, by_group = True):
        """
        Get the segment occurrences from all entries in the corpus.
        """
        dict_ = {}
        # Get all segments' frequency
        for word in self._data:
            for segment in word:
                if segment in dict_:
                    dict_[segment] += 1
                else:
                    dict_[segment] = 1

        if by_group:
            # Classify by sound category
            vowels = {}
            consonants = {}
            others = {}
            for segment, frequency in dict_.items():
                if segment in self._vowels:
                    vowels[segment] = frequency
                elif segment in self._consonants:
                    consonants[segment] = frequency
                else:
                    others[segment] = frequency

            return {
                'vowels': vowels,
                'consonants': consonants,
                'other': others
            }

        return dict_
