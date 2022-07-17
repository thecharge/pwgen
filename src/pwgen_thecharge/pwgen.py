import string
import secrets
import shlex  # noqa
import sys  # noqa
from base64 import b64encode


def pwgen(
    length: int = 20,
    hasCapital: bool = True,
    hasNumbers: bool = True,
    hasSpecial: bool = False,
    hasXKCDStyle: bool = False,
    b64: bool = False,
    generate: int = 1,
):
    """
    Password Generator
    Arguments:
    length
        - the length of the password to be generated
    hasCapital
        -   the password has and should consist of
            at least 1 capital letter(s) in it
    hasNumbers
        -   the password has and should consist of
            at least 1 digit(s) in it
    hasSpecial
        -   the password has and should consist of
            at least 1 special character(s) in it
    hasXKCDStyle
        -   in addition to the defined previous properties,
            like in XKCD style, will separate the output to
            at least one occurence of space in the password,
            splitting it into "words"
    b64
        -   returning the password in encoded base64 string
            (handy for k8s secrets)
    generate
        -   to generate a list of passwords
            (if 1 - will return only one string)
    """

    if generate > 1:
        result = []
        while generate:
            result.append(
                pwgen(
                    length,
                    hasCapital,
                    hasNumbers,
                    hasSpecial,
                    hasXKCDStyle,
                    b64,
                )
            )
            generate -= 1
        return result

    alphabet = string.ascii_lowercase

    if True == hasCapital:  # noqa
        alphabet += string.ascii_uppercase

    if True == hasSpecial:  # noqa
        alphabet += string.punctuation

    if True == hasXKCDStyle:  # noqa
        alphabet += " "

    if True == hasNumbers:  # noqa
        alphabet += string.digits

    while True:
        counter = 0
        result = ""
        while counter < length:
            counter += 1
            result += secrets.choice(alphabet)

        if (
            (True == hasCapital and not any(i.isupper() for i in result))  # noqa
            or (
                True == hasSpecial  # noqa
                and not any(i in string.punctuation for i in result)
            )
            or (True == hasNumbers and not any(i.isdigit() for i in result))  # noqa
            or (True == hasXKCDStyle and (" " not in result.strip()))  # noqa
        ):
            continue
        break

    if True == b64:  # noqa
        result = b64encode(result.encode("utf-8")).decode("utf-8")
    return result


# print(pwgen(20, True, True, False, True))


# for cli tool
# should do it with bitmask like pwgen 20 0110 or +C +S +D +X
# if __name__ == '__main__':
