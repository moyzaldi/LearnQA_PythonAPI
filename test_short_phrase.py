class TestShortPhrase:

    def test_short_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) <= 15,  f"The length of the phrase is {len(phrase)} , which is more than 15 characters"





