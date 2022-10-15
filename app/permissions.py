# API functions for interacting with permissions
"""
all logged-in users will have an associated user ID in the DB
permissions are also held in DB

"""
from app import app


def request_coach(user):
    """
    call when a user requests coach privileges in the UI
    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """
    # TODO call some functionality to inform admins of request and present admins with approval/denial UI

    return


def request_admin(user):
    """
    call when a user requests admin privileges in the UI
    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """
    # TODO call some functionality to inform admins of request and present admins with approval/denial UI

    return


def deny_coach(admin, user):
    """
    call when admin rejects user requests for coach privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial

    return


def deny_admin(admin, user):
    """
    call when admin rejects user requests for admin privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial

    return


def approve_coach(admin, user):
    """
    call when admin approves user requests for coach privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """
    # TODO add privilege to user in db
    # TODO call some functionality to inform user of approval

    return


def approve_admin(admin, user):
    """
    call when admin approves user requests for admin privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """
    # TODO add privilege to user in db
    # TODO call some functionality to inform user of approval

    return


def is_coach(user):
    """
    call when checking for coach privilege
    :param user: user id from user data model
    :return: bool representing if user is coach
    """
    # TODO query db
    print("is_coach is being called.")
    return True


def is_admin(user):
    """
    call when checking for admin privilege
    :param user: user id from user data model
    :return: bool representing if user is admin
    """
    # TODO query db
    print("is_admin is being called")
    return True
