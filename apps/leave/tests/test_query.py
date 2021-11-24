from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory
from apps.leave.factories import LeaveFactory


class TestLeaveQuery(GraphQLTestCase):
    def setUp(self):
        super().setUp()
        self.created_by = UserFactory.create()

    def test_leave(self):
        self.query_leave = '''
            query MyQuery {
                leaves {
                    additionalInformation
                    createdAt
                    deniedReason
                    endDate
                    id
                    numOfDays
                    startDate
                    status
                    statusDisplay
                    type
                    typeDisplay
                    createdBy {
                        id
                        firstName
                        lastName
                        }
                    leaveDay {
                        additionalInformation
                        date
                        id
                        type
                        typeDisplay
                        }
                    }
                }
        '''
        # Without Login session
        self.query_check(self.query_leave, assert_for_error=True)

        # Try with real user
        user = self.created_by

        # Login
        self.force_login(user)
        leaves = LeaveFactory.create_batch(5, created_by=user)
        content = self.query_check(self.query_leave)
        # query object count must be equal to the number of leave object created by authenticated user
        self.assertEqual(len(content['data']['leaves']), 5, content)
        # authenticatd user id must be equal to user id of a user in query
        self.assertIdEqual(content['data']['leaves'][0]['createdBy']['id'], user.id, content)
        self.assertIdEqual(content['data']['leaves'][0]['createdBy']['id'], leaves[0].created_by.id, content)

        user2 = UserFactory.create()
        # Login
        self.force_login(user2)
        content = self.query_check(self.query_leave)
        # new authenticated leave count has to be 0
        self.assertEqual(len(content['data']['leaves']), 0, content)
