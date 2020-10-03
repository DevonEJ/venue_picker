import json
import sys
import getopt
import copy
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

    

# SORT OUT THE DRINKS

# Get their favourite drinks
preferred_drinks = [[drink for drink in user["drinks"]] for user in all_users if user["name"] in args] 
preferred_drinks_flattened = list(chain.from_iterable(preferred_drinks))

# Create dict to map drink preferences to team members
preferred_drinks_dict = {drink: [] for drink in preferred_drinks_flattened}

for user, details in filtered_users.items():
    for drink in details["drinks"]:
        if drink in preferred_drinks_flattened:
            preferred_drinks_dict[drink].append(user)



venues_response = {"places_to_visit": [],
                    "places_to_avoid":[]}

avoid_venue_dict = {
    "name": "",
    "reason": []
}

venues_food_pass = [] 
venues_food_fail = [] 

venues_drink_pass = [] 
venues_drink_fail = []
# Filter venues by foods first
for venue in all_venues:

    venue_foods = set(venue["food"])

    problem_foods = venue_foods.intersection(set(banned_foods_dict.keys()))

    if len(problem_foods) > 0:
        for food in problem_foods:
            for user in banned_foods_dict[food]:
                reason = f"There is nothing for {user} to eat."
                result = copy.deepcopy(avoid_venue_dict)
                result["name"] = venue["name"]
                result["reason"].append(reason)
                venues_food_fail.append(result)
        else:
            venues_food_pass.append(venue["name"])


    # First eliminate drinks that none of the users want to drink
    venue_drinks = [drink for drink in venue["drinks"] if drink in preferred_drinks_dict.keys()]

    for drink in venue_drinks:
        # If all users are ok with this drink, then this venue passes on drinks
        if len(preferred_drinks_dict[drink]) == len(filtered_users.keys()):
            # IF NOT ALRAEDY IN FOOD FAIL LIST
            print(f"Current drink is preferred by all users")
            venues_drink_pass.append(venue["name"])
        else:
            drinkless_users = filtered_users.keys() - preferred_drinks_dict[drink]
            print(f"These are drinkless users: {drinkless_users}")
            reason = f"There is nothing for {user} to drink."
            # IF NOT ALRAEDY IN FOOD FAIL LIST
            result = copy.deepcopy(avoid_venue_dict)
            result["name"] = venue["name"]
            result["reason"].append(reason)
            venues_drink_fail.append(result)


        



    #     drinkless_users = banned_foods_dict.keys() - venue["drinks"]
    #     print(drinkless_users)

    #     for user in drinkless_users:
            reason = f"There is nothing for {user} to drink."
            # IF NOT ALRAEDY IN FOOD FAIL LIST
            result = copy.deepcopy(avoid_venue_dict)
            result["name"] = venue["name"]
            result["reason"].append(reason)
            venues_drink_fail.append(result)


# print(venues_drink_fail)
# print("Passing venues:")
# print(set(venues_drink_pass))

            
# print("Passing venues:")
# print(set(venues_food_pass))
# print("Failing venues:")
# print(venues_food_fail)
    


#TODO - Warn user if a person entered is not in the users list
#TODO - add validation for the JSON data format, types etc.
#TODO - Add some tests (also for incorrect or no names)
# TODO - can you validate the input files against a schema?
# TODO - Are there any errors in the input files?
#TODO - add a help script
