from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:ghimire@localhost/warbler-test"
# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):

    class UserModelTestCase(TestCase):
        """Test views for messages."""

        def setUp(self):
            """Create test client, add sample data."""
            db.drop_all()
            db.create_all()

            self.uid = 10
            u = User.signup("testing", "testing@test.com", "password", None)
            u.id = self.uid
            db.session.commit()

            self.u = User.query.get(self.uid)

            self.client = app.test_client()

        def tearDown(self):
            res = super().tearDown()
            db.session.rollback()
            return res

        def test_message_model(self):
            """Does basic model work?"""

            m = Message(
                text="Hello",
                user_id=self.uid
            )

            db.session.add(m)
            db.session.commit()

            # User should have 1 message
            self.assertEqual(len(self.u.messages), 1)
            self.assertEqual(self.u.messages[0].text, "Hello")
