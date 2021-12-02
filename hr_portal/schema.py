import graphene

from apps.user import schema as user_schema, mutation as user_mutation
from apps.leave import schema as leave_schema, mutation as leave_mutation


class Query(
    user_schema.Query,
    leave_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    user_mutation.Mutation,
    leave_mutation.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
