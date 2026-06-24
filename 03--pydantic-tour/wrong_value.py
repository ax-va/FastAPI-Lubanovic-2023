from model import Creature

dragon = Creature(
    name=" !",
    description="some creature",
    country="*" ,
    area="*",
    aka="firedrake",
)

# Run the script
"""
...
pydantic_core._pydantic_core.ValidationError: 1 validation error for Creature
name
  String should have at least 2 characters [type=string_too_short, input_value=' !', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_short
"""
