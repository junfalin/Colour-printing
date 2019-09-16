from colour_printing.custom import ColourPrint, Back, Fore, Mode
from colour_printing import cprint


class MyColour(ColourPrint):
    def custom(self):
        self.test = self.Markers('test').flag_style(fore=Fore.CYAN, mode=Mode.HIDE).time_style(
            mode=Mode.UNDERLINE).message_style(
            fore=Fore.YELLOW)


echo = MyColour()
cprint(echo, fore=Fore.BLUE, mode=Mode.BOLD)
echo.test('hello world!')
