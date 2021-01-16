from split_text import split_text, match_abbreviation, is_capitalized



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
