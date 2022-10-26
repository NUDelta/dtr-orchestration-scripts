# DTR Orchestration Scripts
Scripts to orchestrate common tasks for DTR, such as creating Sprint Logs.

## Setup
1. Make sure you have [Python 3.x](https://www.python.org/downloads/) (we use 3.8.5) and [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/#install-pipenv-today) installed.
2. Clone the repo to your local machine.
3. Install dependencies using `pipenv install`. To run scripts, start a virtual environment using `pipenv shell`. 
4. Generate a `credentials.json` for the [Google Drive v3 API](https://developers.google.com/drive/api/v3/quickstart/python) and a `service_account.json` for the [Google Spreadsheet API](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account). Place both of these files at the root of the cloned repo. _Note: these can be under the same project. See the instructions for [setting up gspread](https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project) to learn more._

## Available Scripts and Usage

### studio_db_to_json.py
This script is used to extract information from the [Studio Database Google Spreadsheet](https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0) for other scripts and tools. When run from the command line, it will download information from the Studio Database Spreadsheet, and parse it into a JSON file.

The script is run as follows: 
```commandline
python studio_db_to_json.py <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example: 
```commandline
python studio_db_to_json.py "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"
```

### create_ipm.py
This script is used to create Individal Progress Maps (IPMs) for a list of students specified in the command line argument, given a IPM template and an output directory.

The script is run as follows:
```commandline
python create_ipm.py <ipm_template_url> <ipm_folder_url> "[\"list\", \"of\", \"students\"]"
```

For example:
```commandline
python create_ipm.py "https://docs.google.com/spreadsheets/d/1AD5GSQ0K3gyblHPxOsP2E6b36DqLuW-WDqvi_GQSFN4/edit\?usp\=sharing" "https://drive.google.com/drive/u/1/folders/1rvw7IJKENjqsvLcQvb4tvld5L6skjSqH" "[\"Leesha Maliakal Shah\", \"Gobi Dasu\", \"Ryan Louie\", \"Kapil Garg\", \"Harrison Kwik\"]"
```

### create_sprint_logs.py
This script is used to create Sprint Logs for each student in DTR, given a Sprint Log template, output directory, and studio database with student and project information.

The script is run as follows: 
```commandline
python create_sprint_logs.py <sprint_log_template_url> <sprint_log_folder_url> <quarter_name> <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example, to create Sprint Logs for Fall 2020:
```commandline
python create_sprint_logs.py "https://docs.google.com/spreadsheets/d/1o1bA6VzpeTfXIhT-PwB8wm7uFfAt6saISTAmGB67d2w/edit#gid=0" "https://drive.google.com/drive/u/1/folders/1fvmX54RwN5YDjMc1id9phsmB6OSvfKcQ" "F2020" "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"
```

### create_the_weekly.py
This script is used to create The Weekly spreadsheets for each student in DTR, given a The Weekly template, output directory, and
studio database with student and project information.

The script is run as follows: 
```commandline
python create_the_weekly.py <the_weekly_template_url> <the_weekly_folder_url> <quarter_name> <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example, to create The Weekly for Fall 2020:
```commandline
python create_the_weekly.py "https://docs.google.com/spreadsheets/d/1NT9GZIZgZy7A-vEXGfY3fASkGzCkxLnKSXRfQ8ep3jE/edit?usp=sharing" "https://drive.google.com/drive/u/1/folders/1IauKy_xd70Y1uwCqSPQTV3BaFwSOK-Ig" "F2020" "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"
```

### create_mqc_individual.py
This script is used to create Mid-Quarter Check-In spreadsheets for each student in DTR, given a Mid-Quarter Check-In, output directory, and
studio database with student and project information.

The script is run as follows: 
```commandline
python create_mqc_individual.py <mqc_template_url> <mqc_folder_url> <quarter_name> <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example, to create the Mid-Quarter Check-In for Fall 2020:
```commandline
python create_mqc_individual.py "https://docs.google.com/spreadsheets/d/1GTXZZu7DVQxRa4mDsSD5OZivSwnv17nwAV6mroKztSs/edit?usp=sharing" "https://drive.google.com/drive/u/1/folders/1w-AK4hBoEwd_tZv-TMFabwpUgMR4RBB7" "F2020" "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"
```

### create_eoq_assessment.py
This script is used to create End-of-Quarter Self-Assessment spreadsheets for each student in DTR, given a template, output directory, and
studio database with student and project information.

The script is run as follows:
```commandline
python create_eoq_assessment.py <eoq-assessment_template_url> <eoq-assessment_folder_url> <quarter_name> <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example, to create End-of-Quarter Self-Assessments for Winter 2022:
```commandline
python create_eoq_assessment.py "https://docs.google.com/spreadsheets/d/188qL45SYEmURRuLc-vV6VtlDQwOiWEaF01yVe_1CiTc/edit?usp=sharing" "https://drive.google.com/drive/folders/1lhGlnu5SY2_3tIFuckbxNDE0xEIGyFFL" "W2022" "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"
```

### create_eoq_checklist.py
This script is used to create End-of-Quarter Checklists for each project in DTR, given a checklist template, output directory, and studio database with student and project information.

The script is run as follows:
```commandline
python create_eoq_checklist.py <eoq_checklist_template_url> <eoq_checklistfolder_url> <quarter_name> <studio_db_url> <sig_info_sheet_name> <proj_info_sheet_name>
```

For example, to create End-of-Quarter Checklists for Sprint 2022:
```commandline
python create_eoq_checklist.py "https://docs.google.com/document/d/1AZcju1KmgREFn8QYDShK27nDYxp1ZqvU8BxyKp17a1I/edit?usp=sharing" "https://drive.google.com/drive/u/1/folders/1MhY7EmMSJYOoeBOgpAI9PkrcQJMAHleS" "S2022" "https://docs.google.com/spreadsheets/d/1CqPVM11RhorBChGnhcYUNN02KMk5mhKEbuzQEY4vxQA/edit#gid=0" "SIG Info" "Proj Info"