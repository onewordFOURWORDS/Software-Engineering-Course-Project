# API functions for interacting with permissions
"""
all logged-in users will have an associated user ID in the DB
permissions are also held in DB

"""
# from app import app, db
from app.models import *


def deny_coach(admin, user, pr=None):
    """
    call when admin rejects user requests for coach privileges in UI
    :param pr: permission request
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial
    if pr:
        user.is_coach = False
        user.coachApproveID = admin.id
        db.session.delete(pr)
        db.session.commit()
    else:
        user.is_coach = False
        user.coachApproveID = admin.id
        db.session.commit()
    return


def deny_admin(admin, user, pr=None):
    """
    call when admin rejects user requests for admin privileges in UI
    :param pr: permission request
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission denied success or fail
    """
    # TODO call some functionality to inform user of denial
    if pr:
        user.is_admin = False
        user.adminApproveID = admin.id
        db.session.delete(pr)
        db.session.commit()
    else:
        user.is_admin = False
        user.adminApproveID = admin.id
        db.session.commit()
    return


def approve_coach(admin, user, pr=None):
    """
    call when admin approves user requests for coach privileges in UI
    :param pr: permission request
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """
    # TODO add privilege to user in db
    # TODO call some functionality to inform user of approval
    if pr:
        user.is_coach = True
        user.coachApproveID = admin.id
        db.session.delete(pr)
        db.session.commit()
    else:
        user.is_coach = True
        user.coachApproveID = admin.id
        db.session.commit()
    return


def approve_admin(admin, user, pr=None):
    """
    call when admin approves user requests for admin privileges in UI
    :param pr: permission request
    :param user:
    :param admin: admin user id from user data model
    :return: bool indicating permission granted success or fail
    """
    # TODO add privilege to user in db
    # TODO call some functionality to inform user of approval
    if pr:
        user.is_admin = True
        user.adminApproveID = admin.id
        db.session.delete(pr)
        db.session.commit()
    else:
        user.is_admin = True
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
    # username = db.session.query(User).filter(User.username == user.username)
    return user.is_coach


def is_admin(user):
    """
    call when checking for admin privilege
    :param user: user id from user data model
    :return: bool representing if user is admin
    """
    # TODO query db
    # username = db.session.query(User).filter(User.username == user)
    return user.is_admin
