#!/usr/bin/env python

import imagemodel, sys
from twisted.python import usage
from twisted.python.filepath import FilePath


class StartOptions(usage.Options):
    def getSynopsis(self):        
        return """Usage: %s <options> [directory holding slideshow data]""" % __file__

    optParameters = [
            ('width', 'w', 1024, 'Width of screen'),
            ('height', 'h', 768, 'Height of screen'),
            ]

    optFlags = [
        ('noexit', 'e', 'Do not allow exit via ESC'),
        ('switch-keys', 'S', 'Switches the up/down keys to switch dirs'),
        ]

    def parseArgs(self, location):
        self.location = FilePath(location).children()[0]

def parseOptions(argv):
    opt = StartOptions()
    try:
        opt.parseOptions(argv[1:])
    except usage.UsageError, e:
        raise SystemExit(str(e))
    return opt


def main(argv):
    opt = parseOptions(argv)
    i = imagemodel.ImageModel(opt.location, 
                              width=opt['width'], height=opt['height'],
                              noexit=opt['noexit'], switchKeys=opt['switch-keys'])
    i.run()

if __name__ == '__main__':
    main(sys.argv)
