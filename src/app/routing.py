from w3fu.args import StrArg, IdArg
from w3fu.routing import Router, Route


router = Router(
                test=Route('/test'),
                index=Route('/'),
                home=Route('/home'),
                register=Route('/register'),
                login=Route('/login'),
                shortcut_login=Route('/login/{shortcut}', shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}')),
                providers_public=Route('/providers'),
                provider_public=Route('/providers/{provider_id}', provider_id=IdArg('provider_id')),
                providers_list_admin=Route('/home/providers/list'),
                providers_admin=Route('/home/providers'),
                provider_admin=Route('/home/providers/{provider_id}', provider_id=IdArg('provider_id')),
                services_list_admin=Route('/home/providers/{provider_id}/services/list', provider_id=IdArg('provider_id')),
                services_admin=Route('/home/providers/{provider_id}/services', provider_id=IdArg('provider_id')),
                service_admin=Route('/home/services/{service_id}', service_id=IdArg('service_id')),
                service_schedule_admin=Route('/home/services/{service_id}/schedule', service_id=IdArg('service_id')),
                service_workers_admin=Route('/home/services/{service_id}/workers', service_id=IdArg('service_id')),
                service_worker_admin=Route('/home/services/{service_id}/workers/{worker_id}', service_id=IdArg('service_id'), worker_id=IdArg('worker_id')),
                service_groups_admin=Route('/home/services/{service_id}/groups', service_id=IdArg('service_id')),
                service_group_admin=Route('/home/groups/{group_id}', group_id=IdArg('group_id')),
                workers_list_admin=Route('/home/providers/{provider_id}/workers/list', provider_id=IdArg('provider_id')),
                workers_admin=Route('/home/providers/{provider_id}/workers', provider_id=IdArg('provider_id')),
                worker_admin=Route('/home/workers/{worker_id}', worker_id=IdArg('worker_id')),
                worker_schedule_admin=Route('/home/workers/{worker_id}/schedule', worker_id=IdArg('worker_id')),
                )
