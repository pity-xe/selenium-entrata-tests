# Selenium Test Suite for Entrata.com

## Overview
This project contains Selenium-based tests using Python and Pytest to validate the functionality of the Entrata website.

## Setup

### Prerequisites
- Python 3.x
- Google Chrome browser
- ChromeDriver

### Steps
1. Clone the repository:
   git clone https://github.com/<your-github-username>/selenium-entrata-tests.git
   cd selenium-entrata-tests

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate      # Windows

3. Install dependencies:
   pip install -r requirements.txt

4.Download and configure ChromeDriver.(UnZip the files in the location of your project folder.)

5.Run the tests:
   pytest -v test_homepage.py

  
  
### Conclusion

You now have the full setup for Selenium tests in Python, including virtual environments, dependencies, and tests written with Pytest. You can run these tests locally.


