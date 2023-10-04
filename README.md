# thinking_feedback
Website providing quick feedback to students using Peter Liljedahl's Thinking Classroom methodology.

To see project in production, visit: https://thinking-feedback.onrender.com/ and login to:

Login: teacher

Password: thinking-feedback

How the webpage works?
It provides a framework to split the math lesson topics into single skills, generate grading tables for each student (each skill on 3 difficulty levels) and update the tables both by first selecting topic and skill as well as first selecting student and topic. Current tables are visible from student's account in real time.

## Installation

1. Create virtual environment and install dependencies from requirements.txt.
2. Set DATABASE_URL connection to your database in thinking_feedback/settings.py
3. Migrate database `python -m manage migrate`.
4. Run server with available port `python -m manage runserver 8080`.
