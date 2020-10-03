import json
import sys
import getopt
import copy
from itertools import chain
from typing import Dict, List, Any


#TODO - Docstrings

def retrieve_json_from_file(file_path:str ) -> List[Dict]:
    """
    """
    try:
        with open(file_path, "r") as inputs:
            data = json.load(inputs)
            inputs.close()
            return data
    except IOError as e:
        print(f"Unable to read file at path {file_path}: {e}")


def validate_args(acceptable_args: List[str], actual_args: List[str]) -> List[str]:
    """
    """
    for arg in actual_args:
        arg = arg.strip()
        if arg == "everyone":
            print("You're taking the whole team!")
            break
        if arg not in acceptable_args:
            print(f"Sorry, this is not a valid user. You can choose from: {acceptable_args}")
            sys.exit(2)
        print("Yep, accepted")
        return actual_args


def filter_users_by_name(names: List[str], users: Dict[str, Any]) -> Dict[str, Any]:
    """
    """
    # Remove users who not present in the specified args
    filtered_users = {user["name"]: {"wont_eat": user["wont_eat"], "drinks": user["drinks"]} for user in users if user["name"] in names}
    return filtered_users


#TODO - These could probably be the same function - just think about variable naming

def create_banned_foods_dict(desired_key: str, desired_value: str, args: Dict[str, Any], all_users: Dict[str, Any], filtered_users: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    """
    banned_foods = [[food for food in user[desired_key]] for user in all_users if user["name"] in args] 
    banned_foods_flattened = list(chain.from_iterable(banned_foods))

    # Create dict to map banned foods to team members
    banned_foods_dict = {food: [] for food in banned_foods_flattened}

    for user, details in filtered_users.items():
        for food in details["wont_eat"]:
            if food in banned_foods_flattened:
                banned_foods_dict[food].append(user)

    return banned_foods_dict



def create_preferred_drinks_dict(desired_key: str, desired_value: str, args: Dict[str, Any], all_users: Dict[str, Any], filtered_users: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    """
    preferred_drinks = [[drink for drink in user["drinks"]] for user in all_users if user["name"] in args] 
    preferred_drinks_flattened = list(chain.from_iterable(preferred_drinks))

    # Create dict to map drink preferences to team members
    preferred_drinks_dict = {drink: [] for drink in preferred_drinks_flattened}

    for user, details in filtered_users.items():
        for drink in details["drinks"]:
            if drink in preferred_drinks_flattened:
                preferred_drinks_dict[drink].append(user)

    return preferred_drinks_dict





venues_food_pass = [] 
venues_drink_pass = [] 
venues_failing = []
# Filter venues by foods first
for venue in all_venues:

    venue_result = copy.deepcopy(avoid_venue_dict)

    problem_foods = list(set(venue["food"]) & set(banned_foods_dict.keys()))

    if len(problem_foods) > 0:
        for food in problem_foods:
            for user in banned_foods_dict[food]:
                reason = f"There is nothing for {user} to eat."
                venue_result["name"] = venue["name"]
                venue_result["reason"].append(reason)
        else:
            venues_food_pass.append(venue["name"])


#     # First eliminate drinks that none of the users want to drink
#     venue_drinks = [drink for drink in venue["drinks"] if drink in preferred_drinks_dict.keys()]

#     for drink in venue_drinks:
#         # If all users are ok with this drink, then this venue passes on drinks
#         if len(preferred_drinks_dict[drink]) == len(filtered_users.keys()):
#             # IF NOT ALRAEDY IN FOOD FAIL LIST
#             venues_drink_pass.append(venue["name"])
#         else:
#             drinkless_users = filtered_users.keys() - preferred_drinks_dict[drink]
#             reason = f"There is nothing for {user} to drink."
#             # IF NOT ALRAEDY IN FOOD FAIL LIST
#             result = copy.deepcopy(avoid_venue_dict)
#             venue_result["name"] = venue["name"]
#             venue_result["reason"].append(reason)

#     venues_failing.append(venue_result)


# #passing_venues = venues_drink_pass.intersection(venues_food_pass)
# passing_venues = list(set(venues_drink_pass) & set(venues_food_pass))
# print(passing_venues)


# print("Failing venues:")
# print(venues_failing)
# # print("Passing venues on drink:")
# # print(set(venues_drink_pass))           
# # print("Passing venues on food:")
# # print(set(venues_food_pass))

    
# #TODO - Warn user if a person entered is not in the users list
# #TODO - add validation for the JSON data format, types etc.
# #TODO - Add some tests (also for incorrect or no names)
# # TODO - can you validate the input files against a schema?
# # TODO - Are there any errors in the input files?
# #TODO - add a help script
# #TODO - Add main function

if __name__ == "__main__":

    all_users = retrieve_json_from_file("./data/users.json")

    all_venues = retrieve_json_from_file("./data/venues.json")

    user_names = [user["name"] for user in all_users]

    args = sys.argv[1:]

    args = validate_args(user_names, args)

    filtered_users = filter_users_by_name(args, all_users)

    print(filtered_users)

    banned_foods_dict = create_banned_foods_dict("wont_eat", "name", args, all_users, filtered_users)
    print(banned_foods_dict)

    preferred_drinks_dict = create_preferred_drinks_dict("drinks", "name", args, all_users, filtered_users)
    print(preferred_drinks_dict)


    venues_response = {"places_to_visit": [],
                    "places_to_avoid":[]}

    avoid_venue_dict = {
        "name": "",
        "reason": []
    }


    print("Done.")