import graphene

from apps.user import schema as user_schema
from apps.user import mutation as user_mutation


class Query(user_schema.Query, graphene.ObjectType):
    pass


class Mutation(user_mutation.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
