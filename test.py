import pytest 

from main import(
    validate_args,
    filter_users_by_name,
    create_banned_foods_dict
)


@pytest.mark.parametrize(
    "acceptable_args, actual_args, expected_output",
    [(["sarah", "david", "max"], ['max', 'sarah'], ['max', 'sarah']),
    (["sarah", "david", "max"], ['everyone'], ["sarah", "david", "max"])
    ])
def test_validate_args_pass(acceptable_args, actual_args, expected_output):
    args = validate_args(acceptable_args, actual_args)
    assert args == expected_output


@pytest.mark.parametrize(
    "acceptable_args, actual_args",
    [(["sarah", "david", "max"], ['']),
    (["sarah", "david", "max"], ['jeff']),
    (["sarah", "david", "max"], ['-']),
     (["sarah", "david", "max"], [])
    ])
def test_validate_args_fail(acceptable_args, actual_args):

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            args = validate_args(acceptable_args, actual_args)
    assert pytest_wrapped_e.type == SystemExit


@pytest.mark.parametrize(
    "names, users, expected_output",
    [(["sarah", "max"], 
    [{"name":"sarah", "wont_eat": ["pies"], "drinks": ["everything"]},{"name":"david", "wont_eat": ["mango"], "drinks": ["cola"]}, { "name":"max", "wont_eat": ["crab"], "drinks": ["tea"]}],
     {"max":{"wont_eat": ["crab"], "drinks": ["tea"]}, "sarah": {"wont_eat": ["pies"], "drinks": ["everything"]}})
    ])
def test_filter_users_by_name_pass(names, users, expected_output):
    filtered_users = filter_users_by_name(names, users)
    assert filtered_users == expected_output



# @pytest.mark.parametrize(
#     "desired_key, desired_value, args, all_users, filtered_users, expected_output",

#     [(
#     ["wont_eat"], 
#     ["name"], 
#     ["sarah", "max"], 

#     [{"name":"sarah", "wont_eat": ["pies"], "drinks": ["everything"]},{"name":"david", "wont_eat": ["mango"], "drinks": ["cola"]}, { "name":"max", "wont_eat": ["crab"], "drinks": ["tea"]}],

#     {"max":{"wont_eat": ["crab"], "drinks": ["tea"]}, "sarah": {"wont_eat": ["pies"], "drinks": ["everything"]}},

#     {"crab": ["max"],
#     "pies": ["sarah"]}  )]
#     )
# def test_create_banned_foods_dict(desired_key, desired_value, args, all_users, filtered_users, expected_output):

#     banned_foods_dict = create_banned_foods_dict(desired_key, desired_value, args, all_users, filtered_users)

#     assert banned_foods_dict == expected_output



# @pytest.mark.parametrize(
#     "desired_key, desired_value, args, all_users, filtered_users, expected_output",

#     [(
#     ["wont_eat"], 
#     ["name"], 
#     ["sarah", "max"], 

#     [{"name":"sarah", "wont_eat": ["pies"], "drinks": ["everything"]},{"name":"david", "wont_eat": ["mango"], "drinks": ["cola"]}, { "name":"max", "wont_eat": ["crab"], "drinks": ["tea"]}],

#     {"max":{"wont_eat": ["crab"], "drinks": ["tea"]}, "sarah": {"wont_eat": ["pies"], "drinks": ["everything"]}},

#     {"crab": ["max"],
#     "pies": ["sarah"]}  )]
#     )
# def test_create_banned_foods_dict(desired_key, desired_value, args, all_users, filtered_users, expected_output):

#     banned_foods_dict = create_banned_foods_dict(desired_key, desired_value, args, all_users, filtered_users)

#     assert banned_foods_dict == expected_output



evaluate_venues_for_suitability




create_response


