import logging

from fastapi import status
from sqlalchemy.orm import Session

from core.logging import get_logger
from exception.app_exceptions import DuplicateUserException, AppException
from exception.error_code import INTERNAL_SERVER_ERROR
from repository import user_repository
from service.dto.user_dto import UserCreate

logger = get_logger(__name__)


def get_users(db: Session):
    try:
        logger.info("Trying to get all users")

        users = user_repository.get_all_users(db)

        logger.info(f"Found {len(users)} users")

        return users
    except Exception as e:
        logger.exception('Unexpected Error has occurred while retrieving users')
        raise AppException(
            code=INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred while reading all users.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


def create_user(db: Session, user: UserCreate):
    try:
        logger.info("Trying to create new user")
        existing_user = user_repository.get_user_by_email(db, user.email)
        if existing_user:
            logging.warn("User with email {} already exists".format(user.email))
            raise DuplicateUserException()

        saved_user = user_repository.add_user(db, user)

        logger.info(f"Created new user with email {user.email}")
        return saved_user
    except DuplicateUserException as e:
        raise e
    except Exception as e:
        logger.exception('Unexpected Error has occurred while saving a new user')
        raise AppException(
            code=INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred while creating the user.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e
