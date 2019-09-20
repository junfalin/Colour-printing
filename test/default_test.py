from colour_printing.default import log

if __name__ == '__main__':
    log.set_default(time='123', flag='s', message='success')
    log.error("hello world!")
    log.success("hello world!")

    log.warning("hello world!")
    log.debug()
