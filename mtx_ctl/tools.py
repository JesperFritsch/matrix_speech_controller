from mtx_ctl.matrix_conn import MatrixConn

matrix_conn = MatrixConn()

def set_brightness(value: int):
    """
    Set the brightness of the screen

    sets the brightness of the screen to the specified value.

    Args:
        value (number): The brightness value to set. Must be between 0 and 100.

    Returns:
        number: The value that was set.

    Raises:
        ValueError: If the value is not between 0 and 100.
    """
    tool_response = matrix_conn.set("brightness", value)
    result = "The brightness is set to: %s" % tool_response
    print(result)
    return result

def get_brightness():
    """
    Get the current brightness of the screen

    Retrieves the current brightness value of the screen.

    Returns:
        number: The current brightness value.
    """
    tool_response = matrix_conn.get("brightness")
    result = "current brightness is %s" % tool_response
    print(result)
    return str(tool_response)

def display_on(mode: bool):
    """
    Sets the display mode for the display

    Sets the display either on or off, True for on, False for off.

    Args:
        mode (boolean): The mode to set the display to (True = on, False = off).

    Returns:
        None
    """
    tool_response = matrix_conn.set("display_on", mode)
    result = "display 'on' is set to: %s" % tool_response
    print(result)
    return result

def get_display_on():
    """
    Get the display status

    Retrieves the current status of the display (on/off).

    Returns:
        boolean: The current display status.
    """
    tool_response = matrix_conn.get("display_on")
    result = "display is %s" % ('on' if tool_response else 'off')
    print(result)
    return str(tool_response)

def set_app(app_name: str):
    """
    Set the current application

    Sets the current application to the specified application. The application must be in the list of available applications.
    run last

    Args:
        app_name (string): The name of the application to set.

    Returns:
        None
    """
    tool_response = matrix_conn.set("current_app", app_name)
    result = "current app set to: %s" % tool_response
    print(result)
    return result

def get_apps():
    """
    Get the list of available applications

    Retrieves the list of available applications for the screen.

    Returns:
        list: The list of available applications.
    """
    tool_response = matrix_conn.get("apps")
    result = "available apps are %s" % tool_response
    print(result)
    return str(tool_response)

def set_snake_count(count: int):
    """
    Set the number of snakes

    Sets the number of snakes to the specified count, usually somewhere around 1-15, but absolutely never higher than 50.

    Args:
        count (number): The number of snakes to set, normally between 1-20, but absolutely never higher than 50.

    Returns:
        None
    """
    tool_response = matrix_conn.set("nr_snakes", count)
    result = "snake count set to: %s" % tool_response
    print(result)
    return result

def get_snake_count():
    """
    Get the number of snakes

    Retrieves the current number of snakes in the simulation.

    Returns:
        number: The current number of snakes.
    """
    tool_response = matrix_conn.get("nr_snakes")
    result = "current number of snakes is %s" % tool_response
    print(result)
    return str(tool_response)

def set_snake_food(food: int):
    """
    Set the amount of food

    Sets the amount of food available to the snakes.

    Args:
        food (number): The amount of food to set.

    Returns:
        None
    """
    tool_response = matrix_conn.set("food", food)
    result = "snake food set to: %s" % tool_response
    print(result)
    return result

def get_snake_food():
    """
    Get the amount of food

    Retrieves the current amount of food available to the snakes.

    Returns:
        number: The current amount of food.
    """
    tool_response = matrix_conn.get("food")
    result = "current food amount is %s" % tool_response
    print(result)
    return str(tool_response)

def set_snake_map(map_name: str):
    """
    Set the map

    Sets the map to the specified map, there are only a few maps available. and you are provided with a list of available maps.
    you can never set a map that is not in the list of available maps.

    Args:
        map_name (string): The name of the map to set.

    Returns:
        None
    """
    tool_response = matrix_conn.set("snake_map", map_name)
    result = "map set to: %s" % tool_response
    print(result)
    return result

def get_snake_map():
    """
    Get the current map

    Retrieves the current map used in the snake simulation.

    Returns:
        string: The name of the current map.
    """
    tool_response = matrix_conn.get("snake_map")
    result = "current snake map is %s" % tool_response
    print(result)
    return str(tool_response)

def get_snake_maps():
    """
    Get the list of available maps

    Retrieves the list of available maps for the snake simulation.

    Returns:
        list: The list of available maps.
    """
    tool_response = matrix_conn.get("snake_maps")
    result = "available snake maps are %s" % tool_response
    print(result)
    return str(tool_response)

def set_snake_food_decay(decay: int):
    """
    Set the food decay rate

    Sets the decay rate of the food on the map. This value determines how fast the food will disappear. The lower the value, the faster the food will disappear.

    Args:
        decay (number): The decay rate to set.

    Returns:
        None
    """
    tool_response = matrix_conn.set("food_decay", decay)
    result = "food decay set to: %s" % tool_response
    print(result)
    return result

def get_snake_food_decay():
    """
    Get the food decay rate

    Retrieves the current decay rate of the food on the map. This value determines how fast the food will disappear. The lower the value, the faster the food will disappear.

    Returns:
        number: The current food decay rate.
    """
    tool_response = matrix_conn.get("food_decay")
    result = "current food decay rate is %s" % tool_response
    print(result)
    return str(tool_response)

def set_snakes_fps(fps: int):
    """
    Set the frames per second (FPS) for the snake simulation

    Sets the FPS for the snake simulation to the specified value. This value if usually around 1-30, but can go higher if needed.
    do not restart if you only change the FPS.

    Args:
        fps (number): The FPS value to set.

    Returns:
        None
    """
    tool_response = matrix_conn.set("snakes_fps", fps)
    result = "snake FPS set to: %s" % tool_response
    print(result)
    return result

def get_snakes_fps():
    """
    Get the frames per second (FPS) for the snake simulation

    Retrieves the current FPS for the snake simulation.

    Returns:
        number: The current FPS value.
    """
    tool_response = matrix_conn.get("snakes_fps")
    result = "current snake FPS is %s" % tool_response
    print(result)
    return str(tool_response)

def restart_snakes():
    """
    Restart the snake simulation

    Ends the current simulation and restarts it, with the same values as before the restart.
    run last

    Returns:
        None
    """
    tool_response = matrix_conn.action("restart_snakes")
    result = "snakes restarted: %s" % tool_response
    print(result)
    return result
