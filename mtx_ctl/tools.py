


def set_brightness(value: int):
    """
    Set the brightness of the screen

    sets the brightness of the screen to the specified value.

    Args:
        value (number): The brightness value to set. Must be between 0 and 100.

    Returns:
        None

    Raises:
        ValueError: If the value is not between 0 and 100.


    """
    tool_response = f"brightness set to {value}"
    print(tool_response)
    return tool_response


def set_app(app_name: str):
    """
    Set the current application

    Sets the current application to the specified app.
    run last

    Args:
        app_name (string): The name of the application to set.

    Returns:
        None

    """
    tool_response = f"current app set to {app_name}"
    print(tool_response)
    return tool_response


def set_snake_count(count: int):
    """
    Set the number of snakes

    Sets the number of snakes to the specified count, usually somewhere around 1-15, but can go higher if needed.

    Args:
        count (number): The number of snakes to set.

    Returns:
        None

    """
    tool_response = f"snake count set to {count}"
    print(tool_response)
    return tool_response


def set_snake_food(food: int):
    """
    Set the amount of food

    Sets the amount of food available to the snakes.

    Args:
        food (number): The amount of food to set.

    Returns:
        None

    """
    tool_response = f"snake food set to {food}"
    print(tool_response)
    return tool_response


def set_snake_map(map_name: str):
    """
    Set the map

    Sets the map to the specified map.

    Args:
        map_name (string): The name of the map to set.

    Returns:
        None

    """
    tool_response = f"map set to {map_name}"
    print(tool_response)
    return tool_response


def set_snake_food_decay(decay: int):
    """
    Set the food decay rate

    Sets the decay rate of the food on the map. the lower the decay rate the faster the food will disappear.

    Args:
        decay (number): The decay rate to set.

    Returns:
        None

    """
    tool_response = f"food decay set to {decay}"
    print(tool_response)
    return tool_response

def restart_snakes():
    """
    Restart the snake simulation

    Ends the current simulation and restarts it, with the same values as before the restart.
    run last

    Returns:
        None

    """
    tool_response = "snakes restarted"
    print(tool_response)
    return tool_response
