# Food & Drink Venue Picker 🍔


The purpose of this programme is to simplify choosing a place to go for food and drink, by taking into account team members' preferences.


## To Run this Programme

- You require: Python 3.7.2.
- A requirements.txt file is provided, so that you can install the necessary packages into a virtual environment of your choice before running.
- Place the users.json and venues.json into a directory named ```data``` within the project root directory.
- From the command line, in the project root, run the following:
    - ```python3 main.py 'FirstName LastName' 'FirstName LastName'```
    - The names must be names of valid team members - e.g. ```python3 main.py 'Tom Mullen' 'Rosie Curran'```
    - You may also run ```python3 main.py 'everyone'``` to select all team members

## To RUun the Tests
- Make sure you have created your virtual environment and installed everything in the requirements.txt file
- Then, from the root directory, run ```pytest test.py``` 


## Future Improvements 🚀
- Enhance test coverage, particularly to cover trickier edge cases which may arise
- Add additional data type validation to input json data
- Reduce number of temporary variables created, but balance with readability
- Add a command line help utility, to assist user in entering command in the correct format
- Allow user to specify path to input files, or to specify if these are located remotely e.g. in a cloud bucket or database