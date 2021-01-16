def test_split_text():
    abbr = [ "Mr.", "mr.", "MR.", "Mrs.", "MRS.", "mrs.", "MRs.", "M.", "Dr.", "DR.", "dr.", "Q." "R." ]
    cap = [ "Mr", "Mrs", "Ramsey", "Lily", "Briscoe", "James", "Paul", "Rayley", "Minta", "Doyle", "Charles",
        "Tansley", "William", "Bankes", "Augustus", "Carmichael", "Andrew", "Jasper", "Roger", "Prue", "Nancy", "Cam",
        "McNab", "Macalister", "Scott" ] 

    text_1 = """br. br! br? "br!" she said. "br. br." "br!" she said. "br!" br. "br!" Ramsey said."""
    expected_1 = [
        'br.',
        'br!',
        'br?',
        '"br!" she said.',
        '"br. br."',
        '"br!" she said.',
        '"br!" br.',
        '"br!" Ramsey said.'
        ]
    assert split_text(text_1, abbreviations=abbr, capitalized=cap) == expected_1
    text_2 = """("br." br). br."""
    expected_2 = [
        '("br." br).',
        'br.'
    ]
#[("\"", "\""), ("“", "”")]
    assert split_text(text_2, abbreviations=abbr, capitalized=cap, 
    quotations=[("\"", "\""), ("“", "”"), ("(", ")")]) == expected_2
    #text_3 = """("br.") Br."""
    #expected_3 = [
    #    '("br.")',
    #    'Br.'
    #]
    #assert split_text(text_3, abbreviations=abbr, capitalized=cap, 
    #quotations=[("\"", "\""), ("“", "”"), ("(", ")")]) == expected_3


def test_match_abbreviation():
    assert match_abbreviation("abc mr. and that mrs.", 4, ["Mr.", "mr.", "mrs."])
    assert not match_abbreviation("abc mr. and that mrs.", 5, ["Mr.", "mr.", "mrs."])
    assert not match_abbreviation("abc mr. and that mrs.", 6, ["Mr.", "mr.", "mrs."])
    assert match_abbreviation("abc mr. and that mrs.", 17, ["Mr.", "mr.", "mrs."])
    assert not match_abbreviation("abc mr. and that mrs.", 18, ["Mr.", "mr.", "mrs."])

# Given a piece of text, a position, and a list of abbreviations
# checks if current position is at the start of an abbreviation
def match_abbreviation(text, pos, abbrs):
    for abbr in abbrs:
        if text[pos:pos + len(abbr)] == abbr:
            return True
    return False

def is_name(text, pos, names):
    for name in names:
        if text[pos:pos+len(name)] == name:
            return True
    return False

def only_one_true(bool_list):
    counter = 0
    for val in bool_list:
        if val:
            counter += 1
    return counter == 1

def split_text(text, abbreviations=[], capitalized=[], quotations=[("\"", "\""), ("“", "”")],
terminating_characters = ["!","?","."], full_stop_characters = ["."]):
    in_quotes = [False for _ in range(len(quotations))]
    #in_quotes = False
    result = []
    open_quotations = [x[0] for x in quotations]
    close_quotations = [x[1] for x in quotations]
    #print(open_quotations)

    #open_quotations = ["\"", "“"]
    #close_quotations = ["\"", "”"]

    """
    Break Logic
    -----------
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
    """

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
                        elif text[pos+3].isupper() and is_name(text, pos+3, capitalized):
                            pos += 1
                        elif text[pos+3].isupper() and not is_name(text, pos+3, capitalized):
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
    with open(filename, "r") as file:
        data = file.read()
    abbr = [ "Mr.", "mr.", "MR.", "Mrs.", "MRS.", "mrs.", "MRs.", "M.", "Dr.", "DR.", "dr.", "Q." "R." ]
    cap = [ "Mr", "Mrs", "Ramsey", "Lily", "Briscoe", "James", "Paul", "Rayley", "Minta", "Doyle", "Charles",
        "Tansley", "William", "Bankes", "Augustus", "Carmichael", "Andrew", "Jasper", "Roger", "Prue", "Nancy", "Cam",
        "McNab", "Macalister", "Scott" ] 
    result = split_text(data, abbreviations=abbr, capitalized=cap)
    with open(output, "w") as file:
        for sentence in result:
            file.write(sentence + '\n')

def main():
    #filename = input("Enter filename to split:")
    #output = input("Enter output file:")
    filename = "ttl_one_line.txt"
    output = "test.txt"
    tokenize(filename, output)

if __name__ == "__main__":
    main()
