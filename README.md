
# Project

## Description

In this project, we created a system that was modeled after IBM Watson's approach to answering
to Jeopardy questions. The system's main goal was to build an extensive database of information
using Wikipedia data. Our system focuses on parsing Wikipedia pages, indexing them in Whoosh,
and using natural language processing methods for query handling. Using metrics such as Mean
Reciprocal Rank (MRR), the system assesses its performance on Jeopardy-style clues with the
goal of identifying the most accurate responses.


## How to run project

 - First of all, install python (it works both with 3.8, 3.9 and 3.11).
 - Second of all, you will need to clone the project using the following command (make sure to check out to the branch master after the project is done cloning):
   ```
   git clone https://github.com/AliceHincu/IBM-Watson
   ```
   ```
   git checkout master
   ```
 - Then, you have to install the packages that the program needs to run it (if you don’t already have them) using this command in the terminal:
   ```
   pip install Whoosh nltk
   ```
 - Now you can run main by either using an IDE like PyCharm or with the command
   ```
   python main.py
   ```
