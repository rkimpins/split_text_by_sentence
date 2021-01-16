A program to split a text file into sentences.

I needed to split a text into sentences to train it on textgenrnn from https://github.com/minimaxir/textgenrnn
I was surprised to learn this isn't a trivial job. A couple surprising factors to consider are:
* Splitting on periods doesn't factor in abbreviations.
* Do we split text within quotations?
* What about parenthesis, brackets, dashes, etc?
* When does punctuation at the end of but inside a quotation end the sentence?
* How do you tell if the sentence ended after a quotation when punctuation is ambivelent?

I tried the nltk sentence splitter but it missed some obvious cases and wasn't satisfactory

That is all. If you find this useful I'm glad!
