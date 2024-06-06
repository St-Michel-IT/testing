from behave import given, when, then

from witness_number import WitnessNumber


# Given my witness number is 10
@given("my witness number is {witness_number:d}")
def step_impl(context, witness_number):
    context.witness_number = WitnessNumber(witness_number)


# When I ask the witness if 747 is a prime number
@when("I ask the witness if {number_under_test:d} is a prime number")
def step_impl(context, number_under_test):
    context.witness_number.set_witness_of(number_under_test)


# Then the witness should say "No"
@then('the witness should say "{answer}"')
def step_impl(context, answer):
    if answer == "Yes":
        assert context.witness_number.is_prime() is True
    elif answer == "No":
        assert context.witness_number.is_prime() is False
    elif answer == "I cannot be a witness":
        assert context.fail_to_instantiate is True
    else:
        raise ValueError("Unknown answer %s" % answer)


@given("my witness is {value_to_instantiate:d}")
def step_impl(context, value_to_instantiate):
    context.value_to_instantiate = value_to_instantiate


# When I instantiate the witness
@when("I instantiate the witness")
def step_impl(context):
    try:
        context.witness_number = WitnessNumber(context.value_to_instantiate)
        context.fail_to_instantiate = False
    except ValueError as e:
        context.fail_to_instantiate = True
