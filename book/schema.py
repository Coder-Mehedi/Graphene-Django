from book.models import Book
from graphene.relay.mutation import ClientIDMutation
from graphene.types.field import Field
from graphene.types.scalars import ID, String
from book.models import Book
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id


class BookType(DjangoObjectType):
  class Meta:
    model = Book
    fields = "__all__"
    filter_fields = { 'title': ['exact', 'icontains'] }
    interfaces = [relay.Node]

class Query(ObjectType):
    book = relay.Node.Field(BookType)
    books = DjangoFilterConnectionField(BookType)

    def resolve_books(root, info, **kwargs):
      return Book.objects.all()


# Create
class CreateBookMutation(ClientIDMutation):
  class Input:
    title = String(required=True)

  book = Field(BookType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, title):
    book = Book(title=title)
    book.save()
    return CreateBookMutation(book=book)


# Update
class UpdateBookMutation(ClientIDMutation):
  class Input:
    title = String(required=True)
    id = ID(required=True)

  book = Field(BookType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, title, id):
    book = Book.objects.get(pk=from_global_id(id)[1])
    book.title = title
    book.save()
    return UpdateBookMutation(book=book)


# Delete
class DeleteBookMutation(ClientIDMutation):
  class Input:
    id = ID(required=True)

  books = DjangoFilterConnectionField(BookType)

  @classmethod
  def mutate_and_get_payload(cls, root, info, id):
    book = Book.objects.get(pk=from_global_id(id)[1])
    book.delete()
    return Book.objects.all()



class Mutation(ObjectType):
  create_book = CreateBookMutation.Field()
  update_book = UpdateBookMutation.Field()
  delete_book = DeleteBookMutation.Field()