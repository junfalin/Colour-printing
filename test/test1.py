from colour_printing import ColourPrint


class Log(ColourPrint):
    def custom(self):
        self.debug = self.Markers('debug').flag_style(mode='hide').time_style(mode='hide').message_style(fore='red')


log = Log()
print(log)
log.debug('123', 'sda', 'sadasd')

s1 = log.dyestuff('this red', fore='red')
s2 = Log.dyestuff('this green', fore='green')
s3 = ColourPrint.dyestuff('this blue', fore='blue')
print(s1, s2, s3)
