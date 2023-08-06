class Keys:
    METHOD_GET = "get"
    METHOD_SET = "set"

    NEW_STATE = "new_state"


class ErrorMessages:
    @staticmethod
    def invalid_method(method):
        raise ValueError("Unable to add listeners to the specified method: {}".format(method))
