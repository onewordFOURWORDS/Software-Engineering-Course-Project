# API functions for interacting with permissions
"""
all logged-in users will have an associated user ID in the DB
permissions are also held in DB

"""
#from app import app, db
from app.models import *


def request_coach(user):
    """
    call when a user requests coach privileges in the UI
    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """
    # TODO call some functionality to inform admins of request and present admins with approval/denial UI
    db.session.commit()
    return


def request_admin(user):
    """
    call when a user requests admin privileges in the UI
    :param user: user id from user data model
    :return: bool indicating request success, false indicates user already has permission
    """
    # TODO call some functionality to inform admins of request and present admins with approval/denial UI
    db.session.commit()
    return


def deny_coach(admin, user):
    """
    call when admin rejects user requests for coach privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial
    user.isCoach = False
    user.coachApproveID = admin.id
    db.session.commit()
    return


def deny_admin(admin, user):
    """
    call when admin rejects user requests for admin privileges in UI
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial

    user.isAdmin = False
    user.adminApproveID = admin.id
    db.session.commit()
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
    user.isCoach = True
    user.coachApproveID = admin.id
    db.session.commit()
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
    user.isAdmin = True
    user.adminApproveID = admin.id
    db.session.commit()
    return


def is_coach(user):
    """
    call when checking for coach privilege
    :param user: user object from user data model
    :return: bool representing if user is coach
    """
    # TODO query db
    #username = db.session.query(User).filter(User.username == user.username)
    return user.isCoach()


def is_admin(user):
    """
    call when checking for admin privilege
    :param user: user id from user data model
    :return: bool representing if user is admin
    """
    # TODO query db
    #username = db.session.query(User).filter(User.username == user)
    return user.isAdmin()
