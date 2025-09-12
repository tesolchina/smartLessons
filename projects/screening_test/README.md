# Screening Test Project Structure

## Folder Organization
```
screening_test/
├── README.md                    # This file
├── screening_test_project.md    # Main project document (synced from Google Drive)
├── my_updates.md               # Personal notes and updates
├── modules/                    # Individual module development
├── test_questions/             # Question bank and materials
├── ui_testing/                 # UI testing feedback and bugs
└── meeting_notes/              # Meeting minutes and discussions
```

## Project Overview
This folder contains all materials related to the screening test development project.

### Five Core Modules
1. **Testing UI for students** - Student-facing interface testing
2. **Invigilation (and test admin)** - Admin tools for test supervision  
3. **Test questions writing** - Content creation (Word documents)
4. **Test questions set up** - Platform integration (Word → Markdown)
5. **Student answer export and grading** - Assessment tools

### Key Timeline
- **July 15**: Finalized test questions due
- **July 18**: First platform upload
- **July 25**: Student piloting complete
- **August 8**: Final version ready

### My Role
- **Assigned dates**: 20250136-20250140
- **Meeting**: Thursdays 10:30 am
- **Focus**: To be determined based on module assignment

## Quick Actions
- Run `python3 ../gdrive_sync.py` to sync latest documents
- Check `my_updates.md` for personal action items
- Review `screening_test_project.md` for full project details

---
*Created: September 6, 2025*

<!-- AUTO_PROJECT_INDEX:START -->
Auto-generated index for project `screening_test` at 2025-09-12T07:04:39Z UTC.
<!-- DAILYASSISTANT_TOOLS_PATH=../tools -->
Regenerate with: `python tools/cli/generate_project_indexes.py --dirs screening_test`

## Tool Access
- Tools directory (relative): `../tools` (packaged import: `import dailyassistant` after editable install)
- Tools directory (absolute at generation time): `/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools`
- Root quick start: see `../README.md` and `../QUICK_START_GUIDE.md`
- CLI (if installed): run `da --help` or regenerate indexes with `da index projects` (future)
- Environment variable (optional): `export DAILYASSISTANT_ROOT=`git rev-parse --show-toplevel``

### Install & Use
1. Editable install (recommended while developing):
   ````bash
   pip install -e /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant
   ````
2. Run a tool script directly (without install):
   ````bash
   python /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/cli/generate_tool_indexes.py
   ````
3. Via package module after install:
   ````bash
   python -m dailyassistant.cli.generate_tool_indexes
   ````
4. Via CLI (if entry point installed):
   ````bash
   da tool-index
   ````
5. Ad-hoc PYTHONPATH (no install):
   ````bash
   PYTHONPATH=/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant python /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/cli/generate_project_indexes.py --dirs screening_test
   ````

### Programmatic Path Detection
- Programmatic path detection snippet:

```python
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent  # contains 'tools' and 'projects'
TOOLS_DIR = REPO_ROOT / 'tools'
```

| File | Type | Size (bytes) |
|------|------|-------------|
| `MERGE_NOTE_SCREENING_DIR.md` | .md | 91 |
| `PY_SCRIPTS_MOVED.md` | .md | 211 |
| `README.md` | .md | 9155 |
| `emails/README.md` | .md | 2766 |
| `emails/communication_002_River-Testing-Instructions.md` | .md | 1283 |
| `emails/email_001_Departmental-Meeting-Screening-Test.md` | .md | 990 |
| `legacy/screening_test_project_root_copy.md` | .md | 0 |
| `my_updates.md` | .md | 1549 |
| `screening_test_project.md` | .md | 2069 |
| `student data.md` | .md | 2149 |
| `student_codes.csv` | .csv | 3732 |
| `test_questions/0notes.md` | .md | 1128 |
| `test_questions/README.md` | .md | 886 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 am/0722_AM_TEST1_QUESTIONNAIRE.pdf` | .pdf | 2122420 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 am/1. Reading/0722_AM_TEST1_READING.pdf` | .pdf | 2952099 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 am/2. Listening/0722_AM_TEST1_LISTENING.pdf` | .pdf | 2919697 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 am/3. Writing/0722_AM_TEST1_WRITING.pdf` | .pdf | 3732141 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 pm/0722_PM_TEST1_QUESTIONNAIRE.pdf` | .pdf | 1204340 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 pm/1. Reading/0722_PM_TEST1_READING.pdf` | .pdf | 1667954 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 pm/2. Listening/0722_PM_TEST1_LISTENING.pdf` | .pdf | 1742153 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0722 pm/3. Writing/0722_PM_TEST1_WRITING.pdf` | .pdf | 3463206 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 am/0723_AM_TEST1_QUESTIONNAIRE.pdf` | .pdf | 3193284 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 am/1. Reading/0723_AM_TEST1_READING.pdf` | .pdf | 4290519 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 am/2. Listening/0723_AM_TEST1_LISTENING.pdf` | .pdf | 4192832 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 am/3. Writing/0723_AM_TEST1_WRITING.pdf` | .pdf | 8928581 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 am/4. Speaking/0723_AM_TEST1_SPEAKING.pdf` | .pdf | 2450410 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 pm/0723_PM_TEST1_QUESTIONNAIRE.pdf` | .pdf | 1758398 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 pm/1. Reading/0723_PM_TEST1_READING.pdf` | .pdf | 2290710 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 pm/2. Listening/0723_PM_TEST1_LISTENING.pdf` | .pdf | 2260706 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 pm/3. Writing/0723_PM_TEST1_WRITING.pdf` | .pdf | 4563670 |
| `test_questions/real_test_set_1/Test 1-from Rhett/Trial Test Results/0723 pm/4. Speaking/0723_PM_TEST1_SPEAKING.pdf` | .pdf | 1409964 |
| `test_questions/real_test_set_1/Test 1-from Rhett/test1-new.md` | .md | 17204 |
| `test_questions/real_test_set_1/Test_1_Analysis.md` | .md | 2605 |
| `test_questions/real_test_set_1/paper_exam0801.md` | .md | 17829 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 am/0722_AM_TEST2_QUESTIONNAIRE.pdf` | .pdf | 2125898 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 am/1. Reading/0722_AM_TEST2_READING.pdf` | .pdf | 3170174 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 am/2. Listening/0722_AM_TEST2_LISTENING.pdf` | .pdf | 3025689 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 am/3. Writing/0722_AM_TEST2_WRITING.pdf` | .pdf | 4510927 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 pm/0722_PM_TEST2_QUESTIONNAIRE.pdf` | .pdf | 1256758 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 pm/1. Reading/0722_PM_TEST2_READING.pdf` | .pdf | 1810455 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 pm/2. Listening/0722_PM_TEST2_LISTENING.pdf` | .pdf | 1819591 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0722 pm/3. Writing/0722_PM_TEST2_WRITING.pdf` | .pdf | 3264902 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 am/0723_AM_TEST2_QUESTIONNAIRE.pdf` | .pdf | 3155197 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 am/1. Reading/0723_AM_TEST2_READING.pdf` | .pdf | 4623579 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 am/2. Listening/0723_AM_TEST2_LISTENING.pdf` | .pdf | 4298341 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 am/3. Writing/0723_AM_TEST2_WRITING.pdf` | .pdf | 9501585 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 am/4. Speaking/0723_AM_TEST2_SPEAKING.pdf` | .pdf | 2450789 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 pm/0723_PM_TEST2_QUESTIONNAIRE.pdf` | .pdf | 1817530 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 pm/1. Reading/0723_PM_TEST2_READING.pdf` | .pdf | 2447596 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 pm/2. Listening/0723_PM_TEST2_LISTENING.pdf` | .pdf | 2328419 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 pm/3. Writing/0723_PM_TEST2_WRITING.pdf` | .pdf | 4924804 |
| `test_questions/real_test_set_2/Test 2/Trial Test Results/0723 pm/4. Speaking/0723_PM_TEST2_SPEAKING.pdf` | .pdf | 1392122 |
| `test_questions/real_test_set_2/paper_exam0802.md` | .md | 17522 |
| `ui_testing/account_testing_log.md` | .md | 3058 |
| `ui_testing/bug_reports.md` | .md | 2690 |
| `ui_testing/comments_on_writing_test_content.md` | .md | 1241 |
| `ui_testing/email_summary.md` | .md | 467 |
| `ui_testing/mail_app_email_summary.md` | .md | 564 |
| `ui_testing/platform_access_credentials.md` | .md | 2463 |
| `ui_testing/quick_mail_search.md` | .md | 12381 |
| `ui_testing/river_testing_plan.md` | .md | 1643 |
| `ui_testing/testing_plan.md` | .md | 2471 |
| `ui_testing/testing_session_20250906.md` | .md | 1609 |
| `ui_testing/writing_section_review.html` | .html | 6816 |
| `ui_testing/writing_section_review.md` | .md | 4575 |
| `ui_testing/writing_section_review.pdf` | .pdf | 304270 |
| `ui_testing/writing_section_review_with_images.html` | .html | 7816 |
| `ui_testing/writing_section_review_with_images.md` | .md | 5407 |
| `ui_testing/writing_section_review_with_images.pdf` | .pdf | 322403 |
| `ui_testing_templates/README.md` | .md | 1481 |
| `ui_testing_templates/test_templates/bug_report_template.md` | .md | 1172 |

<!-- AUTO_PROJECT_INDEX:END -->
