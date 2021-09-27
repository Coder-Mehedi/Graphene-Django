from graphql.type import schema
from category.models import Category
import graphene
from book.schema import Query as BookQuery, Mutation as BookMutation
from category.schema import Query as CategoryQuery, Mutation as CategoryMutation

class Query(BookQuery, CategoryQuery, graphene.ObjectType):
  pass

class Mutation(CategoryMutation, BookMutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)