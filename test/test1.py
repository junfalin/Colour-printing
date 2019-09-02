from colour_printing import ColourPrint


class Log(ColourPrint):
    def custom(self):
        self.debug = self.Markers('debug').flag_style(mode='hide').time_style(mode='hide').message_style(fore='red')


log = Log()
log.debug('error')