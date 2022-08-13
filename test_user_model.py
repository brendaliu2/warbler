"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase, expectedFailure
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
load_dotenv()
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Tests user is created"""
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test__repr__(self):
        """Test repr function works"""
        u1 = User.query.get(self.u1_id)
        repr = u1.__repr__()

        self.assertIn(f'{self.u1_id}', repr)

    def test_is_following(self):
        """"Tests is following"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)

        followA = u1.is_following(u2)
        followB = u2.is_following(u1)

        self.assertTrue(followB)
        self.assertFalse(followA)

    def test_is_followed_by(self):
        """Test is_followed_by"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)

        followA = u1.is_followed_by(u2)
        followB = u2.is_followed_by(u1)

        self.assertTrue(followA)
        self.assertFalse(followB)


    # @expectedFailure
    def test_signup_fail(self):
        """Test sign up fails with invalid inputs"""
# import integrity error?

        # invalid_user = User.signup('u90','invalidemail', 'password', None)
        # db.session.commit()

        # self.assertRaises(IntegrityError, db.session.commit)

        with self.assertRaises(IntegrityError):
            invalid_user = User.signup('u90','invalidemail', 'password', None)
            db.session.commit()

    def test_signup_valid(self):
        """Test sign up valid with valid inputs"""

        u3 = User.signup('u3','u3@email.com', 'password', None)
        db.session.commit()

        self.assertIsInstance(u3, User)



    def test_authenticate(self):
        """Test authenticate"""

        u1 = User.query.get(self.u1_id)
        valid = User.authenticate(u1.username, 'password')
        invalid_pw = User.authenticate(u1.username, 'invalid')
        invalid_username = User.authenticate('invalid', 'password')


        self.assertEqual(u1, valid)
        self.assertFalse(invalid_pw)
        self.assertFalse(invalid_username)






