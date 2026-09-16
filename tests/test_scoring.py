import unittest
from scoring.match_score import compute_overall_match, get_match_category
from scoring.recommendations import generate_recommendations

class TestScoring(unittest.TestCase):

    def test_overall_match_formula(self):
        resume_skills = ["Python", "Machine Learning", "SQL", "Pandas"]
        job_skills = ["Python", "Machine Learning", "SQL", "Docker", "AWS"]
        
        # 3 out of 5 skills match -> 60% skill match
        tfidf_score = 70.0
        candidate_edu = ["B.Tech Computer Science"]
        job_edu = {"degree_levels": ["Bachelor's Degree"], "text": "Bachelor's Degree in Computer Science"}
        candidate_years = 2
        job_exp = {"min_years": 2, "max_years": 4, "text": "2+ years"}
        
        result = compute_overall_match(
            resume_skills=resume_skills,
            job_skills=job_skills,
            tfidf_similarity_percentage=tfidf_score,
            candidate_education=candidate_edu,
            job_education=job_edu,
            candidate_years=candidate_years,
            job_experience=job_exp
        )

        self.assertEqual(result["skills_analysis"]["matching_skills"], ["Machine Learning", "Python", "SQL"])
        self.assertEqual(result["skills_analysis"]["missing_skills"], ["AWS", "Docker"])
        
        # Expected:
        # TF-IDF = 70 * 0.50 = 35.0
        # Skill = 60 * 0.40 = 24.0
        # Req = 100 * 0.10 = 10.0
        # Total = 69.0
        self.assertAlmostEqual(result["overall_score"], 69.0, places=1)
        self.assertEqual(result["category"], "Moderate Match")

    def test_recommendations_reflect_missing_skills(self):
        match_result = {
            "overall_score": 69.0,
            "score_breakdown": {"tfidf_similarity": 70.0},
            "skills_analysis": {
                "matching_skills": ["Python"],
                "missing_skills": ["Docker", "AWS", "PyTorch"]
            },
            "experience_match": {"score": 100}
        }
        recs = generate_recommendations(match_result, "ML Engineer")
        rec_skills = [r["skill"] for r in recs if "skill" in r]
        self.assertIn("Docker", rec_skills)
        self.assertIn("AWS", rec_skills)

    def test_category_thresholds(self):
        label, color = get_match_category(95)
        self.assertEqual(label, "Excellent Match")
        label, color = get_match_category(80)
        self.assertEqual(label, "Strong Match")
        label, color = get_match_category(65)
        self.assertEqual(label, "Moderate Match")
        label, color = get_match_category(45)
        self.assertEqual(label, "Weak Match")
        label, color = get_match_category(20)
        self.assertEqual(label, "Poor Match")

if __name__ == "__main__":
    unittest.main()
