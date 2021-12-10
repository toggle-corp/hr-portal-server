import json

from utils.graphene.tests import GraphQLTestCase
# from aaps.leave.factories import LeaveFactory
from apps.user.factories import UserFactory


class TestLeaveMutation(GraphQLTestCase):

    CREATE_LEAVE_QUERY = '''
            mutation MyMutation ($input: LeaveApplyInputType!) {
                leaveApply(data: $input){
                    errors
                    ok
                    result {
                        additionalInformation
                        createdAt
                        createdBy {
                            address
                            birthday
                            email
                            secondaryPhoneNumber
                            secondaryEmail
                            primaryPhoneNumber
                            primaryEmail
                            lastName
                            joinedAt
                            id
                            genderDisplay
                            gender
                            firstName
                        }
                        deniedReason
                        endDate
                        id
                        numOfDays
                        requestDayType
                        startDate
                        status
                        statusDisplay
                        type
                        typeDisplay
                        leaveDay {
                            additionalInformation
                            date
                            id
                            type
                            typeDisplay
                        }
                        numOfDays
                        requestDayType
                        startDate
                        status
                        statusDisplay
                        type
                        typeDisplay
                        }
                    }
                }
        '''

    UPDATE_LEAVE_QUERY = '''
            mutation MyMutation ($input: LeaveUpdateInputType!){
                    leaveUpdate(data: $input) {
                        errors
                        ok
                        result {
                        additionalInformation
                        createdAt
                        createdBy {
                            address
                            birthday
                            email
                            firstName
                            gender
                            genderDisplay
                            id
                            joinedAt
                            lastName
                            primaryEmail
                            primaryPhoneNumber
                            secondaryEmail
                            secondaryPhoneNumber
                        }
                        deniedReason
                        endDate
                        id
                        leaveDay {
                            additionalInformation
                            date
                            id
                            type
                            typeDisplay
                            user
                        }
                        numOfDays
                        requestDayType
                        startDate
                        status
                        statusDisplay
                        type
                        typeDisplay
                        }
                    }
                }
        '''

    def setUp(self):
        self.created_by = UserFactory.create()
        super().setUp()

    def test_apply_leave(self):
        self.input = {
            "additionalInformation": "This is a test leave",
            "type": "SICK",
            "leaveDays": [
                {
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-03",
                    "type": "FULL",
                },
                {
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-04",
                    "type": "FULL",
                }
            ]
        }
        # Without Login session
        self.query_check(
            self.CREATE_LEAVE_QUERY,
            input_data=self.input,
            assert_for_error=True
        )

        # Try with real user
        user = self.created_by

        # Login
        self.force_login(user)
        response = self.query(
            self.CREATE_LEAVE_QUERY,
            input_data=self.input
        )
        content = json.loads(response.content)
        print(content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['leaveApply']['ok'], content)
        self.assertIsNone(content['data']['leaveApply']['errors'], content)
        self.assertIsNotNone(content['data']['leaveApply']['results']['id'])
        # self.assertEqual(content['data']['leaveApply']['results']['id']),
        #                 content['data']['leaveApply']['results']['leave_days'][0]['leave']['id'])



    # def test_update_leave(self):
    #     self.apply_leave_input = {
    #         "additionalInformation": "This is a test leave",
    #         "type": "SICK",
    #         "leaveDays": [
    #             {
    #                 "additionalInformation": "This is a test information",
    #                 "date": "2021-01-04",
    #                 "type": "FULL",
    #             },
    #             {
    #                 "additionalInformation": "This is a test information",
    #                 "date": "2021-01-05",
    #                 "type": "FULL",
    #             }
    #         ]
    #     }
    #     # Without Login session
    #     self.query_check(
    #         self.CREATE_UPDATE_QUERY,
    #         input_data=self.input,
    #         assert_for_error=True
    #     )

    #     # Try with real user
    #     user = self.created_by

    #     # Login
    #     self.force_login(user)
    #     apply_leave_response = self.query(
    #         self.CREATE_LEAVE_QUERY,
    #         input_data=self.input
    #     )
    #     leave_apply_content = json.loads(apply_leave_response.content)
    #     self.assertResponseNoErrors(response)
