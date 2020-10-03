import json
import sys
import getopt
import copy
from itertools import chain
from typing import Dict, List, Any, Tuple


#TODO - Docstrings


def clean_input(input_dict: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    for key in keys:
        clean_values = [value.lower() for value in input_dict[key] if value is not '']
        input_dict[key] = clean_values
    return input_dict


def retrieve_json_from_file(file_path:str, food_key: str) -> List[Dict]:
    """
    """
    try:
        with open(file_path, "r") as inputs:
            data = json.load(inputs)
            # Lower case all food and drink names for consistency
            clean_data = []
            for row in data:
                row = clean_input(row, ["drinks", food_key])
                clean_data.append(row)
            inputs.close()
            return clean_data
    except IOError as e:
        print(f"Unable to read file at path {file_path}: {e}")


def validate_args(acceptable_args: List[str], actual_args: List[str]) -> List[str]:
    """
    """    
    if len(actual_args) == 0:
        print(f"You must enter valid users to find venues for. Choose from: {acceptable_args} or type 'everyone' to take the whole team!")
        sys.exit(2)
    for arg in actual_args:
        arg = arg.strip()
        if arg == "everyone":
            actual_args = acceptable_args
            return actual_args
        if len(arg) == 0 or arg not in acceptable_args:
            print(f"Sorry, {arg} is not a valid user. Choose from: {acceptable_args} or type 'everyone' to take the whole team!")
            sys.exit(2)
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


def evaluate_venues_for_food_suitability(banned_foods_dict: Dict[str, List[str]], all_venues: Dict[str, Any], failing_venues_reasons_dict: Dict[str, Any], filtered_users: Dict[str, Any]) -> Tuple[List[Dict], List[str], List[str]]:
    """
    """
    venues_food_pass = [] 

    # Filter venues by foods first
    for venue in all_venues:

        # Foods from the venue left over after subtracting the banned foods
        acceptable_foods = [food for food in venue["food"] if food not in banned_foods_dict.keys()]
    
        if len(acceptable_foods) == 0:
            for food in acceptable_foods:
                for user in banned_foods_dict[food]:
                    reason = f"There is nothing for {user} to eat."
                    if venue["name"] not in failing_venues_reasons_dict.keys():
                        failing_venues_reasons_dict[venue["name"]] = []
                    if reason not in failing_venues_reasons_dict[venue["name"]]:
                        failing_venues_reasons_dict[venue["name"]].append(reason)
        else:
            venues_food_pass.append(venue["name"])

    return failing_venues_reasons_dict, venues_food_pass
                


def evaluate_venues_for_drink_suitability(preferred_drinks_dict: Dict[str, Any], all_venues: Dict[str, Any], failing_venues_reasons_dict: Dict[str, Any], filtered_users: Dict[str, Any]):
    """
    """
    venues_drink_pass = []

    for venue in all_venues:

        # First eliminate drinks that none of the users want to drink
        venue_drinks = [drink for drink in venue["drinks"] if drink in preferred_drinks_dict.keys()]

        names = []
        for drink in venue_drinks:
            # Users happy with this venue's drinks - collect their names up
            names.append(preferred_drinks_dict[drink])
        # Is everyone accounted for in the 'happy with this venue's drinks' list?
        names_flattened = set(list(chain.from_iterable(names)))

        if len(names_flattened) == len(filtered_users.keys()):
            venues_drink_pass.append(venue["name"])
        else:
            drinkless_users = filtered_users.keys() - names_flattened
            for user in drinkless_users:
                reason = f"There is nothing for {user} to drink."
                if venue["name"] not in failing_venues_reasons_dict.keys():
                        failing_venues_reasons_dict[venue["name"]] = []
                if reason not in failing_venues_reasons_dict[venue["name"]]:
                    failing_venues_reasons_dict[venue["name"]].append(reason)

    return failing_venues_reasons_dict, venues_drink_pass



def create_response(venues_passing_food: List[str], venues_passing_drink: List[str], failing_venues: List[Dict[str, Any]]) -> json:
    """
    """
    passing_venues = list(set(venues_passing_food) & set(venues_passing_drink))

    failures = []
    for venue, reasons in failing_venues.items():
        failures.append({
            "name" :venue,
            "reasons": reasons 
        })

    venues_response = {"places_to_visit": passing_venues,
                    "places_to_avoid": failures}

    venues_response_json = json.dumps(venues_response)

    return venues_response

    
# #TODO - add validation for the JSON data format, types etc.
# # TODO - can you validate the input files against a schema?
# # TODO - Are there any errors in the input files?
# #TODO - add a help script
# TODO - Chcek consistency of var names e.g. for dicts

if __name__ == "__main__":

    all_users = retrieve_json_from_file("./data/users.json", "wont_eat")

    all_venues = retrieve_json_from_file("./data/venues.json", "food")

    # print(all_venues)

    user_names = [user["name"] for user in all_users]

    args = sys.argv[1:]

    args = validate_args(user_names, args)

    filtered_users = filter_users_by_name(args, all_users)

    print(filtered_users)

    banned_foods_dict = create_banned_foods_dict("wont_eat", "name", args, all_users, filtered_users)

    # print("Banned foods:")
    print(banned_foods_dict)

    preferred_drinks_dict = create_preferred_drinks_dict("drinks", "name", args, all_users, filtered_users)

    # print("preferred drinks:")
    print(preferred_drinks_dict)

    failing_venues_reasons_dict = {}

    # failing_venues, venues_drinks_pass, venues_food_pass = 
    failing_venues_reasons_dict, venues_passing_food = evaluate_venues_for_food_suitability(banned_foods_dict, all_venues, failing_venues_reasons_dict, filtered_users)

    # print(failing_venues_reasons_dict)
    # print(venues_passing_food)

    failing_venues_reasons_dict, venues_passing_drink = evaluate_venues_for_drink_suitability(preferred_drinks_dict, all_venues, failing_venues_reasons_dict, filtered_users)


    print(failing_venues_reasons_dict)
    print(venues_passing_drink)
    # print(venues_passing_food)


    response = create_response(venues_passing_food, venues_passing_drink, failing_venues_reasons_dict)

    # print(json.dumps(response, indent=3))

