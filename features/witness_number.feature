Feature: Witness Number

  Scenario: The number under test is not a prime number
    Given my witness number is 23
    When I ask the witness if 747 is a prime number
    Then the witness should say "No"

  Scenario: The number under test is a prime number
    Given my witness number is 10
    When I ask the witness if 91 is a prime number
    Then the witness should say "Yes"

  Scenario Outline: The witness number cannot be a 1 or inferior
    Given my witness is <number>
    When I instantiate the witness
    Then the witness should say "I cannot be a witness"


    Examples:
      | number |
      | -1     |
      | 0      |
      | -10000 |
      | -2     |