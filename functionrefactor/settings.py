import json

__all__ = ['Settings', 'settings']


class Settings():

    def __init__(self):
        with open("functionrefactor/settings.json", "r") as infile:
            self.json_file = json.load(infile)

        self._keywords_only_shown_in_hpp = self.json_file[
            "keywords_only_shown_in_hpp"]
        self._dontmove_on_cpp_if = self.json_file["dontmove_on_cpp_if"]

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


settings = Settings()
