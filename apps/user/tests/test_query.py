from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory
from apps.leave.factories import LeaveFactory


class TestUserQuery(GraphQLTestCase):
    def setUp(self):
        self.query_me = '''
            query MyQuery {
                me {
                    email
                    firstName
                    gender
                    genderDisplay
                    id
                    isActive
                    lastName
                    lastLogin
                    remainingLeave
                    totalLeavesDays
                }
            }
        '''
        super().setUp()

    def test_me(self):
        # Without Login session
        self.query_check(self.query_me, assert_for_error=True)

        # Try with real user
        user = UserFactory.create()

        # Login
        self.force_login(user)
        LeaveFactory.create_batch(5, created_by=user)

        content = self.query_check(self.query_me)
        self.assertIdEqual(content['data']['me']['id'], user.id, content)
        self.assertEqual(content['data']['me']['email'], user.email, content)
