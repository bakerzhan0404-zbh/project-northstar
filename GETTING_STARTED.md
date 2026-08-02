# Getting Started

## 1. Create your project repository

Create a **private repository** named `project-northstar`, then extract the full contents of `Baker_Project_Northstar.zip` into the repository root. Keep the existing folder structure unchanged.

If you are starting locally:

```bash
mkdir project-northstar
cd project-northstar
git init
# Copy and extract the project package here.
git add .
git commit -m "Initialize Project Northstar"
```

Connect the folder to your private remote repository and push the initial commit using the instructions provided by your repository platform.

## 2. Understand the project package

| Location | What it contains |
|---|---|
| `WELCOME_BAKER.md` | Your engagement welcome letter and role |
| `README.md` | Project overview, requirements, and final deliverables |
| `program/` | Engagement charter, one-month playbook, consulting standards, and evaluation rubric |
| `client/` | Client brief, stakeholder evidence, and data dictionary |
| `references/` | JPMorgan benchmarks, client cases, official links, and citation guidance |
| `data/raw/` | Source datasets; do not edit these files manually |
| `data/processed/` | Reproducible analytical outputs created by your code |
| `src/` | Data generator and starter Python analysis |
| `tests/` | Data-quality checks |
| `templates/` | Workplan, issue tree, source log, risk register, weekly update, memo, and presentation templates |
| `deliverables/working/` | Your weekly working files and submissions |
| `deliverables/final/` | Your final executive deliverables |

## 3. Run the project setup

```bash
python3 -m pip install -r requirements.txt
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 tests/test_data_quality.py
```

All data-quality checks should pass before you begin the diagnostic analysis.

## 4. Organize your weekly submissions

Create one folder for each week:

```text
deliverables/working/week_1/
deliverables/working/week_2/
deliverables/working/week_3/
deliverables/working/week_4/
```

Follow `program/ONE_MONTH_PLAYBOOK.md`. Submit one integrated assignment and one weekly update at the end of each week. Commit your work regularly with clear messages so that your analysis and decisions remain traceable.

