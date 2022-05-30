import functools

from utils.ui.components.component import Component


class IFrame(Component):
    """
    Base iframe component

    Example:
        >>> iframe = IFrame('some_locator', 'My IFrame')
    """
    on_iframe = False

    def __init__(self, name_or_id, locator=None):
        super().__init__(locator)
        self._name_or_id = name_or_id

    @property
    def type_of(self):
        return 'iframe'

    @property
    def name_or_id(self):
        return self._name_or_id

    def switch_to_iframe(self):
        self.py.switch_to.frame(self._name_or_id)
        IFrame.on_iframe = True

    def switch_to_default_content(self):
        self.py.switch_to.default_content()
        IFrame.on_iframe = False


def with_iframe(iframe: IFrame):
    """
    Should be used for page object action if this
    action is uses iframe

    @with_iframe(iframe)
    def click_some_button(self):
        ...
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if not IFrame.on_iframe:
                iframe.switch_to_iframe()

            return func(*args, **kwargs)

        return inner

    return wrapper


def without_iframe(iframe: IFrame):
    """
    Should be used for page object action if this
    action is not uses iframe

    @without_iframe(iframe)
    def click_some_button(self):
        ...
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if IFrame.on_iframe:
                iframe.switch_to_default_content()

            return func(*args, **kwargs)

        return inner

    return wrapper
