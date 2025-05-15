"""
test config file
contains the test config class
"""
import os

class TestConfig:
    """test environment config class"""
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # disable CSRF in testing
    SERVER_NAME = 'localhost.localdomain'  # set server name, help session management
    SESSION_TYPE = 'filesystem'  # use file system to store session
    PRESERVE_CONTEXT_ON_EXCEPTION = False  # avoid keeping context exception in testing