from colour_printing import ColourPrint


class Log(ColourPrint):
    def custom(self):
        self.debug = self.Markers('debug').flag_style(mode='hide').time_style(mode='hide').message_style(fore='red')


log = Log()

log.info('123', 'sda', 'sadasd')
s1 = log.dyestuff('this red', fore='red')
s2 = log.dyestuff('this green', fore='green')
print(s1, s2)
