import sys
import os
import csv

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

sys.path.append(src_dir)
sys.path.append(project_root)

from prompt_handler import handle_prompt

# Test questions
test_questions = [
    "How do I resolve an heirs' property dispute in Arizona?",
    "How do I resolve an heirs' property dispute in Delaware?",
    "How do I resolve an heirs' property dispute in Wisconsin?",
    "How do I resolve an heirs' property dispute in Peru?",
    "How do I resolve an heirs' property dispute in Florida?",
    "What should I do if I inherited property with my siblings but there's no will?",
    "Where can I find legal aid for property issues in Mississippi?",
    "What resources exist in North Carolina to prevent forced partition sales?",
    "Are there laws in Louisiana to protect against predatory land sales?"
]

# Results to export
records = []

# Run test
for q in test_questions:
    print(f"\n🟦 Question: {q}")
    try:
        result = handle_prompt(q)
        answer = result["answer"]
        curated_link = result.get("curated_link", "")
        sources = ", ".join(result.get("source_info", []))

        print(f"\n🧠 Answer:\n{answer}\n")
        print(f"🔗 Link: {curated_link}")
        print(f"📄 Sources: {sources}")

        # Flags
        issues = []
        if len(answer.strip()) < 100:
            issues.append("Too short")
        if not curated_link:
            issues.append("No curated link")

        records.append({
            "question": q,
            "answer": answer,
            "curated_link": curated_link,
            "sources": sources,
            "issues": "; ".join(issues) if issues else "None"
        })

    except Exception as e:
        print(f"❌ Error processing question: {e}")
        records.append({
            "question": q,
            "answer": "",
            "curated_link": "",
            "sources": "",
            "issues": f"Error: {e}"
        })

# Export to CSV
output_path = os.path.join(project_root, "test_outputs.csv")
with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["question", "answer", "curated_link", "sources", "issues"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"\n✅ All results saved to: {output_path}")