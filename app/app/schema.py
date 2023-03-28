import graphene
import assistencia_tecnica.schema


class Query(assistencia_tecnica.schema.Query, graphene.ObjectType):
    pass


class Mutation(assistencia_tecnica.schema.Mutation, graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
