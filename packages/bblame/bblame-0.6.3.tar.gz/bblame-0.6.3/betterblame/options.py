"""Module for maintaining and defining user options"""
from .util import check_string


class ToggleOption(object):
    """An option that has no value, it is only either enabled or disabled. It
    can be specifically set to either enabled or disabled, or be toggled back
    and fourth.
    """

    def __init__(self, name, enabled_by_default):
        """A new ToggleOption that must have a name and a default setting"""
        self.name = name
        if enabled_by_default:
            self.__enabled = True
        else:
            self.__enabled = False

    def is_enabled(self):
        """Returns True if this option is enabled, else false"""
        return self.__enabled

    def enable_option(self):
        """Set option to be enabled"""
        self.__enabled = True

    def disable_option(self):
        """Set option to be disabled"""
        self.__enabled = False

    def toggle_option(self):
        """Toggle a "toggle" option between disabled and enabled"""
        if self.is_enabled():
            self.disable_option()
        else:
            self.enable_option()


class FreeFormTextOption(object):
    """An option that has a free form text value. These options will mostly be
    used for config file values such as format strings or complex user
    preferences.
    """

    def __init__(self, name, default_value):
        """A new FreeFormTextOption that must have a name and a default value
        """
        self.name = name
        self.__value = default_value

    def get_free_text_option(self):
        """Return the free form value"""
        return self.__value

    def set_free_text_option(self, value):
        """Add <value> to option manager. Option must be a string"""
        check_string(value, 'Value must be a string!')
        self.__value = value


SHORTEN_FILEPATHS_OPT = 'shorten_filepaths'
SYNTAX_HIGHLIGHT_OPT = 'syntax_highlighting'
DEBUG_MODE_OPT = 'debug_mode'

OPTION_DEFAULTS = {
    SHORTEN_FILEPATHS_OPT: ToggleOption(SHORTEN_FILEPATHS_OPT, False),
    SYNTAX_HIGHLIGHT_OPT: ToggleOption(SYNTAX_HIGHLIGHT_OPT, True),
    DEBUG_MODE_OPT: ToggleOption(DEBUG_MODE_OPT, False),
}


def singleton(cls):
    """Decorator to only return one instance of a class object"""
    instances = {}

    def getinstance():
        """Return a new or existing instance of this class"""
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class UserOptionManager(object):
    """An object to manage all the user related options.
    There should only ever be one instance of this object (see singleton
    above).
    """

    def __init__(self):
        """Contruct a new UOM"""
        # Just bootstrap options from the defaults. As of right now, I'm not
        # worried about modifying the defaults dict object. The only case where
        # this would cause issues is if you wanted to go back and check what
        # the default is during runtime, which I don't have a use case for yet.
        # This can be changed to a deepcopy if such a use case arises.
        self.options = OPTION_DEFAULTS

    def get_option(self, option):
        """Return the option object for the option name <option>"""
        # Option names are strings
        check_string(option, 'Option name must be a string!')
        # Just let python dict KeyError be raised if that option doesn't exist
        return self.options[option]
