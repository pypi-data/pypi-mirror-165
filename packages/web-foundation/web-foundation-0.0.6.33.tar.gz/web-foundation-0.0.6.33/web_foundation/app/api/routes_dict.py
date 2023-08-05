import loguru

from web_foundation.app.events.base import CloseChargeAeEvent
from web_foundation.app.events.store import StoreUpdateEvent


async def some_handler(context, container):
    loguru.logger.info("ASSSSSSSSSSSSSSSSSSSSSSSsss")
    # await container.ticket_service().emmit_event(CloseChargeAeEvent())
    # await container.ticket_service().emmit_event(StoreUpdateEvent("plugins", mg.plugs_to_send))
    return {}


async def add_plugin(context, app_container):
    await app_container.ticket_service().worker.add_new_middleware(context.request.json.get("filename"))
    # mg = app_container.plugin_manager()
    # # await app_container.store().get_all()
    # await mg.add_new_middleware(context.request.json.get("filename"))
    # await app_container.ticket_service().emmit_event(StoreUpdateEvent("plugins", mg.available_middlewares))
    # await app_container.ticket_service().emmit_event(CloseChargeAeEvent())
    return {}


routes_dict = {
    "apps": [
        {
            "app_name": "ae_app",
            "version_prefix": "/api/v",
            "endpoints": {
                "/test": {
                    "v14": {
                        "get": {"handler": some_handler,
                                "protector": None, },
                        "post": {
                            "handler": add_plugin,
                            "protector": None,
                        }
                    }
                }
            }
        }
    ]
}
