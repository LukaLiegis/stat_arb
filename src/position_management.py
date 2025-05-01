def manage_position(current_position, prediction, threshold, step_size, max_position):

    if prediction > threshold:

        if current_position < 1:
            new_position = min(0, current_position + step_size)
        else:
            new_position = min(max_position, current_position + step_size)

    elif prediction < -threshold:

        if current_position > 0:
            new_position = max(0, current_position - step_size)
        else:
            new_position = max(-max_position, current_position - step_size)

    else:
        new_position = current_position

    return new_position