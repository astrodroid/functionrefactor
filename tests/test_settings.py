from functionrefactor.settings import Settings


def test_settings():
    settings = Settings()
    assert settings.use_keyword_in_cpp("noexcept") == True
    assert settings.dont_move_oncpp_ifpresent("inline") == True
    try:
        settings.use_keyword_in_cpp("not a keyword")
    except KeyError:
        print("OK")
