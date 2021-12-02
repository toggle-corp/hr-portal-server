# import json
# import factory
# from factory import fuzzy

# from utils.graphene.tests import GraphQLTestCase
# # from aaps.leave.factories import LeaveFactory
# from apps.user.factories import UserFactory
# from apps.leave.models import Leave, LeaveDay


# class TestLeaveMutation(GraphQLTestCase):

#     CREATE_LEAVE_QUERY = '''
#             mutation MyMutation ($input: LeaveApplyInputType!) {
#                 leaveApply(data: $input){
#                     errors
#                     ok
#                     result {
#                         additionalInformation
#                         createdAt
#                         createdBy {
#                             address
#                             birthday
#                             email
#                             secondaryPhoneNumber
#                             secondaryEmail
#                             primaryPhoneNumber
#                             primaryEmail
#                             lastName
#                             joinedAt
#                             id
#                             genderDisplay
#                             gender
#                             firstName
#                         }
#                         deniedReason
#                         endDate
#                         id
#                         numOfDays
#                         requestDayType
#                         startDate
#                         status
#                         statusDisplay
#                         type
#                         typeDisplay
#                         leaveDay {
#                             additionalInformation
#                             date
#                             id
#                             type
#                             typeDisplay
#                         }
#                     }
#                 }
#             }

#         '''

#     def setUp(self):
#         self.created_by = UserFactory.create()
#         self.input = {
#             "start_date": "2021-01-01",
#             "end-date": "2021-01-01",
#             "additional_information ": "This is a test leave",
#             "type": self.genum(Leave.Type.SICK),
#             "status": self.genum(Leave.Status.APPROVED),
#             "num_of_days": str(fuzzy.FuzzyInteger(0, 42)),
#             "created_by": str(factory.SubFactory(UserFactory)),
#             "leave_days": [
#                 {
#                     "additional_information": "This is a test information",
#                     "date": "2021-01-01",
#                     "type": str(fuzzy.FuzzyChoice(LeaveDay.Type)),
#                 }
#             ]
#         }
#         super().setUp()

#     def test_apply_leave(self):
#         # Without Login session
#         self.query_check(
#             self.CREATE_LEAVE_QUERY,
#             input_data=self.input,
#             assert_for_error=True
#         )

#         # Try with real user
#         user = self.created_by

#         # Login
#         self.force_login(user)
#         response = self.query(
#             self.CREATE_LEAVE_QUERY,
#             input_data=self.input
#         )
#         content = json.loads(response.content)
#         print(content)
#         self.assertResponseNoErrors(response)
