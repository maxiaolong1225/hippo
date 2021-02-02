from channels.routing import ProtocolTypeRouter,ChannelNameRouter

from hippo_api.apps.consumer import routing

application = ProtocolTypeRouter({
    'websocket': routing.ws_router,
})