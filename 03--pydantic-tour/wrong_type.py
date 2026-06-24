from model import Creature

dragon = Creature(
    name="dragon",
    description=["incorrect", "string", "list"],
    country="*" ,
    area="*",
    aka="firedrake",
)

# Run the script
"""
...
pydantic_core._pydantic_core.ValidationError: 1 validation error for Creature
description
  Input should be a valid string [type=string_type, input_value=['incorrect', 'string', 'list'], input_type=list]
    For further information visit https://errors.pydantic.dev/2.13/v/string_type
"""
