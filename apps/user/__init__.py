# from utils.graphene.tests import GraphQLTestCase
# from apps.user.factories import LeaveFactory


# class TestUserMutation(GraphQLTestCase):
#     def setUp(self):
#         self.login_mutation = '''
#             mutation Mutation($input: LoginInputType!) {
#               login(data: $input) {
#                 ok
#                 result {
#                   id
#                   username
#                   primaryEmail
#                   firstName
#                   lastName
#                 }
#               }
#             }
#         '''
#         super().setUp()

#     def test_login(self):
#         # Try with random user
#         minput = dict(username='xyz', password='pasword-xyz')
#         self.query_check(self.login_mutation, minput=minput, okay=False)

#         # Try with real user
#         user = UserFactory.create(username=minput['username'])
#         minput = dict(username=user.username, password=user.password_text)
#         content = self.query_check(self.login_mutation, minput=minput, okay=True)
#         self.assertIdEqual(content['data']['login']['result']['id'], user.id, content)
#         self.assertEqual(content['data']['login']['result']['username'], user.username, content)

#     def test_logout(self):
#         query = '''
#             query Query {
#               me {
#                 id
#                 email
#               }
#             }
#         '''
#         logout_mutation = '''
#             mutation Mutation {
#               logout {
#                 ok
#               }
#             }
#         '''
#         user = UserFactory.create()
#         # # Without Login session
#         self.query_check(query, assert_for_error=True)

#         # # Login
#         self.force_login(user)

#         # Query Me (Success)
#         content = self.query_check(query)
#         self.assertIdEqual(content['data']['me']['id'], user.id, content)
#         self.assertEqual(content['data']['me']['email'], user.email, content)
#         # # Logout
#         self.query_check(logout_mutation, okay=True)
#         # Query Me (with error again)
#         self.query_check(query, assert_for_error=True)
