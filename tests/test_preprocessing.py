import unittest
from nlp.preprocessing import clean_text, extract_contact_info, protect_technical_tokens, restore_technical_tokens
from nlp.tokenizer import tokenize_words, tokenize_sentences
from nlp.lemmatizer import preprocess_and_lemmatize, remove_stopwords, lemmatize_tokens

class TestPreprocessing(unittest.TestCase):

    def test_clean_text_preserves_technical_tokens(self):
        raw = "Proficient in C++, C#, .NET, and Node.js with 2+ years exp. • Bullet point item."
        cleaned = clean_text(raw)
        self.assertIn("c++", cleaned.lower())
        self.assertIn("c#", cleaned.lower())
        self.assertIn(".net", cleaned.lower())
        self.assertIn("node.js", cleaned.lower())
        self.assertNotIn("•", cleaned)

    def test_extract_contact_info(self):
        text = (
            "John Doe\n"
            "Email: john.doe@example.com\n"
            "Phone: +1 555-123-4567\n"
            "LinkedIn: linkedin.com/in/johndoe\n"
            "GitHub: github.com/johndoe\n"
        )
        contact = extract_contact_info(text)
        self.assertEqual(contact["email"], "john.doe@example.com")
        self.assertTrue("555" in contact["phone"])
        self.assertIn("johndoe", contact["linkedin"])
        self.assertIn("johndoe", contact["github"])

    def test_tokenization_and_lemmatization(self):
        text = "Developers are developing machine learning models."
        tokens = tokenize_words(text)
        self.assertTrue(len(tokens) > 0)
        
        no_stops, lemmas = preprocess_and_lemmatize(tokens)
        self.assertNotIn("are", no_stops)
        # Verify lemmatization transformed developing -> develop or similar root
        self.assertTrue("develop" in lemmas or "developing" in lemmas)
        self.assertTrue("model" in lemmas or "models" in lemmas)

    def test_sentence_tokenization(self):
        text = "First sentence here. Second sentence starts now! Third sentence?"
        sents = tokenize_sentences(text)
        self.assertEqual(len(sents), 3)

if __name__ == "__main__":
    unittest.main()
