from dynamic_preferences.types import (
    BooleanPreference, LongStringPreference, FilePreference
)
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
# from dynamic_preferences.users.registries import user_preferences_registry

from django.utils.translation import gettext as _


general = Section('general')
app = Section('app')


@global_preferences_registry.register
class VerificationEmail(BooleanPreference):
    section = app
    name = 'verification_email'
    default = False


@global_preferences_registry.register
class MaintenanceMode(BooleanPreference):
    section = general
    name = 'maintenance_mode'
    default = False


@global_preferences_registry.register
class MaintenaceModeText(LongStringPreference):
    section = general
    name = 'maintenance_mode_text'
    default = _(
        'Estamos realizando un mantenimiento programado, '
        'disculpe las molestias'
    )
    required = False
