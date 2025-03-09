# exam-check-tool
A tool to evaluate student exam answers using an LLM based approach.

## How to run?
1. Clone the repo and add a .env file and save your API key in environment variables.
2. Start the Flask server by running main.py at ui/backend/main.py.
3. Start the Node server by running npm start at ui/btp. This would open the UI page.
4. Follow along and create exam and add questions, scores, theory and student answer.
5. Create an exam_marking_schema file at ui/backend/exam_marking_schema.json.
6. Click on Evaluate Exam button on the UI page. This would call the API which can be seen in Flask server terminal.
7. After a while all the checked answers and other details are stored in data folder in form of a JSON file.
