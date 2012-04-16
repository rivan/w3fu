from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage.collections.providers import Providers
from app.storage.documents.providers import Provider


class ProvidersPublic(Resource):

    route = Route('/providers')

    @xml('pages/providers-public/providers-public.html.xsl')
    @user()
    def get(self, req):
        return Response.ok({})


class ProviderPublic(Resource):

    route = Route('/providers/{id}', id=IdArg('id'))

    @xml('pages/provider-public/provider-public.html.xsl')
    @user()
    def get(self, req):
        provider = Providers(self.ctx.db).find_id(req.ctx.args['id'])
        if provider is None:
            return Response.not_found()
        return Response.ok({'provider': provider})


class ProviderForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class ProvidersAdmin(Resource):

    route = Route('/home/providers')

    @xml('pages/providers-admin/providers-admin.html.xsl')
    @user(required=True)
    def get(self, req):
        return Response.ok({})

    @xml('pages/providers-admin/providers-admin.html.xsl')
    @user(required=True)
    def post(self, req):
        form = ProviderForm(req)
        if form.errors:
            return Response.ok({'form': form})
        provider = Provider.new(name=form.data['name'],
                        owner=req.ctx.state['user'])
        Providers(self.ctx.db).insert(provider)
        return Response.redirect(ProviderAdmin.route.url(req, id=provider.id))


class ProviderAdmin(Resource):

    route = Route('/home/providers/{id}', id=IdArg('id'))

    @xml('pages/provider-admin/provider-admin.html.xsl')
    @user(required=True)
    def get(self, req):
        provider = Providers(self.ctx.db).find_id(req.ctx.args['id'])
        if provider is None:
            return Response.not_found()
        return Response.ok({'provider': provider})

    @xml('pages/provider-admin/provider-admin.html.xsl')
    @user(required=True)
    def put(self, req):
        form = ProviderForm(req)
        if form.errors:
            return Response.ok({'form': form})
        providers = Providers(self.ctx.db)
        provider = providers.find_id(req.ctx.args['id'])
        if provider is not None and provider.writable_by(req.ctx.state['user']):
            provider.name = form.data['name']
            providers.update(provider)
        return Response.redirect(ProvidersAdmin.route.url(req))

    @user(required=True)
    def delete(self, req):
        providers = Providers(self.ctx.db)
        provider = providers.find_id(req.ctx.args['id'])
        if provider is not None and provider.writable_by(req.ctx.state['user']):
            providers.remove_id(provider.id)
        return Response.redirect(ProvidersAdmin.route.url(req))


def block_providers(req, providers):
    return [{'provider': provider, 'path': ProviderAdmin.route.path(id=provider.id)}
            for provider in providers]


class ProvidersListAdmin(Resource):

    route = Route('/home/providers/list')

    @xml('pages/providers-list-admin/providers-list-admin.html.xsl')
    @user(required=True)
    def get(self, req):
        found = Providers(self.ctx.db).find_user(req.ctx.state['user'])
        return Response.ok({'providers': block_providers(req, found)})
