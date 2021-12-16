import json

from utils.graphene.tests import GraphQLTestCase
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
        self.input = {
            "additionalInformation": "This is a test leave",
            "type": "SICK",
            "leaveDays": [
                {
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-04",
                    "type": "FULL",
                },
                {
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-05",
                    "type": "FULL",
                }
            ]
        }
        super().setUp()

    def test_apply_leave(self):

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
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['leaveApply']['ok'], content)
        self.assertIsNone(content['data']['leaveApply']['errors'], content)
        self.assertIsNotNone(content['data']['leaveApply']['result']['id'])
        self.assertEqual(
            content['data']['leaveApply']['result']['startDate'],
            content['data']['leaveApply']['result']['leaveDay'][0]['date']
        )
        self.assertEqual(
            content['data']['leaveApply']['result']['endDate'],
            content['data']['leaveApply']['result']['leaveDay'][-1]['date']
        )
        self.assertIsNotNone(content['data']['leaveApply']['result']['leaveDay'][0]['id'])

    def test_validate_apply_leave(self):
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
        self.assertTrue(content['data']['leaveApply']['ok'])
        response = self.query(
            self.CREATE_LEAVE_QUERY,
            input_data=self.input
        )
        content = json.loads(response.content)
        #  Should not be able to apply already existing leave
        self.assertFalse(content['data']['leaveApply']['ok'])

    def test_update_leave(self):
        # Try with real user
        user = self.created_by

        # Login
        self.force_login(user)

        #  create a leave
        apply_leave_response = self.query(
            self.CREATE_LEAVE_QUERY,
            input_data=self.input
        )
        leave_apply_content = json.loads(apply_leave_response.content)
        leave_id = leave_apply_content['data']['leaveApply']['result']['id']

        leave_days = leave_apply_content['data']['leaveApply']['result']['leaveDay']
        leave_day_id_list = [leave_day['id'] for leave_day in leave_days]

        self.update_leave_input = {
            "id": leave_id,
            "additionalInformation": "This is a test update leave",
            "type": "SICK",
            "leaveDays": [
                {
                    "id": leave_day_id_list[0],
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-04",
                    "type": "FULL",
                },
                {
                    "id": leave_day_id_list[1],
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-05",
                    "type": "FIRST_HALF",
                },
                {
                    "additionalInformation": "This is a test information",
                    "date": "2021-01-06",
                    "type": "FULL",
                }
            ]
        }
        update_leave_response = self.query(
            self.UPDATE_LEAVE_QUERY,
            input_data=self.update_leave_input
        )
        leave_update_content = json.loads(update_leave_response.content)
        #  Should not be able to update leave that is already approved or Denied
        self.assertFalse(leave_update_content['data']['leaveUpdate']['ok'])
