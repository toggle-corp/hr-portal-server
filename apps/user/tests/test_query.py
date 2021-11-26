from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory


class TestUserQuery(GraphQLTestCase):
    def setUp(self):
        self.query_me = '''
            query Query {
                me {
                    id
                    gender
                    firstName
                    lastName
                    username
                    secondaryPhoneNumber
                    secondaryEmail
                    primaryPhoneNumber
                    primaryEmail
                    joinedAt
                    isSuperuser
                    genderDisplay
                    email
                    birthday
                    avatarUrl
                    avatar
                    address
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

        content = self.query_check(self.query_me)
        self.assertIdEqual(content['data']['me']['id'], user.id, content)
        self.assertEqual(content['data']['me']['email'], user.email, content)
