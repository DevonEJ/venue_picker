import pytest 

from main import validate_args



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


