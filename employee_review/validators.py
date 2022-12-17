def validate_alpha_length_case(string):
    errors = check_multiple([
        check_length,
        check_first_letter_uppercase,
        check_only_letters
    ], string)
    return errors


def validate_length_case(string):
    errors = check_multiple([
        check_length,
        check_first_letter_uppercase
    ], string)
    return errors


def validate_length(string):
    errors = check_multiple([
        check_length
    ], string)
    return errors


def check_multiple(checkers, string):
    errors = []
    for checker in checkers:
        error = checker(string)
        if error:
            errors.append(error)
    return errors


def check_length(string, min_length=3):
    if len(string) < min_length:
        return 'Must be at least ' + str(min_length) + ' characters long.'
    return False


def check_first_letter_uppercase(string):
    if (string[0].islower()):
        return 'Must start with a capital letter.'
    return False


def check_only_letters(string):
    if (not string.isalpha()):
        return 'Must only contain letters.'
    return False
