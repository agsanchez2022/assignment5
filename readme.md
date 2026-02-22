# Enhanced Calculator Application – Module 5

This repository contains a modular Python command-line calculator developed for the IS601 Module 5 assignment. The application demonstrates advanced software design patterns, persistent data management using pandas, environment-based configuration, and automated testing with continuous integration through GitHub Actions.

The calculator runs in a Read–Eval–Print Loop (REPL) that allows users to continuously perform calculations and manage their history. It supports arithmetic operations including addition, subtraction, multiplication, division, exponentiation (power), and root calculations. The application includes undo and redo functionality using the Memento design pattern, observers for logging and automatic saving of calculation history, interchangeable operation strategies implemented through the Strategy pattern, object creation through a Factory pattern, and a simplified interface using a Facade-style Calculator class.

Calculation history is stored and managed using pandas DataFrames and can be automatically saved to and loaded from CSV files. Application settings such as history size limits and auto-save behavior are controlled using environment variables loaded through python-dotenv.

## Project Structure

The project follows a flat modular structure:

app/ contains all calculator logic including the REPL interface, calculation models, operation strategies, configuration management, memento implementation, observers, validation, and exception handling.  
tests/ contains unit and parameterized tests for all major components.

## Setup Instructions

Clone the repository and navigate into the project directory. Create and activate a virtual environment using:

python3 -m venv venv  
source venv/bin/activate  

Install dependencies:

pip install -r requirements.txt  

Create a .env file in the project root with the following values:

CALCULATOR_MAX_HISTORY_SIZE=100  
CALCULATOR_AUTO_SAVE=true  
CALCULATOR_DEFAULT_ENCODING=utf-8  

Run the application:

python3 main.py  

## REPL Commands

help – display available commands  
history – show calculation history  
clear – clear stored history  
undo – undo the last calculation  
redo – redo the last undone calculation  
save – save history to file  
load – load history from file  
exit – exit the application  

## Testing and Coverage

Run all tests using:

pytest  

Run tests with coverage reporting:

pytest --cov=app --cov-report=term-missing  

GitHub Actions automatically runs all tests on every push and pull request to the main branch and enforces a minimum test coverage threshold.

## Continuous Integration

The project includes a GitHub Actions workflow that sets up Python, installs dependencies, runs pytest with coverage, and ensures code quality on every commit.

## Notes

Environment variables should not be committed to GitHub. A .env file is required locally to configure application behavior.

This project was developed as part of the IS601 Module 5 Enhanced Calculator Assignment.
