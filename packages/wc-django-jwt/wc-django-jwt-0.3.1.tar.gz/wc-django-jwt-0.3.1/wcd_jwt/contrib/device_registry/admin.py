from django.contrib import admin
from django.utils.translation import pgettext_lazy

from .models import TokenInterlocutorConnection


@admin.register(TokenInterlocutorConnection)
class TokenInterlocutorConnectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_device', 'get_os', 'get_app',
        'interlocutor', 'token', 'created_at',
    )
    date_hierarchy = 'created_at'
    list_select_related = (
        'interlocutor', 'interlocutor__device', 'interlocutor__os',
        'interlocutor__app',
        'token',
    )
    readonly_fields = 'updated_at', 'created_at',
    autocomplete_fields = 'interlocutor', 'token',
    search_fields = (
        'id', 'interlocutor__user_agent', 'token__token', 'token__jti',
        'token__user_connections__user__pk',
        'token__user_connections__user__username',
    )

    def get_device(self, obj):
        return obj.interlocutor.device
    get_device.short_description = pgettext_lazy('wcd_jwt', 'Device')
    get_device.admin_order_field = 'interlocutor__device'

    def get_os(self, obj):
        return obj.interlocutor.os
    get_os.short_description = pgettext_lazy('wcd_jwt', 'OS')
    get_os.admin_order_field = 'interlocutor__os'

    def get_app(self, obj):
        return obj.interlocutor.app
    get_app.short_description = pgettext_lazy('wcd_jwt', 'App')
    get_app.admin_order_field = 'interlocutor__app'

    def get_queryset(self, request):
        return super().get_queryset(request).distinct()
