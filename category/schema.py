from graphene.relay.mutation import ClientIDMutation
from graphene.types.field import Field
from graphene.types.scalars import ID, String
from category.models import Category
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id


class CategoryType(DjangoObjectType):
  class Meta:
    model = Category
    fields = "__all__"
    filter_fields = ['title']
    interfaces = [relay.Node]

class Query(ObjectType):
    category = relay.Node.Field(CategoryType)
    categories = DjangoFilterConnectionField(CategoryType)

    def resolve_categories(root, info, **kwargs):
      return Category.objects.all()


# Create
class CreateCategoryMutation(ClientIDMutation):
  class Input:
    title = String(required=True)

  category = Field(CategoryType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, title):
    category = Category(title=title)
    category.save()
    return CreateCategoryMutation(category=category)


# Update
class UpdateCategoryMutation(ClientIDMutation):
  class Input:
    title = String(required=True)
    id = ID(required=True)

  category = Field(CategoryType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, title, id):
    category = Category.objects.get(pk=from_global_id(id)[1])
    category.title = title
    category.save()
    return UpdateCategoryMutation(category=category)


# Delete
class DeleteCategoryMutation(ClientIDMutation):
  class Input:
    id = ID(required=True)

  categories = DjangoFilterConnectionField(CategoryType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, id):
    category = Category.objects.get(pk=from_global_id(id)[1])
    category.delete()
    return Category.objects.all()



class Mutation(ObjectType):
  create_category = CreateCategoryMutation.Field()
  update_category = UpdateCategoryMutation.Field()
  delete_category = DeleteCategoryMutation.Field()