# API functions for interacting with permissions
"""
all logged-in users will have an associated user ID in the DB
permissions are also held in DB

"""


def request_coach(user):
    """

    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """

    return


def request_admin(user):
    """

    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """

    return


def approve_coach(approver):
    """

    :param approver: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """

    return


def approve_admin(approver):
    """

    :param approver: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """

    return


def is_coach(user):
    """

    :param user: user id from user data model
    :return: bool representing if user is coach
    """

    return


def is_admin(user):
    """

    :param user: user id from user data model
    :return: bool representing if user is admin
    """

    return
