import json
import sys
import getopt
from itertools import chain


with open("data/users.json", "r") as inputs:
    all_users = json.load(inputs)
    inputs.close()

with open("data/venues.json", "r") as inputs:
    all_venues = json.load(inputs)
    inputs.close()


user_names = [user["name"] for user in all_users]

args = sys.argv[1:]
for arg in args:
    if arg == "everyone":
        print("You're taking the whole team!")
        break
    if arg not in user_names:
        print(f"Sorry, this is not a valid user. You can choose from: {user_names}")
        sys.exit(2)
    print("Yep, accepted")


# Filter the users list by those users that are going for food preferences
filtered_users = {user["name"]: { "wont_eat": user["wont_eat"], "drinks": user["drinks"]} for user in all_users if user["name"] in args}


# SORT OUT THE FOODS
# Get what they won't eat
banned_foods = [[food for food in user["wont_eat"]] for user in all_users if user["name"] in args] 
banned_foods_flattened = list(chain.from_iterable(banned_foods))

# Create dict to map banned foods to team members
banned_foods_dict = {food: [] for food in banned_foods_flattened}

for user, details in filtered_users.items():
    for food in details["wont_eat"]:
        if food in banned_foods_flattened:
            banned_foods_dict[food].append(user)

print(banned_foods_dict)
    

# SORT OUT THE DRINKS

# Get their favourite drinks
preferred_drinks = [[drink for drink in user["drinks"]] for user in all_users if user["name"] in args] 
preferred_drinks_flattened = list(chain.from_iterable(preffered_drinks))

# Create dict to map drink preferences to team members
preferred_drinks_dict = {drink: [] for drink in preferred_drinks_flattened}

for user, details in filtered_users.items():
    for drink in details["drinks"]:
        if drink in preferred_drinks_flattened:
            preferred_drinks_dict[food].append(user)

print(preferred_drinks_dict)


#users_foods = {user["wont_eat"] for user in all_users if user["name"] in args}

#users_drinks = {user["drinks"]: user["name"] for user in all_users if user["name"] in args}

#print(users_foods)
#print(users_drinks)

#   {
#         "name": "Karol Drewno",
#         "wont_eat": ["Bread", "Pasta"],
#         "drinks": ["Vodka", "Gin", "Whisky", "Rum"]
#     },


#TODO - Warn user if a person entered is not in the users list
#TODO - add validation for the JSON data format, types etc.
#TODO - Add some tests (also for incorrect or no names)
# TODO - can you validate the input files against a schema?
# TODO - Are there any errors in the input files?
#TODO - add a help script
# print(all_venues)
# print(all_users)