import pytest

from main import (
    validate_args,
    filter_users_by_name,
    evaluate_venues_for_food_suitability,
    evaluate_venues_for_drink_suitability,
)


@pytest.mark.parametrize(
    "acceptable_args, actual_args, expected_output",
    [
        (["sarah", "david", "max"], ["max", "sarah"], ["max", "sarah"]),
        (["sarah", "david", "max"], ["everyone"], ["sarah", "david", "max"]),
    ],
)
def test_validate_args_pass(acceptable_args, actual_args, expected_output):
    args = validate_args(acceptable_args, actual_args)
    assert args == expected_output


@pytest.mark.parametrize(
    "acceptable_args, actual_args",
    [
        (["sarah", "david", "max"], [""]),
        (["sarah", "david", "max"], ["jeff"]),
        (["sarah", "david", "max"], ["-"]),
        (["sarah", "david", "max"], []),
    ],
)
def test_validate_args_fail(acceptable_args, actual_args):

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = validate_args(acceptable_args, actual_args)
    assert pytest_wrapped_e.type == SystemExit


@pytest.mark.parametrize(
    "names, users, expected_output",
    [
        (
            ["sarah", "max"],
            [
                {"name": "sarah", "wont_eat": ["pies"], "drinks": ["everything"]},
                {"name": "david", "wont_eat": ["mango"], "drinks": ["cola"]},
                {"name": "max", "wont_eat": ["crab"], "drinks": ["tea"]},
            ],
            {
                "max": {"wont_eat": ["crab"], "drinks": ["tea"]},
                "sarah": {"wont_eat": ["pies"], "drinks": ["everything"]},
            },
        )
    ],
)
def test_filter_users_by_name_pass(names, users, expected_output):
    filtered_users = filter_users_by_name(names, users)
    assert filtered_users == expected_output


@pytest.mark.parametrize(
    "banned_foods_dict, all_venues, failing_venues_dict, filtered_users, expected_failing_venues_dict, expected_venues_pass_food",
    [
        (
            {
                "fish": ["Danielle Ren"],
                "bread": ["Karol Drewno"],
                "pasta": ["Karol Drewno"],
            },
            [
                {
                    "name": "El Cantina",
                    "food": ["mexican"],
                    "drinks": ["soft drinks", "tequila", "beer"],
                },
                {
                    "name": "Spice of life",
                    "food": ["eggs", "meat", "fish", "pasta", "dairy"],
                    "drinks": [
                        "vodka",
                        "gin",
                        "whisky",
                        "rum",
                        "cider",
                        "beer",
                        "soft drinks",
                    ],
                },
                {
                    "name": "Spirit House",
                    "food": ["nuts", "cheese", "fruit"],
                    "drinks": ["vodka", "gin", "rum", "tequila"],
                },
            ],
            {},
            {
                "Danielle Ren": {
                    "wont_eat": ["fish"],
                    "drinks": ["cider", "rum", "soft drinks"],
                },
                "Karol Drewno": {
                    "wont_eat": ["bread", "pasta"],
                    "drinks": ["vodka", "gin", "whisky", "rum"],
                },
            },
            {},
            ["El Cantina", "Spice of life", "Spirit House"],
        )
    ],
)
def test_evaluate_venues_for_food_suitability_pass(
    banned_foods_dict,
    all_venues,
    failing_venues_dict,
    filtered_users,
    expected_failing_venues_dict,
    expected_venues_pass_food,
):

    (
        failing_venues_reasons_dict,
        venues_passing_food,
    ) = evaluate_venues_for_food_suitability(
        banned_foods_dict, all_venues, failing_venues_dict, filtered_users
    )

    assert failing_venues_reasons_dict == expected_failing_venues_dict
    assert venues_passing_food == expected_venues_pass_food


@pytest.mark.parametrize(
    "preferred_drinks_dict, all_venues, failing_venues_dict, filtered_users, expected_failing_venues_dict, expected_venues_pass_drink",
    [
        (
            {
                "cider": ["Danielle Ren"],
                "rum": ["Danielle Ren", "Karol Drewno"],
                "soft drinks": ["Danielle Ren"],
                "vodka": ["Karol Drewno"],
                "gin": ["Karol Drewno"],
                "whisky": ["Karol Drewno"],
            },
            [
                {
                    "name": "El Cantina",
                    "food": ["mexican"],
                    "drinks": ["soft drinks", "tequila", "beer"],
                },
                {
                    "name": "Spice of life",
                    "food": ["eggs", "meat", "fish", "pasta", "dairy"],
                    "drinks": [
                        "vodka",
                        "gin",
                        "whisky",
                        "rum",
                        "cider",
                        "beer",
                        "soft drinks",
                    ],
                },
                {
                    "name": "Spirit House",
                    "food": ["nuts", "cheese", "fruit"],
                    "drinks": ["vodka", "gin", "rum", "tequila"],
                },
            ],
            {},
            {
                "Danielle Ren": {
                    "wont_eat": ["fish"],
                    "drinks": ["cider", "rum", "soft drinks"],
                },
                "Karol Drewno": {
                    "wont_eat": ["bread", "pasta"],
                    "drinks": ["vodka", "gin", "whisky", "rum"],
                },
            },
            {"El Cantina": ["There is nothing for Karol Drewno to drink."]},
            ["Spice of life", "Spirit House"],
        )
    ],
)
def test_evaluate_venues_for_drink_suitability_pass(
    preferred_drinks_dict,
    all_venues,
    failing_venues_dict,
    filtered_users,
    expected_failing_venues_dict,
    expected_venues_pass_drink,
):

    (
        failing_venues_reasons_dict,
        venues_passing_drink,
    ) = evaluate_venues_for_drink_suitability(
        preferred_drinks_dict, all_venues, failing_venues_dict, filtered_users
    )

    assert failing_venues_reasons_dict == expected_failing_venues_dict
    assert venues_passing_drink == expected_venues_pass_drink


@pytest.mark.parametrize(
    "preferred_drinks_dict, banned_foods_dict, all_venues, failing_venues_dict, filtered_users, expected_failing_venues_dict",
    [
        (
            {
                "cider": ["Danielle Ren", "Wen Li"],
                "rum": ["Danielle Ren", "Karol Drewno", "Wen Li"],
                "soft drinks": ["Danielle Ren"],
                "vodka": ["Karol Drewno"],
                "gin": ["Karol Drewno"],
                "whisky": ["Karol Drewno"],
                "beer": ["Wen Li"],
            },
            {
                "fish": ["Danielle Ren"],
                "bread": ["Karol Drewno"],
                "pasta": ["Karol Drewno"],
                "chinese": ["Wen Li"],
            },
            [
                {
                    "name": "El Cantina",
                    "food": ["mexican"],
                    "drinks": ["soft drinks", "tequila", "beer"],
                },
                {
                    "name": "Spice of life",
                    "food": ["eggs", "meat", "fish", "pasta", "dairy"],
                    "drinks": [
                        "vodka",
                        "gin",
                        "whisky",
                        "rum",
                        "cider",
                        "beer",
                        "soft drinks",
                    ],
                },
                {
                    "name": "Spirit House",
                    "food": ["nuts", "cheese", "fruit"],
                    "drinks": ["vodka", "gin", "rum", "tequila"],
                },
                {
                    "name": "Tally Joe",
                    "food": ["fish", "meat", "salad", "deserts"],
                    "drinks": ["beer", "cider", "soft drinks", "sake"],
                },
                {
                    "name": "Fabrique",
                    "food": ["bread", "cheese", "deli"],
                    "drinks": ["soft drinks", "tea", "coffee"],
                },
            ],
            {},
            {
                "Danielle Ren": {
                    "wont_eat": ["fish"],
                    "drinks": ["cider", "rum", "soft drinks"],
                },
                "Karol Drewno": {
                    "wont_eat": ["bread", "pasta"],
                    "drinks": ["vodka", "gin", "whisky", "rum"],
                },
                "Wen Li": {"wont_eat": ["chinese"], "drinks": ["beer", "cider", "rum"]},
            },
            {
                "El Cantina": ["There is nothing for Karol Drewno to drink."],
                "Tally Joe": ["There is nothing for Karol Drewno to drink."],
                "Fabrique": [
                    "There is nothing for Karol Drewno to drink.",
                    "There is nothing for Wen Li to drink.",
                ],
            },
        )
    ],
)
def test_combined_evaluate_venues_for_drink_and_food_suitability_pass(
    preferred_drinks_dict,
    banned_foods_dict,
    all_venues,
    failing_venues_dict,
    filtered_users,
    expected_failing_venues_dict,
):

    failing_venues_reasons_dict, _ = evaluate_venues_for_drink_suitability(
        preferred_drinks_dict, all_venues, failing_venues_dict, filtered_users
    )

    failing_venues_reasons_dict, _ = evaluate_venues_for_food_suitability(
        banned_foods_dict, all_venues, failing_venues_dict, filtered_users
    )

    assert failing_venues_reasons_dict == expected_failing_venues_dict
