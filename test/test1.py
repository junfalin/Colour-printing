from colour_printing.default import ColourPrint,Back, Fore, Mode
from colour_printing import cprint


class MyColour(ColourPrint):
    def custom(self):
        self.test = self.Pen('test') \
            .flag_style(fore=Fore.CYAN) \
            .time_style(mode=Mode.UNDERLINE) \
            .message_style(fore=Fore.YELLOW)


echo = MyColour()
cprint(echo, fore=Fore.BLUE, mode=Mode.BOLD)
echo.test('hello world!')
