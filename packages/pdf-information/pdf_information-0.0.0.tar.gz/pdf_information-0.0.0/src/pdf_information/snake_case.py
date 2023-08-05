def convert_to_snake_case(  # noqa: WPS231
    convert: str,
) -> str:
    converted: list[str] = []
    last_was_space = True
    last_was_upper = False
    for character in convert:
        if character.isspace():
            last_was_space = True
            last_was_upper = False
            converted.append("_")
            continue
        if character.isupper():
            lower = character.lower()
            if not last_was_space and not last_was_upper:
                converted.append("_")
            last_was_space = False
            converted.append(lower)
            last_was_upper = True
            continue
        last_was_space = False
        last_was_upper = False
        converted.append(character)
    return "".join(converted)
