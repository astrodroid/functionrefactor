import json
import os

__all__ = ['Settings', 'settings']


class Settings():
    ''' sets the settings.
        Each case can have settings set within the launcher(json) object (medium priority)
        or within the case object (high priority).
        If none of these is found, then the  default one is used'''

    def __init__(self, run_settings=None):
        path = os.path.join(os.path.dirname(__file__), "settings.json")
        with open(path, "r") as infile:
            self.default_settings = json.load(infile)

        self.run_settings = None
        self._keywords_only_shown_in_hpp = None
        self._dontmove_on_cpp_if = None
        self.update_global_settings(None)

    def update_global_settings(self, run_settings):
        ''' updates the settings that affect all the launched cases'''
        self.run_settings = run_settings
        self.update_case_settings(None)

    def update_case_settings(self, case_settings):
        ''' updates the settins that affect only the current case'''
        self._keywords_only_shown_in_hpp = find_jkey(
            "keywords_only_shown_in_hpp", case_settings, self.run_settings,
            self.default_settings)
        self._dontmove_on_cpp_if = find_jkey("dontmove_on_cpp_if",
                                             case_settings, self.run_settings,
                                             self.default_settings)

    def use_keyword_in_cpp(self, keyw):
        """
        returns true if the keyword needs to be shown in the C++ source file
        together with the function declaration
            If the key is not found returns true as it assumes it's the return type of a function
        """

        if keyw in self._keywords_only_shown_in_hpp:
            return self._keywords_only_shown_in_hpp[keyw]
        else:
            return True

    def dont_move_oncpp_ifpresent(self, keyw):
        """
        Returns true if a function with such a keyword doesn't need to be moved in
        the C++ source file, for example inline functons and constexpr functions (?)
        should remain im th header file
            If the key is not found returns False as it assumes it's the return type of a function
        """

        if keyw in self._dontmove_on_cpp_if:
            return self._dontmove_on_cpp_if[keyw]
        else:
            return False


def find_jkey(key, high_priority, low_priority, default_json):
    ''' checks if a key is contained within a  JSON object:
        first in the override file (user settings)
        and if not then on the default settings'''

    if high_priority and key in high_priority:
        return high_priority[key]
    elif low_priority and key in low_priority:
        return low_priority[key]
    return default_json[key]


settings = Settings()
