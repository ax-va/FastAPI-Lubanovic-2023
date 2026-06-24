from typing import Annotated

from pydantic import BaseModel, StringConstraints  # See also `Field`


class Creature(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=2,  # at least two characters long
        )
    ]
    country: str
    area: str
    description: str
    aka: str


if __name__ == "__main__":
    thing = Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )
    print("Name is", thing.name)

