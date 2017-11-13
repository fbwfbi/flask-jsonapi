import flask_jsonapi.nested.nested_resources
from flask_jsonapi import descriptors
from flask_jsonapi import resource_repositories
from flask_jsonapi import resources
from flask_jsonapi.nested import nested_repository


class NestedResourceRepositoryViewSet(resource_repositories.ResourceRepositoryViewSet):
    nested_schema = descriptors.NotImplementedProperty('nested_schema')

    def __init__(self, *, nested_schema=None, **kwargs):
        super().__init__(**kwargs)
        if nested_schema:
            self.nested = nested_schema
        self.repository = self.extend_repository()

    def extend_repository(self):
        return nested_repository.NestedRepository(repository=self.repository)

    def as_list_view(self, view_name):
        return self.decorate(
            NestedResourceRepositoryListView.as_view(view_name, filter_schema=self.filter_schema, **self.get_list_view_kwargs())
        )

    def get_list_view_kwargs(self):
        kwargs = self.get_views_kwargs()
        kwargs.update({
            'nested_schema': self.nested_schema,
        })
        return kwargs


class NestedResourceRepositoryListView(resource_repositories.ResourceRepositoryViewMixin,
                                       flask_jsonapi.nested.nested_resources.NestedResourceList):
    def read_many(self, filters):
        return self.repository.get_list(filters)

    def create(self, data, **kwargs):
        return self.repository.create(data, **kwargs)
