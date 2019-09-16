from colour_printing.custom import ColourPrint, Mode, Fore, Back


class Log(ColourPrint):
    def custom(self):
        self.debug = self.Markers('debug').flag_style(fore=Fore.PURPLE).time_style(mode=Mode.INVERT).message_style(
            fore=Fore.YELLOW)


log = Log()
log.debug('123', 'sda', 'sadasd')
