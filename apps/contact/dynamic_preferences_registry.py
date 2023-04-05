from dynamic_preferences.types import BooleanPreference, StringPreference, LongStringPreference,FilePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry

from django.utils.translation import gettext as _


contact = Section('contact')

@global_preferences_registry.register
class Telephone(StringPreference):
    section = contact
    name = 'telephone'
    default= ''
    required = False

@global_preferences_registry.register
class Address(LongStringPreference):
    section = contact
    name = 'address'
    default= ''
    required = False

@global_preferences_registry.register
class Email(StringPreference):
    section = contact
    name = 'email'
    default= ''
    required = False

@global_preferences_registry.register
class ShowMap(BooleanPreference):
    section = contact
    name = 'show_map'
    default = False

@global_preferences_registry.register
class Latitude(StringPreference):
    section = contact
    name = 'latitude'
    default= ''
    required = False

@global_preferences_registry.register
class Longitude(StringPreference):
    section = contact
    name = 'longitude'
    default= ''
    required = False

@global_preferences_registry.register
class TextMap(LongStringPreference):
    section = contact
    name = 'text_map'
    default= ''
    required = False

@global_preferences_registry.register
class AdministratorEmail(LongStringPreference):
    section = contact
    name = 'administrator_email'
    default= 'admin@admin.es'
    required = False
