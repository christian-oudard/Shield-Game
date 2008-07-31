_logfile = None

def init(logfile):
    global _logfile
    _logfile = open(logfile, 'w', 1)
    write('log "%s" initialized' % logfile)
    
def write(*args):
    message = ' '.join(str(a) for a in args)
    _logfile.write(message + '\n')
