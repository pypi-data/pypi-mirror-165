"""
A word class for phonetic analysis.
"""
class Word:
    """
    Represent a word.
    """
    def __init__(self, word, vowels = None, consonants = None):

        if vowels is None:
            vowels = ['a', 'e', 'i', 'o', 'u']

        if consonants is None:
            consonants = []

        self._vowels = vowels
        self._consonants = consonants
 
        if isinstance(word, str):
            lst_word = self._string_to_word(word)
        elif isinstance(word, (list, tuple, str)):
            lst_word = word
        else:
            raise TypeError('A Word must be built from a string or an iterable.')

        self._word = lst_word
        self._word_str = ' '.join(lst_word)
        self._cv = self.to_cv()

    @property
    def vowels(self):
        return self._vowels

    @property
    def consonants(self):
        return self._consonants

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, new_word):
        self._word = new_word
        self._cv = self.to_cv()
        self._word_str = ' '.join(self._word)

    @property
    def cv(self):
        return self._cv

    @property
    def word_str(self):
        return self._word_str

    def __str__(self):
        return ' '.join(self.word)

    def __len__(self):
        return self.word.__len__()

    def __iter__(self):
        return self.word.__iter__()

    def __reversed__(self):
        return self._word.__reversed__()

    def __getitem__(self, index):
        return self.word.__getitem__(index)

    def __contains__(self, char):
        return self.word.__contains__(char)

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __ne__(self, other):
        return self.word.__ne__(other.word)

    def __setitem__(self, index, value):
        return self.word.__setitem__(index, value)

    def _string_to_word(self, word):
        """
        Parse a word into a list of segments.

        Parameters
        ----------
        word : str
            A word as a sequence of characters.

        Returns
        -------
        list
            A word as a sequence of segments in a list.
        """
        # Get compound segments and sort them by size in descending order
        all_chars = self.vowels + self.consonants
        chars_ = [segment for segment in all_chars if len(segment) > 1]
        chars = sorted(chars_, key=len, reverse = True)

        lst_word = []
        while word != '':
            # Get maximal distance from left to right
            char_len = 1
            for char in chars:
                if word.startswith(char):
                    char_len = len(char)
                    break

            # Split word
            segment = word[0:char_len]
            word = word[char_len:]
            lst_word.append(segment)
        return lst_word

    def startswith(self, segment):
        """
        Check if :class:`Word` starts with a segment.

        Parameters
        ----------
        segment : str
            A character.

        Returns
        -------
        bool
           `True` if the word starts with a segment. Otherwise, it is False.
        """
        return self[0] == segment

    def endswith(self, segment):
        """
        Check if :class:`Word` ends with a segment.

        Parameters
        ----------
        segment : str
            A character.

        Returns
        -------
        bool
            `True` if the word ends with a segment. Otherwise, it is False.
        """
        maxIndex = len(self) - 1
        return self[maxIndex] == segment

    def reverse(self):
        """
        Reverse the word segment.
        """
        self.word = [element for element in self.__reversed__()]

    def is_minimal_pair(self, other):
        """
        Check if the word and `other` are minimal pairs.

        When two words are different in one segment, this difference
        must be between segments of the same type. For example, 
        `cana` and `canu` are minimal pairs, while `cana` and `cant`
        are not.

        Parameters
        ----------
        other : :class:`Word`
            A segment representation of a word to be compared.

        Returns
        -------
        bool
            `True` if it is minimal pair. Otherwise, return `False`.
        """
        if not len(self) == len(other):
            # If both do not have the same len
            return False

        if self == other:
            # If both have the same segments
            return False

        if self.cv != other.cv:
            # If both do not have the same CV pattern
            return False

        diff_counter = 0
        for i in range(0, len(self)):
            if self[i] != other[i]:
                diff_counter+=1

            if diff_counter > 1:
                return False
        return True

    def to_cv(self):
        """
        Convert to CV.

        Returns
        -------
        str
            A cv representation of a word
        """
        cv_pattern = []
        for segment in self:
            if segment in self._vowels:
                cv_pattern.append('V')
            else:
                cv_pattern.append('C')
        cv_pattern= ''.join(cv_pattern)
        return cv_pattern

    def get_invalid_segments(self):
        """
        Get a list of invalid segments in a word

        Returns
        -------
        list
            Only invalid segments
        """
        valid_segment_list = self._vowels + self._consonants
        return [phon for phon in self if not phon in valid_segment_list]
