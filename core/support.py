


def to_camelcase(string):
    "snake_case --> camelCase"
    return ''.join(
        [
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(
                string.split('_')
            )
        ]
    )


def to_snakecase(string):
    "--> snake_case"
    return string.lower().replace(' ', '_').replace('-', '_')