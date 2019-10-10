class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(f"\n[*]Tip>> {message}")
