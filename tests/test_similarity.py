import unittest
from nlp.similarity import calculate_tfidf_cosine_similarity

class TestSimilarity(unittest.TestCase):

    def test_identical_texts_high_similarity(self):
        text = "Machine learning engineer with Python and TensorFlow experience."
        result = calculate_tfidf_cosine_similarity(text, text)
        self.assertAlmostEqual(result["similarity_score"], 1.0, places=2)
        self.assertGreaterEqual(result["similarity_percentage"], 99.0)

    def test_unrelated_texts_low_similarity(self):
        text1 = "Python developer building machine learning models with PyTorch."
        text2 = "Professional chef specializing in Italian pasta and culinary arts."
        result = calculate_tfidf_cosine_similarity(text1, text2)
        self.assertLess(result["similarity_score"], 0.2)

    def test_related_vs_unrelated_ordering(self):
        resume = "Python machine learning engineer building natural language processing models."
        job_ml = "Hiring machine learning engineer with Python NLP background."
        job_cook = "Hiring master pastry chef for bakery operations."
        
        sim_ml = calculate_tfidf_cosine_similarity(resume, job_ml)["similarity_score"]
        sim_cook = calculate_tfidf_cosine_similarity(resume, job_cook)["similarity_score"]
        
        self.assertGreater(sim_ml, sim_cook)

if __name__ == "__main__":
    unittest.main()
