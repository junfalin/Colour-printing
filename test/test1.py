from colour_printing.custom import ColourPrint, Back, Fore, Mode
from colour_printing import cprint


class MyColour(ColourPrint):
    def custom(self):
        self.test = self.Markers('test').flag_style(fore=Fore.PURPLE, mode=Mode.HIDE).time_style(
            mode=Mode.INVERT).message_style(
            fore=Fore.YELLOW)


echo = MyColour()
cprint(echo, fore=Fore.CYAN)
echo.test('hello world!')
