# StudySprint

StudySprint is a study task management application built with Python and Streamlit.

## Features

* Dashboard to track study progress
* Add study tasks with subjects, due dates, priorities, and estimated study time
* View, search, and filter tasks
* Update task details and completion status
* Delete tasks
* View task completion charts and overdue task counts
* Store tasks using SQLite

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* SQLite

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shivench-rgb/StudySprint.git
   ```

2. Open the project folder and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   streamlit run app.py
   ```

## Project Structure

* `app.py`: Streamlit user interface
* `database.py`: Database operations
* `requirements.txt`: Python dependencies
* `studysprint.db`: Local SQLite database, generated when the app runs

## Author

Shiven Chaware
