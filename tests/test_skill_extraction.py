import unittest
from nlp.skill_extractor import extract_skills

class TestSkillExtraction(unittest.TestCase):

    def test_canonical_skills_extraction(self):
        text = "Experience with Python, SQL, Docker, and TensorFlow."
        skills, categorized, details = extract_skills(text)
        self.assertIn("Python", skills)
        self.assertIn("SQL", skills)
        self.assertIn("Docker", skills)
        self.assertIn("TensorFlow", skills)

    def test_alias_normalization(self):
        # 'ml' should map to 'Machine Learning', 'sklearn' to 'Scikit-learn', 'postgres' to 'PostgreSQL'
        text = "Strong background in ML and deep learning using sklearn and postgres."
        skills, categorized, details = extract_skills(text)
        self.assertIn("Machine Learning", skills)
        self.assertIn("Deep Learning", skills)
        self.assertIn("Scikit-learn", skills)
        self.assertIn("PostgreSQL", skills)

    def test_no_false_positive_single_letters(self):
        # Word 'Company' or 'Core' should not trigger C programming language
        text = "Working at Company ABC doing Quality assurance."
        skills, categorized, details = extract_skills(text)
        self.assertNotIn("C", skills)

    def test_punctuated_skills(self):
        text = "Proficient in C++ and .NET architecture."
        skills, categorized, details = extract_skills(text)
        self.assertIn("C++", skills)
        self.assertIn(".NET", skills)

if __name__ == "__main__":
    unittest.main()
