import graphene

from apps.user import schema as user_schema


class Query(user_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
