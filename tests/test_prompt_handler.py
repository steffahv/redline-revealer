import sys
import os
import csv
import unittest

# Setup paths
current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(src_dir)
sys.path.append(project_root)

from prompt_handler import handle_prompt  # noqa: E402


class TestPromptHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_questions = [
            "How do I resolve an heirs' property dispute in Arizona?",
            "How do I resolve an heirs' property dispute in Delaware?",
            "How do I resolve an heirs' property dispute in Wisconsin?",
            "How do I resolve an heirs' property dispute in Peru?",
            "How do I resolve an heirs' property dispute in Florida?",
            "What should I do if I inherited property but there's no will?",
            "Where can I find legal aid for property issues in Mississippi?",
            "What resources exist in North Carolina to prevent forced "
            "partition sales?",
            "Are there laws in Louisiana to protect against "
            "predatory land sales?"
        ]
        cls.records = []

    def test_questions_responses(self):
        for question in self.test_questions:
            with self.subTest(question=question):
                try:
                    result = handle_prompt(question)
                    answer = result["answer"]
                    curated_link = result.get("curated_link", "")
                    sources = ", ".join(result.get("source_info", []))

                    issues = []
                    if len(answer.strip()) < 100:
                        issues.append("Too short")
                    if not curated_link:
                        issues.append("No curated link")

                    self.records.append({
                        "question": question,
                        "answer": answer,
                        "curated_link": curated_link,
                        "sources": sources,
                        "issues": "; ".join(issues) if issues else "None"
                    })

                    self.assertIsInstance(answer, str)
                    self.assertGreater(len(answer.strip()), 40)

                except Exception as e:
                    self.records.append({
                        "question": question,
                        "answer": "",
                        "curated_link": "",
                        "sources": "",
                        "issues": f"Error: {e}"
                    })
                    self.fail(f"Error processing question: {e}")

    @classmethod
    def tearDownClass(cls):
        path = os.path.join(project_root, "test_outputs.csv")
        with open(path, "w", newline='', encoding='utf-8') as f:
            fields = [
                "question", "answer", "curated_link",
                "sources", "issues"
            ]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(cls.records)

        print(f"\n✅ Test results saved to: {path}")


if __name__ == "__main__":
    unittest.main()
