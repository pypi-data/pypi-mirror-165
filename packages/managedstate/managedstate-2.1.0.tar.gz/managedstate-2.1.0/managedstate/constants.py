class ErrorMessages:
    @staticmethod
    def no_default(path_index):
        raise ValueError("No value found and no default provided for the path key at index {0}".format(path_index))
