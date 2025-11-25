import pdfplumber
import pandas as pd

pdf_path = "LTSAE-Checklist_COMPLIANT_30MCorrection_508.pdf"

data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        if "Your baby at" in text or "Your child at" in text:
            age_line = [line for line in text.split("\n") if "Your baby at" in line or "Your child at" in line][0]
            age = age_line.replace("Your baby at ", "").replace("Your child at ", "").strip()

            categories = [
                "Social/Emotional Milestones",
                "Language/Communication Milestones",
                "Cognitive Milestones",
                "Movement/Physical Development"
            ]

            for category in categories:
                if category in text:
                    section = text.split(category, 1)[1]

                    next_category_index = len(section)
                    for next_cat in categories:
                        if next_cat in section and next_cat != category:
                            idx = section.find(next_cat)
                            if 0 < idx < next_category_index:
                                next_category_index = idx
                    section_text = section[:next_category_index]

                    # Extract checklist items (lines starting with "")
                    items = [line.strip(" ").strip() for line in section_text.split("\n") if "" in line]
                    for item in items:
                        data.append({
                            "Age": age,
                            "Category": category,
                            "Milestone": item
                        })

df = pd.DataFrame(data)

print(df.head())

df.to_csv("developmental_milestones.csv", index=False)
print("Data saved to developmental_milestones.csv")
