# Summative-Lab-AI-Project-Management-CLI
AI Project Management CLI for Flatiron SE-FND2-FT

## Features
- Cumbersome interface that would've been better as an interactive menu system! It's left this way due to the module's emphasis on argparse.
- Users, their projects, and tasks for each project.
- AI Summary available for each project.
- Fancy formatting!
- All fields for all objects can be updated.
- Nearly all arguments have a short form, to make the painful typing process slightly easier.

## Installation
- Fork and clone the repo
- From a terminal inside the cloned folder, run `pipenv install` and `pipenv shell`
- From inside the shell, run `./main.py` followed by your arguments.

## Usage
Management of users and tasks comes in a tiered structure.
All commands have help info available. After each keyword, just enter `-h` or `--help` to see what options are available, and what's required or optional.
- `users` allows the user to `add`, `update`, `remove`, or `list` users.
  - These commands accept the arguments:
    - name: `-n/--name`
    - email: `-e/--email`
- `projects` allows the user to `add`, `update`, `remove`, or `list` projects. Also provides `summary` to get an AI summary of the specified project.
  - These commands accept the arguments:
    - user: `-u/--user`
    - title: `-t/--title`
    - description: `-d/--description`
    - due date: `--due_date`
  - The `list` argument can list all projects, grouped by user, or only list the projects of a user specified with `-u/--user`
- `tasks` allows the user to `add`, `update`, `remove`, or `list` tasks.
  - These commands accept the arguments:
    - user: `-u/--user`
    - project: `-p/--project`
    - title: `-t/--title`
    - status: `-s/--status`
    - assigned to: `-a/--assigned_to`
