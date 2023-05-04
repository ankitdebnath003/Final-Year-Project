"""
This function is used to divide the message into two parts, both having alternative
characters and return both the string.
"""
def splitMessage(msg):
    characters = list(msg)
    # Storing the alternative characters.
    firstMsg = characters[::2]
    secondMsg = characters[1::2]

    # Creating string from the list and return it.
    return '' . join(firstMsg), '' . join(secondMsg)

"""
This function is used to join the divided message.
"""
def joinMessage(firstMsg, secondMsg):
    msg = [char1 + char2 for char1, char2 in zip(firstMsg, secondMsg)]

    # Add the remaining elements from the list.
    if len(firstMsg) > len(secondMsg):
        msg.extend(firstMsg[len(secondMsg):])
    elif len(secondMsg) > len(firstMsg):
        msg.extend(secondMsg[len(firstMsg):])

    return '' . join(msg)