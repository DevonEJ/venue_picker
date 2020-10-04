import json
import sys
import getopt
import copy
from itertools import chain
from typing import Dict, List, Any, Tuple


def clean_input(
    input_dict: Dict[str, List[str]], keys: List[str]
) -> Dict[str, List[str]]:
    """Given a dictionary and a list of dictionary keys, function lower cases
    dictionary values (which should be lists of strings) corresponding to those keys.

    Args:
        input_dict (Dict[str, List[str]]): Dictionary with list values requiring lower-casing.
        keys (List[str]): List of keys corresponding to list values requiring lower-casing.

    Returns:
        Dict[str, List[str]]: Cleaned dictionary.
    """
    for key in keys:
        clean_values = [value.lower() for value in input_dict[key] if value is not ""]
        input_dict[key] = clean_values
    return input_dict


def retrieve_json_from_file(
    file_path: str, keys: List[str], expected_record_count: int
) -> List[Dict]:
    """Reads list of JSON objects into a list of dictionaries, and applies lower casing and record
    count checks.

    Args:
        file_path (str): File path for JSON.
        keys (List[str]): List of keys in resulting dict requiring lower-casing.
        expected_record_count (int): Expected records.

    Returns:
        List[Dict]: List of dictionaries.
    """
    try:
        with open(file_path, "r") as inputs:
            data = json.load(inputs)
            # Lower case all food and drink names for consistency
            clean_data = []
            for row in data:
                row = clean_input(row, keys)
                clean_data.append(row)
            inputs.close()
            # Check record count against expected
            assert (
                len(clean_data) == expected_record_count
            ), f"Got {len(clean_data)} records, expected {expected_record_count}"
            return clean_data
    # Catch exceptions with data validation, or reading from input files
    except Exception as e:
        print(f"An error occurred reading file at file path {file_path}: {e}")
        sys.exit(2)


def validate_args(acceptable_args: List[str], actual_args: List[str]) -> List[str]:
    """Validates that the command line arguments used to run the programme contain valid user
    names, against a list of acceptable options. Provides error message if not validated.

    Args:
        acceptable_args (List[str]): List of valid user name options to check against.
        actual_args (List[str]): Args received when programme is run.

    Returns:
        List[str]: Validated args.
    """
    #  If no args provided, print error prompt and exit
    if len(actual_args) == 0:
        print(
            f"You must enter valid users to find venues for. Choose from: {acceptable_args} or\
             type 'everyone' to take the whole team - don't forget the single quotes!"
        )
        sys.exit(2)
    for arg in actual_args:
        arg = arg.strip()
        # If 'everyone' given as arg, include all possible users
        if arg == "everyone":
            actual_args = acceptable_args
            return actual_args
        # If arg is empty, or an invalid arg provided, print error prompt and exit
        if len(arg) == 0 or arg not in acceptable_args:
            print(
                f"Sorry, that is not a valid user. Choose from: {acceptable_args} or type\
                 'everyone' to take the whole team - don't forget the single quotes!"
            )
            sys.exit(2)
        return actual_args


def filter_users_by_name(
    names: List[str], users: List[Dict[str, Any]]
) -> Dict[str, Dict]:
    """Filters users dictionary to only include those users named in the names argument,
    and re-formats the dict into a shallower structure, with user names as keys.

    Args:
        names (List[str]): List of valid user names to filter on.
        users (List[Dict[str, Any]]): List of dictionaries with user details in them.

    Returns:
        Dict[str, Dict]: Dictionary of filtered users and their details.
    """
    # Remove users who not present in the specified args, and convert list of dicts to single dict
    filtered_users = {
        user["name"]: {"wont_eat": user["wont_eat"], "drinks": user["drinks"]}
        for user in users
        if user["name"] in names
    }
    return filtered_users


def create_banned_foods_dict(
    desired_key: str,
    args: List[str],
    all_users: List[Dict[str, Any]],
    filtered_users: Dict[str, Any],
) -> Dict[str, List[str]]:
    """Invert users dictionary to have foods as keys mapped to user's names.

    Args:
        desired_key (str): Value in input user dictionary that will become dictionary
        key in output dictionary.
        args (List[str]): List of user names to include in output.
        all_users (List[Dict[str, Any]]): List of dictionaries for all users.
        filtered_users (Dict[str, Any]): Dictionary with only selected users.

    Returns:
        Dict[str, List[str]]: Dictionary of banned foods: users banning them.
    """
    # Get foods banned by all relevant users as a single list
    banned_foods = [
        [food for food in user[desired_key]]
        for user in all_users
        if user["name"] in args
    ]
    banned_foods_flattened = list(chain.from_iterable(banned_foods))

    # Create dict to map banned foods to team members
    banned_foods_dict = {food: [] for food in banned_foods_flattened}

    for user, details in filtered_users.items():
        for food in details["wont_eat"]:
            if food in banned_foods_flattened:
                banned_foods_dict[food].append(user)

    return banned_foods_dict


def create_preferred_drinks_dict(
    desired_key: str,
    args: Dict[str, Any],
    all_users: List[Dict[str, Any]],
    filtered_users: Dict[str, Any],
) -> Dict[str, List[str]]:
    """Invert users dictionary to have drinks as keys mapped to user's names.

    Args:
        desired_key (str): Value in input user dictionary that will become dictionary
        key in output dictionary.
        args (List[str]): List of user names to include in output.
        all_users (List[Dict[str, Any]]): List of dictionaries for all users.
        filtered_users (Dict[str, Any]): Dictionary with only selected users.

    Returns:
        Dict[str, List[str]]: Dictionary of preferred drinks: users preferring them.
    """
    # Get drinks preferred by all relevant users as a single list
    preferred_drinks = [
        [drink for drink in user["drinks"]]
        for user in all_users
        if user["name"] in args
    ]
    preferred_drinks_flattened = list(chain.from_iterable(preferred_drinks))

    # Create dict to map drink preferences to team members
    preferred_drinks_dict = {drink: [] for drink in preferred_drinks_flattened}

    for user, details in filtered_users.items():
        for drink in details["drinks"]:
            if drink in preferred_drinks_flattened:
                preferred_drinks_dict[drink].append(user)

    return preferred_drinks_dict


def evaluate_venues_for_food_suitability(
    banned_foods_dict: Dict[str, List[str]],
    all_venues: List[Dict[str, Any]],
    failing_venues_reasons_dict: Dict[str, Any],
    filtered_users: Dict[str, Any],
) -> Tuple[List[Dict], List[str]]:
    """For each venue, checks if there are foods left to eat there after subtracting
    the banned foods for all relevant users. Outputs results of this evaluation.

    Args:
        banned_foods_dict (Dict[str, List[str]]): Dictionary mapping banned foods to users banning them.
        all_venues (List[Dict[str, Any]]): Dictionary of all available venues.
        failing_venues_reasons_dict (Dict[str, Any]): Dictionary to hold failing venues and their reasons.
        filtered_users (Dict[str, Any]): Dictionary of only relevant users.

    Returns:
        Tuple[List[Dict], List[str]]: Outputs List of passing venues, and Dict of failing venues with
        reasons.
    """
    venues_food_pass = []
    for venue in all_venues:

        # Get list of foods available from current venue left over after subtracting the banned foods
        acceptable_foods = [
            food for food in venue["food"] if food not in list(banned_foods_dict.keys())
        ]
        # If no acceptable foods left after filtering, create reason and mark venue as failing on food
        if len(acceptable_foods) == 0:
            for food in venue["food"]:
                for user in banned_foods_dict[food]:
                    reason = f"There is nothing for {user} to eat."
                    if venue["name"] not in list(failing_venues_reasons_dict.keys()):
                        failing_venues_reasons_dict[venue["name"]] = []
                    if reason not in failing_venues_reasons_dict[venue["name"]]:
                        failing_venues_reasons_dict[venue["name"]].append(reason)
        # Otherwise, mark venue as passing on food
        else:
            venues_food_pass.append(venue["name"])

    return failing_venues_reasons_dict, venues_food_pass


def evaluate_venues_for_drink_suitability(
    preferred_drinks_dict: Dict[str, Any],
    all_venues: List[Dict[str, Any]],
    failing_venues_reasons_dict: Dict[str, Any],
    filtered_users: Dict[str, Any],
) -> Tuple[List[Dict], List[str]]:
    """For each venue, checks if all users will drink at least one of their drink options.
     Outputs results of this evaluation.

    Args:
        preferred_drinks_dict (Dict[str, List[str]]): Dictionary mapping preferred drinks
        to users preferrering them.
        all_venues (List[Dict[str, Any]]): Dictionary of all available venues.
        failing_venues_reasons_dict (Dict[str, Any]): Dictionary to hold failing venues and their reasons.
        filtered_users (Dict[str, Any]): Dictionary of only relevant users.

    Returns:
        Tuple[List[Dict], List[str]]: Outputs List of passing venues, and Dict of failing venues with
        reasons.
    """
    venues_drink_pass = []

    for venue in all_venues:
        # First filter out drinks that none of the users want to drink
        venue_drinks = [
            drink
            for drink in venue["drinks"]
            if drink in list(preferred_drinks_dict.keys())
        ]
        names = []
        for drink in venue_drinks:
            # Collect names of users happy with this venue's drinks options
            names.append(preferred_drinks_dict[drink])
        names_flattened = set(list(chain.from_iterable(names)))
        # If all relevant users are present in the list of names, then everyone is happy with
        # venue's drinks options - mark venue as passed on drinks
        if len(names_flattened) == len(list(filtered_users.keys())):
            venues_drink_pass.append(venue["name"])
        # Otherwise, if we have drinkless users - create reason and mark venue as failed
        else:
            drinkless_users = set(list(filtered_users.keys())) - names_flattened
            for user in drinkless_users:
                reason = f"There is nothing for {user} to drink."
                if venue["name"] not in list(failing_venues_reasons_dict.keys()):
                    failing_venues_reasons_dict[venue["name"]] = []
                if reason not in failing_venues_reasons_dict[venue["name"]]:
                    failing_venues_reasons_dict[venue["name"]].append(reason)

    return failing_venues_reasons_dict, venues_drink_pass


def create_response(
    venues_passing_food: List[str],
    venues_passing_drink: List[str],
    failing_venues: List[Dict[str, Any]],
) -> json:
    """Takes the results of evaluating venues against food and drink requirements,
    and forms them into desired JSON output.

    Args:
        venues_passing_food (List[str]): Venues passing food evaluation.
        venues_passing_drink (List[str]): Venues passing drink evaluation.
        failing_venues (List[Dict[str, Any]]): Venues failing food and/or drink evaluation,
        and their reasons.

    Returns:
        json: JSON output holding all evaluation results.
    """
    # Get venues passing on both food and drink - those appearing in both lists
    passing_venues = list(set(venues_passing_food) & set(venues_passing_drink))

    failures = []
    for venue, reasons in failing_venues.items():
        failures.append({"name": venue, "reasons": reasons})

    venues_response = {"places_to_visit": passing_venues, "places_to_avoid": failures}

    venues_response_json = json.dumps(venues_response)

    return venues_response


if __name__ == "__main__":

    all_users = retrieve_json_from_file("./data/users.json", ["drinks", "wont_eat"], 7)

    all_venues = retrieve_json_from_file("./data/venues.json", ["food", "drinks"], 9)

    user_names = [user["name"] for user in all_users]

    # Get command line args, ignoring the first term (filename)
    args = sys.argv[1:]

    args = validate_args(user_names, args)

    filtered_users = filter_users_by_name(args, all_users)

    banned_foods_dict = create_banned_foods_dict(
        "wont_eat", args, all_users, filtered_users
    )

    preferred_drinks_dict = create_preferred_drinks_dict(
        "drinks", args, all_users, filtered_users
    )

    failing_venues_reasons_dict = {}

    (
        failing_venues_reasons_dict,
        venues_passing_food,
    ) = evaluate_venues_for_food_suitability(
        banned_foods_dict, all_venues, failing_venues_reasons_dict, filtered_users
    )

    (
        failing_venues_reasons_dict,
        venues_passing_drink,
    ) = evaluate_venues_for_drink_suitability(
        preferred_drinks_dict, all_venues, failing_venues_reasons_dict, filtered_users
    )

    response = create_response(
        venues_passing_food, venues_passing_drink, failing_venues_reasons_dict
    )

    # Display output
    print(json.dumps(response, indent=3))
