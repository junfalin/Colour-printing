class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__("\n[*]Tip>> {message}".format(message=message))
