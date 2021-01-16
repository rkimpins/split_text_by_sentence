# Given a piece of text, a position, and a list of abbreviations
# checks if current position is at the start of an abbreviation
def match_abbreviation(text, pos, abbrs):
    """Checks if the current text position matches the start of an abbreviation"""

    for abbr in abbrs:
        if text[pos:pos + len(abbr)] == abbr:
            return True
    return False

def is_capitalized(text, pos, caps):
    """Checks if the current text position matches that start of a capitalized word"""
    for cap in caps:
        if text[pos:pos+len(cap)] == cap:
            return True
    return False

def only_one_true(bool_list):
    """Returns True if exactly one element of a list is True"""
    counter = 0
    for val in bool_list:
        if val:
            counter += 1
    return counter == 1

def split_text(text, abbreviations=[], capitalized=[], quotations=[("\"", "\""), ("“", "”")],
terminating_characters = ["!","?","."], full_stop_characters = ["."]):
    """Splits a piece of text into a list of sentences

    Parameters
    ----------
    text: string
        the text that we wish to split by sentence
    abbreviations: list[string]
        list of abbreviations that we want to avoid splitting on (each ends in a period)
    capitalized: list[string]
        list of words that are always capitalized in our text, mostly names
        It is rarely necessary to include words other than names
    quotations: list[(char, char)]
        tuple of opening and closing quotations
        Most common choices are: "", “”, (), [], {}, ‘’, ——
        Not, single quotations are not advised since program doesn't differentiate their
        appearance in contraction like "don't"
    terminating_characters: list[char]
        list of characters that terminate a sentence
    full_stop_characters: list[char]
        list of characters that terminate a sentence in quotations

    Returns
    -------
    list[string]
        list of split sentences


    There are a few important notes to make.
    This program does not break sentences that are contained within quotes
    This program handles nested quotations by always continuing if inside multiple sets.
    Program does not consider a newline characters as a sentence break


    Breaking A Sentence Logic
    -------------------------
    If character is a quotation:
        continue + housekeeping
    elif character begins an abbreviation
        skip to the end of the abbreviation
    elif character is a terminating character
        if we are in quotes
            if character is full stop at end of quotes, break including quote
            elif character isn't full stop
                if at end of quote and starting a new sentence: break
        elif not in quotes
            include closing parenthesis, otherwise break normally


    For a more expansive list of abbreviations and capitalized words (names), check out
    https://github.com/DictionaryHouse/EnglishName/
    https://github.com/fangpsh/Abbreviations
    """

    in_quotes = [False for _ in range(len(quotations))]
    result = []
    open_quotations = [x[0] for x in quotations]
    close_quotations = [x[1] for x in quotations]

    pos = 0
    prev_pos = 0
    text_len = len(text)
    while pos < text_len:
        #If char is a quotation, continue
        if text[pos] in open_quotations:
            index = open_quotations.index(text[pos])
            in_quotes[index] = not in_quotes[index]
            pos += 1
        elif text[pos] in close_quotations:
            index = close_quotations.index(text[pos])
            in_quotes[index] = not in_quotes[index]
            pos += 1
        #If char starts an abbreviation, skip to the end of the abbreviation
        elif match_abbreviation(text, pos, abbreviations):
            while text[pos] != ".":
                pos += 1
            pos += 1
        elif text[pos] in terminating_characters:
            if only_one_true(in_quotes):
                if text[pos] in full_stop_characters and only_one_true(in_quotes):
                    #Break on period only if at the end of a quote and only 1 nested quote
                    if text[pos+1] in close_quotations:
                        #in_quotes = not in_quotes
                        index = close_quotations.index(text[pos+1])
                        in_quotes[index] = not in_quotes[index]

                        result.append(text[prev_pos:pos+2])
                        pos = pos + 3
                        prev_pos = pos
                    else:
                        pos += 1
                else:
                    #If non-period terminating character, check if text starts a new sentence
                    if text[pos+1] in close_quotations:
                        if text[pos+3].islower():
                            pos += 1
                        elif text[pos+3].isupper() and is_capitalized(text, pos+3, capitalized):
                            pos += 1
                        elif text[pos+3].isupper() and not is_capitalized(text, pos+3, capitalized):
                            result.append(text[prev_pos:pos+2])
                            pos = pos + 3
                            prev_pos = pos
                            #in_quotes = not in_quotes
                            index = close_quotations.index(text[pos+1])
                            in_quotes[index] = not in_quotes[index]
                    else:
                        pos += 1
            #If nested within multiple quotes, just get out of there
            elif any(in_quotes):
                pos += 1
            else:
                #Include closing parenthesis when terminated inside it
                if pos != text_len - 1 and text[pos+1] in [")", "]", "}"]:
                    result.append(text[prev_pos:pos+2])
                    pos = pos + 3
                    prev_pos = pos
                #Do a normal break on terminating character
                else:
                    result.append(text[prev_pos:pos+1])
                    pos = pos + 2
                    prev_pos = pos
        else:
            pos += 1

    return result

def tokenize(filename, output):
    """Takes input and output file names and splits into list of sentences

    Parameters
    ----------
    filename: string
        name of file we wish to read text from to split
    output: string
        name of file to write output to

    Returns
    -------
        writes to file each sentence on a new line

    Uses a very simple set of abbreviations and capitalized words as laid out in text files
    abbreviations.txt and names.txt
    These files are in the format
    entry1
    entry2
    ...
    entry3
    """

    with open("abbreviations.txt", "r") as file:
        abbr = file.read().splitlines()
    with open("names.txt", "r") as file:
        cap = file.read().splitlines()

    with open(filename, "r") as file:
        data = file.read()

    result = split_text(data, abbreviations=abbr, capitalized=cap)

    with open(output, "w") as file:
        for sentence in result:
            file.write(sentence + '\n')

def main():
    filename = input("Enter file name to split:")
    output = input("Enter output file name:")
    tokenize(filename, output)

if __name__ == "__main__":
    main()
