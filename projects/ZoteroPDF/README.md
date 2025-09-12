# ZoteroMDsMineru3 - Academic RAG System

A project for processing and organizing Zotero references with advanced RAG (Retrieval-Augmented Generation) capabilities and citation analysis tools.

## Features

- **Academic Search**: Query a corpus of research papers with natural language
- **Citation Review**: Analyze manuscript citations and improve citation quality
- **Interactive Interface**: Streamlit-based web interfaces for easy use
- **Export Capabilities**: Save search results and citations
- **Advanced Caching**: Multi-layer caching for improved performance
- **Pedagogical Focus**: Specialized filtering for education-related content

## Quick Start

### 1. Search Academic Papers
```bash
streamlit run app.py
```

### 2. Review Manuscript Citations
```bash
streamlit run citation_app.py
```

### 3. Command Line Citation Analysis
```bash
python scripts/citation_reviewer.py \
    --manuscript my_paper.md \
    --references faiss_index \
    --output citation_review.md
```

## System Documentation

- **[Citation Review Guide](CITATION_REVIEW_GUIDE.md)** - Complete guide for manuscript citation analysis
- **[SPRINTS.md](docs/SPRINTS.md)** - Development sprints and implementation phases
- **[PROJECT_PLAN.md](docs/PROJECT_PLAN.md)** - Comprehensive project planning

## Project Structure

```
ZoteroMDsMineru3/
├── README.md                 # This file
├── docs/                     # Documentation and notes
│   ├── 0notes.md            # Project notes
│   └── NotesfromAhmad.md    # Notes from Ahmad
├── scripts/                  # Python processing scripts
│   ├── GitUpMD5.py          # Git upload with MD5 functionality
│   └── mdMove.py            # Markdown file movement utilities
└── data/                     # Processed data
    ├── batch_001/           # First batch of processed files (~1000 files)
    └── batch_002/           # Second batch of processed files (~930 files)
```

## Overview

This repository contains processed Zotero reference files that have been converted to Markdown format. The files are organized in batches and contain academic papers, research documents, and related materials.

## Getting Started

1. Clone the repository
2. Review the documentation in the `docs/` folder
3. Use the scripts in the `scripts/` folder for processing

## Contributors

- Ahmad (ahmad-rev0) - Original repository owner
- tesolchina - Fork maintainer

## License

[Add license information here]

<!-- AUTO_PROJECT_INDEX:START -->
Auto-generated index for project `ZoteroPDF` at 2025-09-12T10:19:25Z UTC.
<!-- DAILYASSISTANT_TOOLS_PATH=../tools -->
Regenerate with: `python tools/cli/generate_project_indexes.py --dirs ZoteroPDF`

## Tool Access
- Tools directory (relative): `../tools` (packaged import: `import dailyassistant` after editable install)
- Tools directory (absolute at generation time): `/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools`
- Root quick start: see `../README.md` and `../QUICK_START_GUIDE.md`
- CLI (if installed): run `da --help` or regenerate indexes with `da index projects` (future)
- Environment variable (optional): `export DAILYASSISTANT_ROOT=`git rev-parse --show-toplevel``

### Install & Use
1. Install latest main directly from Git (no clone needed):
   ````bash
   pip install git+https://github.com/tesolchina/DailyAssistant.git
   ````
2. Install specific tag/ref:
   ````bash
   pip install git+https://github.com/tesolchina/DailyAssistant.git@<tag_or_commit>
   ````
3. Editable install after cloning (development):
   ````bash
   git clone https://github.com/tesolchina/DailyAssistant.git dailyassistant-src
   cd dailyassistant-src
   pip install -e .
   ````
4. Run a tool script directly (no install):
   ````bash
   python /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/cli/generate_tool_indexes.py
   ````
5. Via package module (after install):
   ````bash
   python -m dailyassistant.cli.generate_tool_indexes
   ````
6. Via CLI entry point (if defined in pyproject):
   ````bash
   da tool-index
   ````
7. Ad-hoc PYTHONPATH (quick test, no install):
   ````bash
   PYTHONPATH=/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant python /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/cli/generate_project_indexes.py --dirs ZoteroPDF
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
| `LitonGoalChatbot/A review of self-regulated learning Six models and four directions for research..clean.md` | .md | 59611 |
| `LitonGoalChatbot/Adapting self-regulated learning in an age of generative artificial intelligence chatbots.clean.md` | .md | 34313 |
| `LitonGoalChatbot/An exploratory study of academic goal-setting, achievement calibration and self-regulated learning.clean.md` | .md | 228 |
| `LitonGoalChatbot/Are We There Yet—A systematic literature review on chatbots in education.clean.md` | .md | 36858 |
| `LitonGoalChatbot/BATCH_REPORT.md` | .md | 15192 |
| `LitonGoalChatbot/Becoming a Self Regulated Learner An Overview.clean.md` | .md | 21120 |
| `LitonGoalChatbot/Being smart about writing SMART objectives. Evaluation and Program Planning.clean.md` | .md | 9839 |
| `LitonGoalChatbot/Beyond goal setting and planning An examination of college students’ self-regulated learning forethought processes.clean.md` | .md | 37691 |
| `LitonGoalChatbot/Chatbots for learning A review of educational chatbots for the Facebook Messenger.clean.md` | .md | 23132 |
| `LitonGoalChatbot/Comparing artificial intelligence and human coaching goal attainment efficacy.clean.md` | .md | 40708 |
| `LitonGoalChatbot/Constructing and evaluating online goal-setting mechanisms in web-based portfolio assessment system for facilitating self-regulated learning.clean.md` | .md | 29951 |
| `LitonGoalChatbot/Cultivating competence, self-efficacy, and intrinsic interest through proximal self-motivation.clean.md` | .md | 40728 |
| `LitonGoalChatbot/Developing Learner Autonomy and Goal-Setting through logbook.clean.md` | .md | 35246 |
| `LitonGoalChatbot/Eliza a computer program for the study of natural language communication between man and machine-clear.clean.md` | .md | 31914 |
| `LitonGoalChatbot/Empowering student self‐regulated learning and science education through ChatGPT  A.clean.md` | .md | 59779 |
| `LitonGoalChatbot/Engaging Students With a Chatbot-Based Academic Advising System.clean.md` | .md | 63506 |
| `LitonGoalChatbot/Examining students  self-set goals for self-regulated learning  Goal properties and patterns.clean.md` | .md | 29492 |
| `LitonGoalChatbot/From cognitive modeling to self-regulation A social cognitive career path.clean.md` | .md | 45989 |
| `LitonGoalChatbot/Goal Setting and Self-Efficacy During Self-Regulated Learning.clean.md` | .md | 32392 |
| `LitonGoalChatbot/Google doc + gaols Developing Learner Autonomy and Goal-Setting through logbook.clean.md` | .md | 35073 |
| `LitonGoalChatbot/How educational chatbots support self-regulated learning A systematic review of the literature.clean.md` | .md | 46951 |
| `LitonGoalChatbot/INDEX.md` | .md | 28522 |
| `LitonGoalChatbot/Implementation and Evaluation of a Tool for Setting Goals in Self-regulated Learning with Web Resources.clean.md` | .md | 1516911 |
| `LitonGoalChatbot/Implementing the Bashayer chatbot in Saudi higher education measuring the influence on students' motivation and learning strategies.clean.md` | .md | 52114 |
| `LitonGoalChatbot/Interacting with educational chatbots A systematic review.clean.md` | .md | 75833 |
| `LitonGoalChatbot/LLM based chatbot+ goals 重要Towards a large-language-model-based chatbot system to automatically.clean.md` | .md | 45986 |
| `LitonGoalChatbot/New developments in and directions for goal-setting research..clean.md` | .md | 35885 |
| `LitonGoalChatbot/One size fits all What counts as quality practice in (reflexive) thematic analysis.clean.md` | .md | 43333 |
| `LitonGoalChatbot/Perceived usefulness, perceived ease of use, and user acceptance of information technology.clean.md` | .md | 74092 |
| `LitonGoalChatbot/Rule-based chabot for student enquiries.clean.md` | .md | 20346 |
| `LitonGoalChatbot/SMART goals pattern-Examining students  self-set goals for self-regulated learning  Goal properties and patterns.clean.md` | .md | 31545 |
| `LitonGoalChatbot/Self-regulated learning of a motoric skill  The role of goal setting and self-monitoring.clean.md` | .md | 28494 |
| `LitonGoalChatbot/Self-regulated learning strategies predict learner behavior and goal attainment in Massive Open Online Courses.clean.md` | .md | 47545 |
| `LitonGoalChatbot/Service chatbots A systematic review.clean.md` | .md | 60346 |
| `LitonGoalChatbot/Studying as self-regulated engagement in learning in metacognition in educational theory and practice.clean.md` | .md | 48667 |
| `LitonGoalChatbot/Supporting students goal setting process using chatbot implementation in a fully online course.clean.md` | .md | 25845 |
| `LitonGoalChatbot/Technology‑based interactive guidance to promote learning performance and self-regulation a chatbot-assisted self-regulated learning approach.clean.md` | .md | 48637 |
| `LitonGoalChatbot/The effect of distal learning  outcome  and proximal goals on a moderately complex task.clean.md` | .md | 15859 |
| `LitonGoalChatbot/The impact of educatinoal chatbot on student learning experience.clean.md` | .md | 35605 |
| `LitonGoalChatbot/There’s a S.M.A.R.T. way to write management’s goals and objectives.clean.md` | .md | 0 |
| `LitonGoalChatbot/Understanding EFL students’ use of self-made AI chatbots as personalized writing assistance tools_ A mixed methods study.clean.md` | .md | 49228 |
| `LitonGoalChatbot/Using Chatbots in Flipped Learning Online Sessions Perceived Usefulness and Ease of Use.clean.md` | .md | 629746 |
| `LitonGoalChatbot/Using chatbots to support student goal setting and social presence in fully online activities learner engagement and perceptions.clean.md` | .md | 50673 |
| `LitonGoalChatbot/Using thematic analysis in psychology.clean.md` | .md | 49809 |
| `LitonGoalChatbot/chatbot+Using chatbots to support student goal setting and social presence in fully online activities learner engagement and perceptions.clean.md` | .md | 50416 |
| `LitonGoalChatbot/chatbot+goals Supporting students goal setting process using chatbot implementation in a fully online course.clean.md` | .md | 25873 |
| `LitonGoalChatbot/human coach + goals Comparing artificial intelligence and human coaching goal attainment efficacy.clean.md` | .md | 42340 |
| `LitonGoalChatbot/the role of goal orientation in self-regulated learning.clean.md` | .md | 92340 |
| `LitonGoalChatbot/港大作者的新文章 重要Towards a large-language-model-based chatbot system to automatically.clean.md` | .md | 44735 |
| `README.md` | .md | 1338 |
| `annotated_data/LitonGoalChatbot/A review of self-regulated learning Six models and four directions for research..clean.md` | .md | 60364 |
| `annotated_data/LitonGoalChatbot/Adapting self-regulated learning in an age of generative artificial intelligence chatbots.clean.md` | .md | 34458 |
| `annotated_data/LitonGoalChatbot/An exploratory study of academic goal-setting, achievement calibration and self-regulated learning.clean.md` | .md | 840 |
| `annotated_data/LitonGoalChatbot/Are We There Yet—A systematic literature review on chatbots in education.clean.md` | .md | 37876 |
| `annotated_data/LitonGoalChatbot/BATCH_REPORT.md` | .md | 15588 |
| `annotated_data/LitonGoalChatbot/Becoming a Self Regulated Learner An Overview.clean.md` | .md | 21620 |
| `annotated_data/LitonGoalChatbot/Being smart about writing SMART objectives. Evaluation and Program Planning.clean.md` | .md | 10546 |
| `annotated_data/LitonGoalChatbot/Beyond goal setting and planning An examination of college students’ self-regulated learning forethought processes.clean.md` | .md | 38667 |
| `annotated_data/LitonGoalChatbot/Chatbots for learning A review of educational chatbots for the Facebook Messenger.clean.md` | .md | 23965 |
| `annotated_data/LitonGoalChatbot/Comparing artificial intelligence and human coaching goal attainment efficacy.clean.md` | .md | 41376 |
| `annotated_data/LitonGoalChatbot/Constructing and evaluating online goal-setting mechanisms in web-based portfolio assessment system for facilitating self-regulated learning.clean.md` | .md | 31135 |
| `annotated_data/LitonGoalChatbot/Cultivating competence, self-efficacy, and intrinsic interest through proximal self-motivation.clean.md` | .md | 41977 |
| `annotated_data/LitonGoalChatbot/Developing Learner Autonomy and Goal-Setting through logbook.clean.md` | .md | 35996 |
| `annotated_data/LitonGoalChatbot/Eliza a computer program for the study of natural language communication between man and machine-clear.clean.md` | .md | 32072 |
| `annotated_data/LitonGoalChatbot/Empowering student self‐regulated learning and science education through ChatGPT  A.clean.md` | .md | 60780 |
| `annotated_data/LitonGoalChatbot/Engaging Students With a Chatbot-Based Academic Advising System.clean.md` | .md | 64125 |
| `annotated_data/LitonGoalChatbot/Examining students  self-set goals for self-regulated learning  Goal properties and patterns.clean.md` | .md | 30413 |
| `annotated_data/LitonGoalChatbot/From cognitive modeling to self-regulation A social cognitive career path.clean.md` | .md | 46859 |
| `annotated_data/LitonGoalChatbot/Goal Setting and Self-Efficacy During Self-Regulated Learning.clean.md` | .md | 32878 |
| `annotated_data/LitonGoalChatbot/Google doc + gaols Developing Learner Autonomy and Goal-Setting through logbook.clean.md` | .md | 35844 |
| `annotated_data/LitonGoalChatbot/How educational chatbots support self-regulated learning A systematic review of the literature.clean.md` | .md | 48361 |
| `annotated_data/LitonGoalChatbot/INDEX.md` | .md | 28574 |
| `annotated_data/LitonGoalChatbot/Implementation and Evaluation of a Tool for Setting Goals in Self-regulated Learning with Web Resources.clean.md` | .md | 1517500 |
| `annotated_data/LitonGoalChatbot/Implementing the Bashayer chatbot in Saudi higher education measuring the influence on students' motivation and learning strategies.clean.md` | .md | 53225 |
| `annotated_data/LitonGoalChatbot/Interacting with educational chatbots A systematic review.clean.md` | .md | 77085 |
| `annotated_data/LitonGoalChatbot/LLM based chatbot+ goals 重要Towards a large-language-model-based chatbot system to automatically.clean.md` | .md | 47137 |
| `annotated_data/LitonGoalChatbot/New developments in and directions for goal-setting research..clean.md` | .md | 36386 |
| `annotated_data/LitonGoalChatbot/One size fits all What counts as quality practice in (reflexive) thematic analysis.clean.md` | .md | 43906 |
| `annotated_data/LitonGoalChatbot/Perceived usefulness, perceived ease of use, and user acceptance of information technology.clean.md` | .md | 74941 |
| `annotated_data/LitonGoalChatbot/Rule-based chabot for student enquiries.clean.md` | .md | 20439 |
| `annotated_data/LitonGoalChatbot/SMART goals pattern-Examining students  self-set goals for self-regulated learning  Goal properties and patterns.clean.md` | .md | 32486 |
| `annotated_data/LitonGoalChatbot/Self-regulated learning of a motoric skill  The role of goal setting and self-monitoring.clean.md` | .md | 29489 |
| `annotated_data/LitonGoalChatbot/Self-regulated learning strategies predict learner behavior and goal attainment in Massive Open Online Courses.clean.md` | .md | 48554 |
| `annotated_data/LitonGoalChatbot/Service chatbots A systematic review.clean.md` | .md | 60863 |
| `annotated_data/LitonGoalChatbot/Studying as self-regulated engagement in learning in metacognition in educational theory and practice.clean.md` | .md | 49215 |
| `annotated_data/LitonGoalChatbot/Supporting students goal setting process using chatbot implementation in a fully online course.clean.md` | .md | 26439 |
| `annotated_data/LitonGoalChatbot/Technology‑based interactive guidance to promote learning performance and self-regulation a chatbot-assisted self-regulated learning approach.clean.md` | .md | 49782 |
| `annotated_data/LitonGoalChatbot/The effect of distal learning  outcome  and proximal goals on a moderately complex task.clean.md` | .md | 16623 |
| `annotated_data/LitonGoalChatbot/The impact of educatinoal chatbot on student learning experience.clean.md` | .md | 36534 |
| `annotated_data/LitonGoalChatbot/There’s a S.M.A.R.T. way to write management’s goals and objectives.clean.md` | .md | 123 |
| `annotated_data/LitonGoalChatbot/Understanding EFL students’ use of self-made AI chatbots as personalized writing assistance tools_ A mixed methods study.clean.md` | .md | 50238 |
| `annotated_data/LitonGoalChatbot/Using Chatbots in Flipped Learning Online Sessions Perceived Usefulness and Ease of Use.clean.md` | .md | 630387 |
| `annotated_data/LitonGoalChatbot/Using chatbots to support student goal setting and social presence in fully online activities learner engagement and perceptions.clean.md` | .md | 51455 |
| `annotated_data/LitonGoalChatbot/Using thematic analysis in psychology.clean.md` | .md | 49900 |
| `annotated_data/LitonGoalChatbot/chatbot+Using chatbots to support student goal setting and social presence in fully online activities learner engagement and perceptions.clean.md` | .md | 51110 |
| `annotated_data/LitonGoalChatbot/chatbot+goals Supporting students goal setting process using chatbot implementation in a fully online course.clean.md` | .md | 26481 |
| `annotated_data/LitonGoalChatbot/human coach + goals Comparing artificial intelligence and human coaching goal attainment efficacy.clean.md` | .md | 43028 |
| `annotated_data/LitonGoalChatbot/the role of goal orientation in self-regulated learning.clean.md` | .md | 92449 |
| `annotated_data/LitonGoalChatbot/港大作者的新文章 重要Towards a large-language-model-based chatbot system to automatically.clean.md` | .md | 45690 |
| `annotated_data/batch_001/out_22MV5CS2_The_influences_of_international.md` | .md | 68156 |
| `annotated_data/batch_001/out_24AE7ZXZ_2020_HKDSE_ENG_P2.md` | .md | 17484 |
| `annotated_data/batch_001/out_24GENQEM_Aish_and_Tomlinson_-_2022_-_Usi.md` | .md | 33007 |
| `annotated_data/batch_001/out_24II5VXW_2023_-_How_do_we_respond_to_gen.md` | .md | 83329 |
| `annotated_data/batch_001/out_24L685MS_A-comparative-genre-analysis-of.md` | .md | 79109 |
| `annotated_data/batch_001/out_24SRJ2J5_Abdi_Tabari_et_al_-_2024_-_Unde.md` | .md | 86267 |
| `annotated_data/batch_001/out_25TGBA6H_Matzler_-_2021_-_Grant_proposal.md` | .md | 70070 |
| `annotated_data/batch_001/out_26J482KX_Hyland_-_2018_-_Genre_and_Secon.md` | .md | 16042 |
| `annotated_data/batch_001/out_26MCVWEZ_Johnson_and_Tweedie_-_2024_-_In.md` | .md | 11821 |
| `annotated_data/batch_001/out_26SR4BLE_English-writing-instructors--us.md` | .md | 67725 |
| `annotated_data/batch_001/out_27374BFX_Li_et_al_-_2024_-_Expert_or_mac.md` | .md | 69731 |
| `annotated_data/batch_001/out_28N5IYVH_Cheng_-_2021_-_Book_review.md` | .md | 10027 |
| `annotated_data/batch_001/out_28T73IMR_Catenaccio_-_2022_-_Press_relea.md` | .md | 65820 |
| `annotated_data/batch_001/out_292E498S_Huang_-_2024_-_Book_review.md` | .md | 10714 |
| `annotated_data/batch_001/out_296L7Y8R_Yu_-_2022_-_A_multi-dimensional.md` | .md | 66805 |
| `annotated_data/batch_001/out_29CA2DXP_Macnamara_-_2014_-_Journalism–P.md` | .md | 71068 |
| `annotated_data/batch_001/out_2D568XQ3_Master_-_2005_-_Research_in_Eng.md` | .md | 65319 |
| `annotated_data/batch_001/out_2DQI3EWC_Chan_-_2019_-_Four_decades_of_E.md` | .md | 67889 |
| `annotated_data/batch_001/out_2DYGMUJF_Topping_-_2015_-_Peer_tutoring.md` | .md | 92779 |
| `annotated_data/batch_001/out_2EVEAMNB_Ekin_-_2023_-_Prompt_Engineerin.md` | .md | 38658 |
| `annotated_data/batch_001/out_2FESQ4UY_Thompson_and_Sinclair_-_1995_-.md` | .md | 2187 |
| `annotated_data/batch_001/out_2FJZKLGY_Ma_et_al_-_2024_-_Teacher_paths.md` | .md | 85852 |
| `annotated_data/batch_001/out_2FUU2UEF_Tong_et_al_-_2024_-_Student_eng.md` | .md | 81361 |
| `annotated_data/batch_001/out_2GIMDC8C_Geng_and_Liang_-_2024_-_From_wo.md` | .md | 70711 |
| `annotated_data/batch_001/out_2GMEMMQV_OECD_-_2014_-_Supplementary_Edu.md` | .md | 70670 |
| `annotated_data/batch_001/out_2GPRWH4X_Perceptions_of_supervisors_and.md` | .md | 84188 |
| `annotated_data/batch_001/out_2GXUWDRH_Thornton_-_2020_-_“That’s_the_w.md` | .md | 577180 |
| `annotated_data/batch_001/out_2H3JVGQD_Hu_et_al_-_2024_-_Metadiscursiv.md` | .md | 76309 |
| `annotated_data/batch_001/out_2J8NQ7ZV_Hirose_-_2003_-_Comparing_L1_an.md` | .md | 84082 |
| `annotated_data/batch_001/out_2KYGWD88_Nicholas_et_al_-_2021_-_Climate.md` | .md | 45023 |
| `annotated_data/batch_001/out_2LRJIYL9_Lee_-_The_shadow_cost_of_educat.md` | .md | 84472 |
| `annotated_data/batch_001/out_2LZB5LUM_Langer_-_2007_-_The_elusive_aim.md` | .md | 75857 |
| `annotated_data/batch_001/out_2N3YCE9G_Tao_and_Rosa_Yeh_-_2008_-_Typol.md` | .md | 62422 |
| `annotated_data/batch_001/out_2NDL8DBY_Su_et_al_-_2022_-_Exemplificati.md` | .md | 68444 |
| `annotated_data/batch_001/out_2P5F5FQB_2024_-_BALEAP_news_-_Introducti.md` | .md | 16009 |
| `annotated_data/batch_001/out_2PZ7X7FT_Shi_et_al_-_2020_-_Internet-Med.md` | .md | 73579 |
| `annotated_data/batch_001/out_2Q244QWT_ChatGPT-4_as_a_journalist_Whose.md` | .md | 64667 |
| `annotated_data/batch_001/out_2QJ8EYGM_Stigmar_-_2016_-_Peer-to-peer_t.md` | .md | 41088 |
| `annotated_data/batch_001/out_2RR5QXXT_The_influence_of_AI_text_genera.md` | .md | 72857 |
| `annotated_data/batch_001/out_2RZV74W9_Fortanet_-_2008_-_Evaluative_la.md` | .md | 48766 |
| `annotated_data/batch_001/out_2S5F4VDF_Berlin_-_2005_-_Contextualizing.md` | .md | 379680 |
| `annotated_data/batch_001/out_2SQTR9MI_Shazly_-_Effects_of_artificial.md` | .md | 75770 |
| `annotated_data/batch_001/out_2SZTXH45_McCarthy_et_al_-_2022_-_Automat.md` | .md | 109819 |
| `annotated_data/batch_001/out_2UA8UUWA_Yu_-_2020_-_Investigating_L2_wr.md` | .md | 79760 |
| `annotated_data/batch_001/out_2UBKUQZK_‘You_certainly_don’t_get_promot.md` | .md | 73958 |
| `annotated_data/batch_001/out_2USQAYNA_Zhang_and_Zhang_-_2024_-_Tracki.md` | .md | 70207 |
| `annotated_data/batch_001/out_2UVZG7LD_Ewert_-_2009_-_L2_writing_confe.md` | .md | 83790 |
| `annotated_data/batch_001/out_2VGRCF5S_Safarov_et_al_-_2017_-_Utilizat.md` | .md | 95929 |
| `annotated_data/batch_001/out_2VPG6LQI_de_Beer_-_The_History_of_the_AL.md` | .md | 227087 |
| `annotated_data/batch_001/out_2VRB42JI_Abd_El-Raziq_et_al_-_2024_-_Lex.md` | .md | 108217 |
| `annotated_data/batch_001/out_2WJULS22_Harrison_-_2024_-_Attitudes_tow.md` | .md | 56168 |
| `annotated_data/batch_001/out_2WKXVD6Y_Dumitru_et_al_-_2023_-_Garbage.md` | .md | 45938 |
| `annotated_data/batch_001/out_2WN2BXQ3_San_Miguel_and_Nelson_-_2007_-.md` | .md | 57655 |
| `annotated_data/batch_001/out_2Y8L9LPF_Heyns_-_2022_-_BALEAP_news_-_In.md` | .md | 5556 |
| `annotated_data/batch_001/out_2YJJ6XCM_Huang_-_2024_-_Unveiling_EFL_gr.md` | .md | 56701 |
| `annotated_data/batch_001/out_2YNUAUBQ_Lohan_and_Dafouz_-_2024_-_A_sit.md` | .md | 62117 |
| `annotated_data/batch_001/out_2Z5TRKGC_Citation-practices-in-applied-l.md` | .md | 81360 |
| `annotated_data/batch_001/out_2ZACMHGG_sahin2015.md` | .md | 35182 |
| `annotated_data/batch_001/out_2ZAXESPL_Williams_-_2004_-_Tutoring_and.md` | .md | 89383 |
| `annotated_data/batch_001/out_2ZXFJ4JE_Bychkovska_-_2021_-_Effects_of.md` | .md | 93158 |
| `annotated_data/batch_001/out_32CLLFWE_Golparvar_et_al_-_2024_-_Mappin.md` | .md | 69920 |
| `annotated_data/batch_001/out_32EYVZ8Q_Koltovskaia_et_al_-_2024_-_Grad.md` | .md | 77889 |
| `annotated_data/batch_001/out_33C3T4Z6_Su_et_al_-_2024_-_Integrating_p.md` | .md | 73161 |
| `annotated_data/batch_001/out_33FC8BRH_Dykstra_et_al_-_2023_-_Reading.md` | .md | 75803 |
| `annotated_data/batch_001/out_34CN7J74_Raising_the_(meta)pragmatic_awa.md` | .md | 78096 |
| `annotated_data/batch_001/out_34M2C7IB_Chun_-_2009_-_Contesting_neolib.md` | .md | 53158 |
| `annotated_data/batch_001/out_34N9SLD8_Evaluating_AI's_impact_on_self-.md` | .md | 88405 |
| `annotated_data/batch_001/out_35PMT2NG_Lea_-_2004_-_Academic_literacie.md` | .md | 59435 |
| `annotated_data/batch_001/out_36MJ5VLM_Icy_Lee_Understanding_written_f.md` | .md | 61435 |
| `annotated_data/batch_001/out_36S3Q8G2_Evans_and_Green_-_2007_-_Why_EA.md` | .md | 57539 |
| `annotated_data/batch_001/out_36TPGBH8_Ellis_-_1994_-_The_Study_of_Sec.md` | .md | 2245378 |
| `annotated_data/batch_001/out_37VBSBQU_Stotesbury_-_2003_-_Evaluation.md` | .md | 42196 |
| `annotated_data/batch_001/out_37WWSTD7_Cavanagh_-_2020_-_The_Role_of_E.md` | .md | 59405 |
| `annotated_data/batch_001/out_384F7RGP_Schneider_et_al_-_2016_-_Can_Yo.md` | .md | 62994 |
| `annotated_data/batch_001/out_38582AIC_Baker_-_2024_-_Intercultural_co.md` | .md | 12125 |
| `annotated_data/batch_001/out_3888B4DF_Shvidko_-_2018_-_Writing_confer.md` | .md | 75657 |
| `annotated_data/batch_001/out_38LCB8GK_Zappavigna_2014_Enacting_identi.md` | .md | 54786 |
| `annotated_data/batch_001/out_38PF4ULY_Chen_et_al_-_2024_-_How_does_em.md` | .md | 75943 |
| `annotated_data/batch_001/out_38QKXMDI_Domke_-_2024_-_How_Children_Rea.md` | .md | 62703 |
| `annotated_data/batch_001/out_3AN6FGLW_Read_-_2008_-_Identifying_acade.md` | .md | 52173 |
| `annotated_data/batch_001/out_3B52RTLR_Coffin_-_2004_-_Arguing_about_h.md` | .md | 51159 |
| `annotated_data/batch_001/out_3BB89AY6_Woodward-Kron_-_2008_-_More_tha.md` | .md | 61179 |
| `annotated_data/batch_001/out_3BLDPMSU_Flowerdew_-_2009_-_Goffman’s_st.md` | .md | 16393 |
| `annotated_data/batch_001/out_3CHC88GP_Applying_the_bundle-move_connec.md` | .md | 88077 |
| `annotated_data/batch_001/out_3DFKI8QG_Marco_-_2000_-_Collocational_fr.md` | .md | 56983 |
| `annotated_data/batch_001/out_3DJN2L5M_Mur_Dueñas_-_2007_-_‘Iwe_focus.md` | .md | 64922 |
| `annotated_data/batch_001/out_3EHD27GE_Kim_-_2006_-_Academic_oral_comm.md` | .md | 35125 |
| `annotated_data/batch_001/out_3EKCQV7J_Perrotta_and_Selwyn_-_2020_-_De.md` | .md | 74652 |
| `annotated_data/batch_001/out_3ENFTKRG_Teló_et_al_-_2024_-_Accent_Bias.md` | .md | 78476 |
| `annotated_data/batch_001/out_3FPBG2JY_Mollick_and_Mollick_-_2023_-_As.md` | .md | 126764 |
| `annotated_data/batch_001/out_3G9F4FMN_Liu_et_al_-_2024_-_The_role_of.md` | .md | 64385 |
| `annotated_data/batch_001/out_3GP9RVF5_Pathak_and_Sovani-Kelkar_-_2023.md` | .md | 84142 |
| `annotated_data/batch_001/out_3HKP47G4_Petrowitz_-_2014_-_The_travelin.md` | .md | 235409 |
| `annotated_data/batch_001/out_3HVXPQWJ_Cardona_and_Rodriguez_-_Designi.md` | .md | 116107 |
| `annotated_data/batch_001/out_3IEGNKAK_Gebril_-_2024_-_Towards_a_recon.md` | .md | 9582 |
| `annotated_data/batch_001/out_3INC95XK_Adhami_and_Taghizadeh_-_2024_-.md` | .md | 109717 |
| `annotated_data/batch_001/out_3IUZHB5J_Biber_-_2006_-_Stance_in_spoken.md` | .md | 56164 |
| `annotated_data/batch_001/out_3JKLUWQN_Yang_et_al_-_2021_-_Human-cente.md` | .md | 39431 |
| `annotated_data/batch_001/out_3KHBGKYM_Editorial-Board_2024_Journal-of.md` | .md | 3286 |
| `annotated_data/batch_001/out_3KJ6U37Q_Jeon_-_2024_-_Exploring_AI_chat.md` | .md | 68010 |
| `annotated_data/batch_001/out_3NH84YX5_Jin_et_al_-_2024_-_Developing_a.md` | .md | 70293 |
| `annotated_data/batch_001/out_3NL63DC7_Artificial_Intelligence_for_Aca.md` | .md | 89238 |
| `annotated_data/batch_001/out_3P3KJSDQ_(Literacies)_Theresa_M_Lillis-S.md` | .md | 512387 |
| `annotated_data/batch_001/out_3Q2UBBDH_Zhan_and_Zhou_-_2024_-_Book_rev.md` | .md | 15635 |
| `annotated_data/batch_001/out_3QAUMTI4_Quan_et_al_-_2024_-_Comparing_c.md` | .md | 70356 |
| `annotated_data/batch_001/out_3R6LR3XI_Zhou_and_Li_-_2024_-_“In_the_pr.md` | .md | 68399 |
| `annotated_data/batch_001/out_3RFUMMI7_Fogal_-_2024_-_Expanding_the_co.md` | .md | 71712 |
| `annotated_data/batch_001/out_3RLSM5JT_Peterson_and_Muñoz_-_2022_-_“St.md` | .md | 71891 |
| `annotated_data/batch_001/out_3RMXBWMW_Crossley_et_al_-_2024_-_A_large.md` | .md | 21539 |
| `annotated_data/batch_001/out_3SEARE2J_Kong_and_Liu_-_2024_-_A_compara.md` | .md | 79109 |
| `annotated_data/batch_001/out_3TJ8NXBF_[Dana_R__Ferris]_Response_To_St.md` | .md | 564215 |
| `annotated_data/batch_001/out_3U7X3N4H_Bunton_-_2005_-_The_structure_o.md` | .md | 52813 |
| `annotated_data/batch_001/out_3UAXAARY_Nguyen_and_Vu_-_2024_-_Explorin.md` | .md | 103340 |
| `annotated_data/batch_001/out_3UEZUCWP_Querol-Julián_-_2023_-_Multimod.md` | .md | 62423 |
| `annotated_data/batch_001/out_3UIGJCEL_Mazdayasna_and_Tahririan_-_2008.md` | .md | 59841 |
| `annotated_data/batch_001/out_3V7DTF69_Yeager_et_al_-_2024_-_Notetakin.md` | .md | 64637 |
| `annotated_data/batch_001/out_3V8TTTSE_Bremner_-_2008_-_Intertextualit.md` | .md | 57297 |
| `annotated_data/batch_001/out_3VMLR6UR_Mayer_et_al_-_1995_-_An_Integra.md` | .md | 75696 |
| `annotated_data/batch_001/out_3W3BNA3I_Bashori_et_al_-_2024_-_‘Look,_I.md` | .md | 73654 |
| `annotated_data/batch_001/out_3WMPWJ5L_Liu_and_Zhang_-_2021_-_Using_Me.md` | .md | 54844 |
| `annotated_data/batch_001/out_3Y6WWY98_Marsely_-_2020_-_Peer_Tutoring.md` | .md | 51578 |
| `annotated_data/batch_001/out_3YN8DD8P_When_artificial_intelligence_su.md` | .md | 64204 |
| `annotated_data/batch_001/out_42TNE8YK_2021_-_Editorial_Board.md` | .md | 4354 |
| `annotated_data/batch_001/out_42VBJDTQ_GSCG_2017_Eng.md` | .md | 347345 |
| `annotated_data/batch_001/out_433JZQQY_Jacobsson_-_2021_-_Young_vs_old.md` | .md | 63329 |
| `annotated_data/batch_001/out_43UUF6B9_Kwan_-_2009_-_Reading_in_prepar.md` | .md | 53626 |
| `annotated_data/batch_001/out_44EQKQ5U_Yin_and_Parkinson_-_2021_-_Crit.md` | .md | 68228 |
| `annotated_data/batch_001/out_44GCMD8D_SLRF-Revised-FINAL-2013bl.md` | .md | 51505 |
| `annotated_data/batch_001/out_45DQIDC7_Garcia-Ponce_-_2020_-_Needs_Ana.md` | .md | 53112 |
| `annotated_data/batch_001/out_45GPAFH6_Language_Testing-2010-Xi-291-30.md` | .md | 31695 |
| `annotated_data/batch_001/out_45ZVM7CQ_Burk_and_Reyman_-_2014_-_Patent.md` | .md | 89128 |
| `annotated_data/batch_001/out_462GIF3S_Weng_et_al_-_2024_-_Effects_of.md` | .md | 65772 |
| `annotated_data/batch_001/out_468ZPMFQ_Panagopoulos_et_al_-_2024_-_Wri.md` | .md | 74954 |
| `annotated_data/batch_001/out_46VAM2E6_Graham_-_2024_-_Assessing_the_i.md` | .md | 48121 |
| `annotated_data/batch_001/out_47BUL4FJ_Pay_structure_for_Academic_Teac.md` | .md | 3619 |
| `annotated_data/batch_001/out_48PT5RTF_Abdalla_and_Mahfoudhi_-_2024_-.md` | .md | 90275 |
| `annotated_data/batch_001/out_48WJWLBR_Richardson_et_al_-_2018_-_Food.md` | .md | 42436 |
| `annotated_data/batch_001/out_49X25EFC_Katznelson_et_al_-_2001_-_What.md` | .md | 54789 |
| `annotated_data/batch_001/out_4AWYQ57Q_Geluso_-_2022_-_Grammatical_and.md` | .md | 60433 |
| `annotated_data/batch_001/out_4CCCNXLS_Siegel_-_2021_-_Evaluating_EAP.md` | .md | 28690 |
| `annotated_data/batch_001/out_4CY8WG4R_Omidian_et_al_-_2021_-_A_new_mu.md` | .md | 80346 |
| `annotated_data/batch_001/out_4DE6I4WP_Wang_et_al_-_2024_-_Learners’_p.md` | .md | 78512 |
| `annotated_data/batch_001/out_4E6TR4DA_Liu_-_2021_-_Book_review.md` | .md | 11375 |
| `annotated_data/batch_001/out_4F4DFXSL_Chan_-_2013_-_The_Role_of_Situa.md` | .md | 44610 |
| `annotated_data/batch_001/out_4F8P56QI_Gaies_-_1980_-_T-Unit_Analysis.md` | .md | 24595 |
| `annotated_data/batch_001/out_4FW5V43U_Stotesbury_-_2009_-_[No_title_f.md` | .md | 10785 |
| `annotated_data/batch_001/out_4G59ZW5V_Chan_-_2024_-_Generative_AI_in.md` | .md | 842419 |
| `annotated_data/batch_001/out_4GKTU86D_1-s2_0-S1060374306000622-main.md` | .md | 71522 |
| `annotated_data/batch_001/out_4IA4S2HW_Impressing_Artificial_Intellige.md` | .md | 23209 |
| `annotated_data/batch_001/out_4IUH4R8S_Yanto_-_2024_-_Scaffolding_for.md` | .md | 17859 |
| `annotated_data/batch_001/out_4J65AES9_Tommerdahl_et_al_-_2024_-_A_sys.md` | .md | 74445 |
| `annotated_data/batch_001/out_4L8FELKB_Topping_-_1998_-_Peer_Assessmen.md` | .md | 90003 |
| `annotated_data/batch_001/out_4LEBX6DT_Angelopoulos_et_al_-_2023_-_Exp.md` | .md | 92576 |
| `annotated_data/batch_001/out_4LRYJTA2_Inquiry_about_traffic_signal_re.md` | .md | 8301 |
| `annotated_data/batch_001/out_4M7Y8LI2_Qiu_and_(Kevin)_Jiang_-_2021_-.md` | .md | 64763 |
| `annotated_data/batch_001/out_4MAKAJU4_Demirdöken_and_Atay_-_2024_-_En.md` | .md | 84786 |
| `annotated_data/batch_001/out_4N52ANBS_[Patrick_Saint-Dizier]_Syntax_a.md` | .md | 815022 |
| `annotated_data/batch_001/out_4NDTN5UM_Soliman_and_Khalil_-_2024_-_The.md` | .md | 50389 |
| `annotated_data/batch_001/out_4PVBPIXS_Aryadoust_-_2024_-_Topic_and_Ac.md` | .md | 77492 |
| `annotated_data/batch_001/out_4PXC74XQ_Li_and_Ngai_-_2018_-_Challenges.md` | .md | 38314 |
| `annotated_data/batch_001/out_4Q4WC3UP_Saadatara_et_al_-_2023_-_Bundle.md` | .md | 104220 |
| `annotated_data/batch_001/out_4QMIXU44_Critical_analysis_of_the_techno.md` | .md | 70300 |
| `annotated_data/batch_001/out_4QWL8GJV_Sharples_-_2023_-_Towards_socia.md` | .md | 23139 |
| `annotated_data/batch_001/out_4R4GIGKW_Hoang_and_Hoang_-_2024_-_Enhanc.md` | .md | 62770 |
| `annotated_data/batch_001/out_4RTYGVHS_Fleury-Vilatte_and_Hert_-_2003.md` | .md | 22456 |
| `annotated_data/batch_001/out_4RWUF8UV_Troyan_et_al_-_2023_-_Toward_hu.md` | .md | 73243 |
| `annotated_data/batch_001/out_4S2W9FNS_Shaw_and_Pecorari_-_2013_-_Sour.md` | .md | 13693 |
| `annotated_data/batch_001/out_4SSSC9AH_Saville_-_2011_-_Strategies_for.md` | .md | 26931 |
| `annotated_data/batch_001/out_4VCJSVPC_Giannoni_-_2008_-_Medical_writi.md` | .md | 38407 |
| `annotated_data/batch_001/out_4W39A6BA_Bailey_and_Garner_-_2010_-_Is_t.md` | .md | 40448 |
| `annotated_data/batch_001/out_4WLLLEPP_Barkaoui_-_2024_-_Exploring_the.md` | .md | 88663 |
| `annotated_data/batch_001/out_4XUM4T8Q_Cummings_et_al_-_2024_-_Generat.md` | .md | 55131 |
| `annotated_data/batch_001/out_4XYCUWZ6_Bourne_-_2007_-_Ten_Simple_Rule.md` | .md | 8160 |
| `annotated_data/batch_001/out_4Z4RFQHB_Morgan_-_2016_-_Language_Teache.md` | .md | 73409 |
| `annotated_data/batch_001/out_4ZE9L4BP_Jorgensen_2002_Understanding_th.md` | .md | 55839 |
| `annotated_data/batch_001/out_52P3UQM2_Etori_and_Gini_-_2024_-_WisComp.md` | .md | 59468 |
| `annotated_data/batch_001/out_53FTYRYH_Sun_and_Soden_-_2021_-_Internat.md` | .md | 78124 |
| `annotated_data/batch_001/out_544TALQE_Bugaj_et_al_-_2021_-_What_do_Fi.md` | .md | 42464 |
| `annotated_data/batch_001/out_54DIG5K9_Richards_-_2010_-_Mentoring_Pre.md` | .md | 67708 |
| `annotated_data/batch_001/out_54FXNZ8H_Swales_-_2009_-_When_there_is_n.md` | .md | 37943 |
| `annotated_data/batch_001/out_55K3RT8M_Zheng_and_Drybrough_-_2023_-_Tr.md` | .md | 50761 |
| `annotated_data/batch_001/out_569QG44N_Hu_-_2023_-_What_can_be_done_to.md` | .md | 3323 |
| `annotated_data/batch_001/out_56JMSINX_Alharbi_and_Alkhonini_-_2024_-.md` | .md | 19925 |
| `annotated_data/batch_001/out_578HPFBY_Liu_and_Sadler_-_2003_-_The_eff.md` | .md | 89508 |
| `annotated_data/batch_001/out_57D56IDU_Reddick_-_2024_-_How_educators.md` | .md | 65782 |
| `annotated_data/batch_001/out_57QH5KT9_Bernicot_et_al_-_2012_-_Forms_a.md` | .md | 72411 |
| `annotated_data/batch_001/out_5893ENYL_Zhang_and_Liu_-_2023_-_An_inves.md` | .md | 73387 |
| `annotated_data/batch_001/out_58KA3BNN_Ash’ari_et_al_-_2023_-_The_rhet.md` | .md | 76116 |
| `annotated_data/batch_001/out_59TRRNAI_Topping_-_2015_-_Peer_tutoring.md` | .md | 92779 |
| `annotated_data/batch_001/out_5A83PH6S_Eilam_et_al_-_2020_-_Climate_Ch.md` | .md | 123444 |
| `annotated_data/batch_001/out_5ABGGSD4_Ur_-_1999_-_A_course_in_languag.md` | .md | 250985 |
| `annotated_data/batch_001/out_5AVJ85GS_Goldstein_-_2004_-_Questions_an.md` | .md | 62577 |
| `annotated_data/batch_001/out_5C6F3LPM_147126266.md` | .md | 215413 |
| `annotated_data/batch_001/out_5CCA9SPX_Farazouli_et_al_-_2023_-_Hello.md` | .md | 52764 |
| `annotated_data/batch_001/out_5CTXFKYW_Jones_et_al_-_2006_-_Interactio.md` | .md | 67186 |
| `annotated_data/batch_001/out_5D5AYBHM_2017_HKDSE_ENG_P2.md` | .md | 16187 |
| `annotated_data/batch_001/out_5DN9IZ29_Liu_et_al_-_2023_-_Discoursing.md` | .md | 75033 |
| `annotated_data/batch_001/out_5DRSUVD4_Virvou_and_Tsiriga_-_2001_-_Web.md` | .md | 19998 |
| `annotated_data/batch_001/out_5E45RXFP_Topping_-_1996_-_The_Effectiven.md` | .md | 74569 |
| `annotated_data/batch_001/out_5ELCN2GH_Groves_and_Mundt_-_2021_-_A_gho.md` | .md | 57449 |
| `annotated_data/batch_001/out_5EWI9UJ2_Kessler_et_al_-_2024_-_Writing.md` | .md | 65977 |
| `annotated_data/batch_001/out_5EXH7M58_Written_corrective_feedback_in.md` | .md | 122608 |
| `annotated_data/batch_001/out_5FE4JSP3_Chan_-_1997_-_The_Legacy_of_the.md` | .md | 46815 |
| `annotated_data/batch_001/out_5FIAW58F_Flowerdew_and_Wang_-_2015_-_Ide.md` | .md | 64950 |
| `annotated_data/batch_001/out_5GB9RDMD_Moskovsky_et_al_-_2015_-_Bottom.md` | .md | 52492 |
| `annotated_data/batch_001/out_5GHHM466_Depraetere_et_al_-_2024_-_Build.md` | .md | 72248 |
| `annotated_data/batch_001/out_5H24PLT6_Analyzing-engagement-strategies.md` | .md | 74345 |
| `annotated_data/batch_001/out_5H2VPLSB_Skrabut_-_80_Ways_to_Use_ChatGP.md` | .md | 204959 |
| `annotated_data/batch_001/out_5H5K8ACC_Chan_and_Hu_-_2023_-_Students’.md` | .md | 66392 |
| `annotated_data/batch_001/out_5HNMM7L2_Baidoo-Anu_and_Ansah_-_Educatio.md` | .md | 38695 |
| `annotated_data/batch_001/out_5ITTA93H_Huang_and_Xia_-_2024_-_Preparin.md` | .md | 75036 |
| `annotated_data/batch_001/out_5KLLNASH_Brice_and_Pelaez-Morales_-_2024.md` | .md | 71190 |
| `annotated_data/batch_001/out_5KMV9VUV_svoboda2015.md` | .md | 62107 |
| `annotated_data/batch_001/out_5M64NGJJ_Alharbi_-_2022_-_Book_review.md` | .md | 10906 |
| `annotated_data/batch_001/out_5M87DHT5_Dörnyei_-_2001_-_Motivational_s.md` | .md | 340873 |
| `annotated_data/batch_001/out_5MGFGJIE_Unlu_and_Wharton_-_2015_-_Explo.md` | .md | 64660 |
| `annotated_data/batch_001/out_5MQQU7RI_Wingate_and_Harper_-_2021_-_Com.md` | .md | 56051 |
| `annotated_data/batch_001/out_5N5RVS9N_Patton_and_Parker_-_2017_-_Teac.md` | .md | 12270 |
| `annotated_data/batch_001/out_5NTF3DXR_Galante_-_2024_-_Translanguagin.md` | .md | 53009 |
| `annotated_data/batch_001/out_5PG8HZAM_Jo_-_2021_-_Short_vs_extended_a.md` | .md | 78742 |
| `annotated_data/batch_001/out_5PQFC84F_Xiao_-_Reflection_and_Standardi.md` | .md | 15504 |
| `annotated_data/batch_001/out_5PTTLTFZ_Editorial-Board_2024_Journal-of.md` | .md | 3286 |
| `annotated_data/batch_001/out_5QSBBYQL_Bowman-Perrott_et_al_-_2013_-_A.md` | .md | 73667 |
| `annotated_data/batch_001/out_5QSJHR5I_Rose_et_al_-_2008_-_Scaffolding.md` | .md | 65926 |
| `annotated_data/batch_001/out_5RBLK99C_Kim_et_al_-_2024_-_Daily_and_et.md` | .md | 67372 |
| `annotated_data/batch_001/out_5RCN77AS_Boodia-Canoo_-_2022_-_Book_revi.md` | .md | 10466 |
| `annotated_data/batch_001/out_5SIJ68YI_Nagda_et_al_-_2003_-_Transforma.md` | .md | 91218 |
| `annotated_data/batch_001/out_5ULDUX9S_Tarigan_and_Lasnumanda_-_2020_-.md` | .md | 31875 |
| `annotated_data/batch_001/out_5V9ADGBH_Derakhshan_and_Javad_Zare_-_202.md` | .md | 11452 |
| `annotated_data/batch_001/out_5VI69CIQ_Lee_et_al_-_2024_-_Enhancing_Pr.md` | .md | 64702 |
| `annotated_data/batch_001/out_5XAGHU7E_Siegel_-_2015_-_A_pedagogic_cyc.md` | .md | 31831 |
| `annotated_data/batch_001/out_5XLQA5B9_Guo_-_2024_-_EvaluMate_Using_AI.md` | .md | 23658 |
| `annotated_data/batch_001/out_5YVZE5ZW_Fang_et_al_-_2021_-_Nominal_com.md` | .md | 93990 |
| `annotated_data/batch_001/out_62KUTTSA_2018_定义_教师教学能力系统构成及水平层级模型研究_王磊.md` | .md | 28248 |
| `annotated_data/batch_001/out_62QHXU72_Wang_and_Csomay_-_2024_-_Constr.md` | .md | 84776 |
| `annotated_data/batch_001/out_636AGMGT_Cheong_et_al_-_2024_-_Character.md` | .md | 80477 |
| `annotated_data/batch_001/out_63W62AT6_Zhang_and_Zou_-_2024_-_Self-reg.md` | .md | 125985 |
| `annotated_data/batch_001/out_64GBVTWU_walton2014.md` | .md | 106762 |
| `annotated_data/batch_001/out_64NY524D_Sullivan_-_2014_-_China’s_Weibo.md` | .md | 47747 |
| `annotated_data/batch_001/out_67BBJGIP_White_et_al_-_2023_-_A_Prompt_P.md` | .md | 111185 |
| `annotated_data/batch_001/out_67QPJJ4X_Podcasting-science--Rhetorical-.md` | .md | 66911 |
| `annotated_data/batch_001/out_69Q86FZ4_Brewer_-_2021_-_BALEAP_News.md` | .md | 6310 |
| `annotated_data/batch_001/out_6A9MTMV9_Cinkara_and_Yüksel_-_2024_-_Per.md` | .md | 72771 |
| `annotated_data/batch_001/out_6C3LXNPA_Kirk_and_King_-_2022_-_EAP_teac.md` | .md | 52560 |
| `annotated_data/batch_001/out_6C554RU4_[Scott_Bennett]_The_Elements_of.md` | .md | 188367 |
| `annotated_data/batch_001/out_6C7LXI5F_Hamp-Lyons_-_2009_-_Editorial.md` | .md | 10170 |
| `annotated_data/batch_001/out_6CB63LFK_Blau_et_al_-_2002_-_Guilt-free.md` | .md | 54499 |
| `annotated_data/batch_001/out_6CBB4MK4_Hayes_et_al_-_2018_-_Climate_ch.md` | .md | 73278 |
| `annotated_data/batch_001/out_6CBE5FS8_Poole_et_al_-_2021_-_Corrigendu.md` | .md | 1782 |
| `annotated_data/batch_001/out_6D2497W4_Eddy-U_-_2015_-_Motivation_for.md` | .md | 64937 |
| `annotated_data/batch_001/out_6E383HK2_Yu_-_2023_-_A_Cross-Cultural_Ge.md` | .md | 99540 |
| `annotated_data/batch_001/out_6E4DAVUI_Puimege_et_al_-_2024_-_The_effe.md` | .md | 64886 |
| `annotated_data/batch_001/out_6ERPHXKW_Winch_-_2018_-_Google_Translate.md` | .md | 9957 |
| `annotated_data/batch_001/out_6EVTW2I4_Read_-_2002_-_The_use_of_intera.md` | .md | 49218 |
| `annotated_data/batch_001/out_6FEUX46I_Freddi_-_2005_-_Arguing_linguis.md` | .md | 61711 |
| `annotated_data/batch_001/out_6G2U2CTZ_Editorial-Board_2023_Journal-of.md` | .md | 3286 |
| `annotated_data/batch_001/out_6GKIMXRE_Foreword_-_Studies_in_Higher_Ed.md` | .md | 6607 |
| `annotated_data/batch_001/out_6GXDM5IF_Effectiveness_of_student_academ.md` | .md | 54109 |
| `annotated_data/batch_001/out_6HFK4NBB_Harwood_-_2005_-_What_do_we_wan.md` | .md | 41067 |
| `annotated_data/batch_001/out_6JKIBZA7_Yonemura_-_1986_-_Reflections_o.md` | .md | 25682 |
| `annotated_data/batch_001/out_6KS8SD5I_Abdi_-_2002_-_Interpersonal_met.md` | .md | 20572 |
| `annotated_data/batch_001/out_6MUHMWUK_Flowerdew_and_Miller_-_2008_-_S.md` | .md | 56349 |
| `annotated_data/batch_001/out_6N3KF24I_Lin_and_Chen_-_2024_-_Investiga.md` | .md | 77331 |
| `annotated_data/batch_001/out_6N8YUJPR_Bowen_and_Nanni_-_2021_-_Piracy.md` | .md | 68264 |
| `annotated_data/batch_001/out_6NFXXV4Q_Exploring_EFL_teachers’_emotion.md` | .md | 68601 |
| `annotated_data/batch_001/out_6P7WUPV6_Emmanouil_et_al_-_2024_-_Lingui.md` | .md | 49195 |
| `annotated_data/batch_001/out_6PI9VHSK_Neupane_Bastola_and_Ho_-_2022_-.md` | .md | 61907 |
| `annotated_data/batch_001/out_6PV53VSW_Soto-Corominas_et_al_-_2024_-_T.md` | .md | 68931 |
| `annotated_data/batch_001/out_6QRADZS8_Jin_et_al_-_2022_-_“Their_encou.md` | .md | 63887 |
| `annotated_data/batch_001/out_6QUTXZIE_shei2008.md` | .md | 52377 |
| `annotated_data/batch_001/out_6T7VTFUR_Pole_and_Parashar_-_2020_-_Am_I.md` | .md | 28800 |
| `annotated_data/batch_001/out_6TRKNYIW_MacDiarmid_et_al_-_2023_-_BALEA.md` | .md | 6003 |
| `annotated_data/batch_001/out_6TWBR89E_Palmour_-_2023_-_Assessing_oral.md` | .md | 55180 |
| `annotated_data/batch_001/out_6U2XC4VL_Moorhouse_-_2024_-_Beginning_an.md` | .md | 64208 |
| `annotated_data/batch_001/out_6UEUTKET_Ryan_and_Tilbury_-_Flexible_Ped.md` | .md | 145514 |
| `annotated_data/batch_001/out_6UGFKNAU_Thorne_-_2024_-_Generative_arti.md` | .md | 24278 |
| `annotated_data/batch_001/out_6VL6SKZV_Yang_-_2023_-_First_language_at.md` | .md | 9478 |
| `annotated_data/batch_001/out_6VZ45FYF_Yasuda_-_2023_-_What_does_it_me.md` | .md | 67609 |
| `annotated_data/batch_001/out_6X8GGMU6_Goldsmith_et_al_-_2022_-_A_mult.md` | .md | 72331 |
| `annotated_data/batch_001/out_6XLLSQ7B_Dai_et_al_-_2024_-_Generative_A.md` | .md | 34726 |
| `annotated_data/batch_001/out_6Z22NZM7_Editorial-Board_2024_Journal-of.md` | .md | 3286 |
| `annotated_data/batch_001/out_6Z4GF2SG_Heyns_-_2022_-_JEAP_-_BALEAP_Ne.md` | .md | 5947 |
| `annotated_data/batch_001/out_6Z977356_Poláková_and_Klímová_-_2019_-_M.md` | .md | 46865 |
| `annotated_data/batch_001/out_6ZSMSUBK_Blachford_and_Zhang_-_2014_-_Re.md` | .md | 65029 |
| `annotated_data/batch_001/out_6ZZ4GYET_Wu_-_2024_-_The_effects_of_Hakk.md` | .md | 48731 |
| `annotated_data/batch_001/out_7276FV7S_Stosic_-_2022_-_A_linguistic_co.md` | .md | 66070 |
| `annotated_data/batch_001/out_72DFQPZF_Colvin_-_2007_-_Peer_tutoring_a.md` | .md | 52929 |
| `annotated_data/batch_001/out_72E8D3X7_Voigt_and_Girgensohn_-_2015_-_P.md` | .md | 35502 |
| `annotated_data/batch_001/out_72WE9PXW_The_need_for_critical_digital_l.md` | .md | 30231 |
| `annotated_data/batch_001/out_73E9A5CI_Siegel_-_2018_-_Did_you_take_“g.md` | .md | 38352 |
| `annotated_data/batch_001/out_73H7ECBB_Martin_and_Hill_-_1991_-_Modern.md` | .md | 2979 |
| `annotated_data/batch_001/out_73MZ7THB_A_comparative_study_of_thematic.md` | .md | 90616 |
| `annotated_data/batch_001/out_73XF5B23_Jaworska_and_Krishnamurthy_-_20.md` | .md | 102266 |
| `annotated_data/batch_001/out_749M2UQA_Brezina_-_2013_-_Corpus_tools_i.md` | .md | 5591 |
| `annotated_data/batch_001/out_74FBQKVM_Zhang_-_2013_-_Business_English.md` | .md | 70211 |
| `annotated_data/batch_001/out_74H7ZZ2J_Shibata_-_2020_-_The_Usefulness.md` | .md | 17173 |
| `annotated_data/batch_001/out_74KSNK9F_Li_and_Ye_-_2023_-_Patterns_and.md` | .md | 79423 |
| `annotated_data/batch_001/out_757Q58H6_Strzelecki_-_2023_-_To_use_or_n.md` | .md | 59623 |
| `annotated_data/batch_001/out_7586EBYL_Exemplification-and-reformulati.md` | .md | 73531 |
| `annotated_data/batch_001/out_75TWFQ8H_So_et_al_-_2024_-_Exploring_pub.md` | .md | 77547 |
| `annotated_data/batch_001/out_76BMP4EE_Zhang_et_al_-_2024_-_An_explora.md` | .md | 90711 |
| `annotated_data/batch_001/out_76D9XWZ3_Wei_and_Zhao_-_2024_-_Effects_o.md` | .md | 70029 |
| `annotated_data/batch_001/out_76FFZSFC_Bauer_et_al_-_2023_-_Using_natu.md` | .md | 95277 |
| `annotated_data/batch_001/out_76R52MNH_Crookes-Lehner-TQ322-1998.md` | .md | 25143 |
| `annotated_data/batch_001/out_7788A62A_Watson_Todd_-_2003_-_EAP_or_TEA.md` | .md | 31678 |
| `annotated_data/batch_001/out_78D3TFLV_Ma_and_Lei_-_2024_-_The_factors.md` | .md | 75089 |
| `annotated_data/batch_001/out_78J9KR94_Yung_-_2015_-_Learning_English.md` | .md | 64411 |
| `annotated_data/batch_001/out_78JDW8A4_Kouzelis_and_Spantidi_-_2024_-.md` | .md | 34491 |
| `annotated_data/batch_001/out_78S2AFHM_Rezaee_et_al_-_2014_-_Symmetric.md` | .md | 66611 |
| `annotated_data/batch_001/out_79Q4QKRW_Dowell_et_al_-_2016_-_Language.md` | .md | 81764 |
| `annotated_data/batch_001/out_79VLG23Q_Gu_-_2023_-_Book_review.md` | .md | 10664 |
| `annotated_data/batch_001/out_7A6IR6PI_Gales_-_2009_-_Diversity'as_ena.md` | .md | 58386 |
| `annotated_data/batch_001/out_7AWTMKCK_Simpson_-_2024_-_A_practitioner.md` | .md | 31504 |
| `annotated_data/batch_001/out_7B65IWGZ_Yenkimaleki_et_al_-_2024_-_The.md` | .md | 63172 |
| `annotated_data/batch_001/out_7BR56HUA_Cushing_-_2024_-_Ungrading_as_a.md` | .md | 8182 |
| `annotated_data/batch_001/out_7CAK96MA_Hyland_-_2003_-_Second_language.md` | .md | 38488 |
| `annotated_data/batch_001/out_7DEWTUMS_Hyland_and_Tse_-_2004_-_Metadis.md` | .md | 66065 |
| `annotated_data/batch_001/out_7DPFV2MF_HBR2021_AI-Should-Augment-Human.md` | .md | 14588 |
| `annotated_data/batch_001/out_7DYQ8SAI_Heyns_-_2024_-_BALEAP_news_-_In.md` | .md | 6234 |
| `annotated_data/batch_001/out_7EM2FXDK_Fujiwara_and_Shimada_-_2024_-_A.md` | .md | 49613 |
| `annotated_data/batch_001/out_7ENP457C_Zokaeieh_et_al_-_2019_-_Develop.md` | .md | 54307 |
| `annotated_data/batch_001/out_7F2YJSMR_Bu_-_2014_-_Towards_a_pragmatic.md` | .md | 77867 |
| `annotated_data/batch_001/out_7FSWFZUI_Kim_et_al_-_Journal_of_Second_L.md` | .md | 4395 |
| `annotated_data/batch_001/out_7GQWEZBE_Hall_-_2011_-_Exploring_English.md` | .md | 653333 |
| `annotated_data/batch_001/out_7HBKTTNJ_Editorial-Board_2024_Assessing-.md` | .md | 3917 |
| `annotated_data/batch_001/out_7HEH8VSA_ChatGPT_as_a_tool_for_self-lear.md` | .md | 125701 |
| `annotated_data/batch_001/out_7IX5C4H5_Ming_and_Wenbin_-_2024_-_“Contr.md` | .md | 80247 |
| `annotated_data/batch_001/out_7J8446UV_Krishnamurthy_and_Kosem_-_2007.md` | .md | 57139 |
| `annotated_data/batch_001/out_7JHVKGET_Creese_and_Blackledge_-_2015_-.md` | .md | 53005 |
| `annotated_data/batch_001/out_7JITPGKK_[Ken_Hyland;_Lillian_L__C_Wong].md` | .md | 759657 |
| `annotated_data/batch_001/out_7LMEXQPR_Berghmans_et_al_-_2013_-_A_typo.md` | .md | 76381 |
| `annotated_data/batch_001/out_7LWNPHHZ_Hollenback_-_2019_-_The_Necessi.md` | .md | 23637 |
| `annotated_data/batch_001/out_7LYURYAL_Narciss_-_Designing_and_Evaluat.md` | .md | 77487 |
| `annotated_data/batch_001/out_7MLICMEW_Yan_et_al_-_2024_-_Promises_and.md` | .md | 194880 |
| `annotated_data/batch_001/out_7MWYF844_From-general-critical-questions.md` | .md | 84492 |
| `annotated_data/batch_001/out_7PNEITYN_Kohnke_et_al_-_2023_-_ChatGPT_f.md` | .md | 26787 |
| `annotated_data/batch_001/out_7QS4563C_Fairclough_-_2016_-_Evaluating.md` | .md | 79695 |
| `annotated_data/batch_001/out_7S5959UH_Reid_and_Kroll_-_2006_-_Designi.md` | .md | 66527 |
| `annotated_data/batch_001/out_7SR9752R_Yang_and_Wang_-_2023_-_Book_rev.md` | .md | 11454 |
| `annotated_data/batch_001/out_7SWANWRP_Li_et_al_-_2024_-_Advancing_the.md` | .md | 67835 |
| `annotated_data/batch_001/out_7TYH9BSI_Severino_et_al_-_2024_-_March_2.md` | .md | 70515 |
| `annotated_data/batch_001/out_7UP5QSFJ_Human–Machine_Collaboration_in.md` | .md | 15007 |
| `annotated_data/batch_001/out_7VDSUICD_Sudowrite_Co-Writing_Creative_S.md` | .md | 12459 |
| `annotated_data/batch_001/out_7VKIDA7L_Khushik_-_2024_-_Is_the_variati.md` | .md | 67788 |
| `annotated_data/batch_001/out_7VKXGLP7_Ortega-Sánchez_et_al_-_2020_-_S.md` | .md | 59248 |
| `annotated_data/batch_001/out_7VSAI6MB_Schauer_and_Adolphs_-_2006_-_Ex.md` | .md | 55982 |
| `annotated_data/batch_001/out_7VWUWVH4_Graça_et_al_-_2019_-_Reducing_m.md` | .md | 89374 |
| `annotated_data/batch_001/out_7VXLX34K_Cope_and_Kalantzis_-_2024_-_A_m.md` | .md | 96300 |
| `annotated_data/batch_001/out_7WRNNMIW_Qiu_et_al_-_2024_-_Interactiona.md` | .md | 85017 |
| `annotated_data/batch_001/out_7XDTRGTK_[Gillian_Brown,_George_Yule]_Di.md` | .md | 651693 |
| `annotated_data/batch_001/out_7Y7XPPUZ_King_et_al_2000_Public_speaking.md` | .md | 37542 |
| `annotated_data/batch_001/out_7YMYKSAZ_Bailey_and_Lee_-_2020_-_An_Expl.md` | .md | 70039 |
| `annotated_data/batch_001/out_7YRHF82K_An_Examination_of_Inter-Rater_O.md` | .md | 363760 |
| `annotated_data/batch_001/out_7Z2RVB2Q_2024_State_of_Generative_AI_in.md` | .md | 20737 |
| `annotated_data/batch_001/out_7Z8GZTZG_Seyyedrezaei_et_al_-_2024_-_A_m.md` | .md | 113868 |
| `annotated_data/batch_001/out_7ZSGB7SW_2021_线上线下融合情境下大学外语教师能力框架构建_徐锦芬.md` | .md | 29438 |
| `annotated_data/batch_001/out_824GM9WD_Trotman_-_2011_-_ACTION_RESEARC.md` | .md | 39968 |
| `annotated_data/batch_001/out_82A22M5J_Nesi_and_Hu_-_Journal_of_Englis.md` | .md | 4144 |
| `annotated_data/batch_001/out_833N6KBQ_Chen_-_2022_-_Book_review.md` | .md | 9586 |
| `annotated_data/batch_001/out_83JLZT5R_Zhao_-_2024_-_A_corpus-based_mu.md` | .md | 87039 |
| `annotated_data/batch_001/out_83K3GBZ6_Hidalgo_Tenorio_and_Internation.md` | .md | 3391 |
| `annotated_data/batch_001/out_84KQCWFP_Bergstrom_-_2024_-_“None_of_You.md` | .md | 51918 |
| `annotated_data/batch_001/out_84P4KTJ6_Developing_language_teachers’_p.md` | .md | 67555 |
| `annotated_data/batch_001/out_85EVM7WP_A-scaffolded-speaking-and-writi.md` | .md | 77278 |
| `annotated_data/batch_001/out_86UYQB5E_Nimehchisalem_and_Mukundan_-_20.md` | .md | 54535 |
| `annotated_data/batch_001/out_86WT84SE_Tan_-_2023_-_An_exploratory_stu.md` | .md | 53277 |
| `annotated_data/batch_001/out_86XHYTYM_Pigg_-_2024_-_Research_writing.md` | .md | 69850 |
| `annotated_data/batch_001/out_86ZD7GSV_Investigating_the_capabilities.md` | .md | 62550 |
| `annotated_data/batch_001/out_879CUXIX_Investigating_the_capabilities.md` | .md | 62550 |
| `annotated_data/batch_001/out_87FZ8QCF_Kim_and_Lu_-_2024_-_Exploring_t.md` | .md | 79600 |
| `annotated_data/batch_001/out_89EK9SSJ_InVideo_AI_Creating_Instruction.md` | .md | 10530 |
| `annotated_data/batch_001/out_8ADAF33M_Engberg_-_2023_-_Book_review.md` | .md | 10656 |
| `annotated_data/batch_001/out_8ALY5PYW_Leshem_-_2012_-_The_Many_Faces.md` | .md | 55193 |
| `annotated_data/batch_001/out_8AT4Q4KV_Flowerdew_-_2005_-_Integrating.md` | .md | 38524 |
| `annotated_data/batch_001/out_8BLIMV3S_Littlejohn_Materials_The_analys.md` | .md | 72082 |
| `annotated_data/batch_001/out_8BN7REJB_Can_novice_teachers_detect_AI-g.md` | .md | 26977 |
| `annotated_data/batch_001/out_8CBGVKX8_Van_Leeuwen_-_2009_-_Discourses.md` | .md | 27798 |
| `annotated_data/batch_001/out_8CCPCTCH_Generative_AI-assisted,_evidenc.md` | .md | 40845 |
| `annotated_data/batch_001/out_8D6HFP2J_Harrison_-_2021_-_Showing_as_se.md` | .md | 59992 |
| `annotated_data/batch_001/out_8DSFV4UL_Crawford_Camiciottoli_-_2021_-.md` | .md | 55664 |
| `annotated_data/batch_001/out_8FC4FEJV_Wang_et_al_-_2024_-_Language_le.md` | .md | 119481 |
| `annotated_data/batch_001/out_8FTC246S_Song_and_Reynolds_-_2022_-_The.md` | .md | 80292 |
| `annotated_data/batch_001/out_8H6J8IFT_A_corpus-based_evaluation_of_sy.md` | .md | 79015 |
| `annotated_data/batch_001/out_8HAI64I2_Perceptions_of_supervisors_and.md` | .md | 84188 |
| `annotated_data/batch_001/out_8HGRRDC8_Evaluating_AI's_impact_on_self-.md` | .md | 88405 |
| `annotated_data/batch_001/out_8HW7JC7T_2009_-_Metadiscourse_in_Academi.md` | .md | 77172 |
| `annotated_data/batch_001/out_8HYMQYRX_Martínez_-_2008_-_Building_cons.md` | .md | 38602 |
| `annotated_data/batch_001/out_8IKCKN8T_Tardy_-_2005_-_“It's_like_a_sto.md` | .md | 46200 |
| `annotated_data/batch_001/out_8IULM97Q_Hu_-_2023_-_Radical_cures_for_a.md` | .md | 3352 |
| `annotated_data/batch_001/out_8JIMSBFJ_wharton2012.md` | .md | 54326 |
| `annotated_data/batch_001/out_8JJN4BFS_Tai_-_2022_-_Effects_of_intelli.md` | .md | 89524 |
| `annotated_data/batch_001/out_8K36YCKH_Abasi_and_Graves_-_2008_-_Acade.md` | .md | 60251 |
| `annotated_data/batch_001/out_8LN2NBDV_Ho_-_2019_-_“Sensible_protester.md` | .md | 71337 |
| `annotated_data/batch_001/out_8MPM4GR4_Chami_et_al_-_2019_-_Nature’s_S.md` | .md | 14795 |
| `annotated_data/batch_001/out_8NBDCJBT_Mayer_2011.md` | .md | 125668 |
| `annotated_data/batch_001/out_8NCRR76N_Nassaji_and_Kartchava_-_2017_-.md` | .md | 565634 |
| `annotated_data/batch_001/out_8PD7G9JM_Elkins_and_Chun_-_2020_-_Can_GP.md` | .md | 31447 |
| `annotated_data/batch_001/out_8PDXI44L_2015_-_The_Effect_of_Two_Types.md` | .md | 26191 |
| `annotated_data/batch_001/out_8PWAI5CF_Pan_et_al_-_2023_-_Revisiting_a.md` | .md | 54320 |
| `annotated_data/batch_001/out_8QXCBJ6X_Diversity_and_Standards_in_Writ.md` | .md | 28369 |
| `annotated_data/batch_001/out_8RZUURMH_Belcher_et_al_-_2009_-_CRITICAL.md` | .md | 63749 |

<!-- AUTO_PROJECT_INDEX:END -->
