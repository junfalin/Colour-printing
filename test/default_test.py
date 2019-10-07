from colour_printing.default import log

if __name__ == '__main__':
    log.set_default(set_level="error",time='123', flag='', message='success')
    log.error()
    log.success("hello world!")

    log.warning("hello world!")
    log.debug('')
