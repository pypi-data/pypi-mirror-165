# PhonText
A python package for phonology analysis from text files

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install phontext.

```bash
pip install phontext
```

## Usage

Working with words

```python
from phontext import Word

config = {
    'vowels': ['a', 'e', 'i', 'o', 'u'],
    'consonants': ['p', 't', 'k', 'ch', 'ts', 'rr', 'r']
}

# Parse words into segments
word = Word('chincha', **config)

len(word)
>> 5

word.cv
>> CVCCV

word.word_str
>> ch i n ch a

word.word
>> ["ch", "i","n", "ch", "a"]

# Find minimal pairs

word1 = Word('tasa', **config)
word2 = Word('kasa', **config)
word3 = Word('tasl', **config)

word1.is_minimal_pair(word2)
>> True

word1.is_minimal_pair(word3)
>> False
        
# and much more...

```
Working with wordlist

```python
from phontext import Corpus

words = ['perro', 'pero', 'piso', 'peso']

config = {
    'vowels': ['a', 'e', 'i', 'o', 'u'],
    'consonants': ['p', 't', 'k', 'ch', 'ts', 'rr', 'r']
}

corpus = Corpus(**config)
for word_str in words:
    corpus.append(word_str)
    
segment_stat = corpus.get_segment_frequency()
segment_stat
>> {
    'vowels': {
        'e':3,
        'i':1
    }
    'consonants':{
        'p':4,
        'rr':1
    }
    'others':
        's':2,
        'r':1
}

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)
