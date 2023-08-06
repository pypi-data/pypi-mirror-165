from . import text

def ErrorBox(error: Exception) -> None:
    '''Shows the type and message of an error on the console.
    
    error paramter must be an instance of Exception class or one of its sub-classes.'''
    
    # Checking whether error is an exception...
    try:
        if not issubclass(error.__class__ ,Exception):
            raise TypeError()
    except:
        raise TypeError()
    
    # Getting error type...
    error_type = ''
    if hasattr(error, '__module__'):
        error_type = error.__module__ + '.'
    error_type += error.__class__.__name__
    
    # Getting error message...
    error_msg  = str(error)

    sqz_msg_iter = text.squeeze_text_iter(error_msg, 56)

    print()
    # Drawing a box using unicode box-drawing characters & printing the type of the error inside it...
    print(' ' * 10, '┌', '─' * 58, '┐', sep='')
    print(' ' * 10, '│ ', sep='', end='')
    print(f'{error_type:<56}', end='')
    print(' │')
    print(' ' * 10, '├', '─' * 58, '┤', sep='')
    # Printing the message of the error...
    print(' ' * 10, '│', ' ' * 58, '│', sep='')
    for line in sqz_msg_iter:
        print(' ' * 10, '│ ', f'{line:<56}', ' │', sep='')
    print(' ' * 10, '│', ' ' * 58, '│', sep='')
    print(' ' * 10, '└', '─' * 58, '┘', sep='')