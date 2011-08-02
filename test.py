#!/usr/bin/env python

import imagemodel, sys
from twisted.python import usage


class StartOptions(usage.Options):
    def getSynopsis(self):        
        return """Usage: %s <options>"""

    optParameters = [
            ('width', 'w', 1024, 'Width of screen'),
            ('height', 'h', 768, 'Height of screen'),
            ('location', 'i', None, 'Location of pictures'),
            ]

def parseOptions(argv):
    opt = StartOptions()
    try:
        opt.parseOptions(argv[1:])
    except UsageError, e:
        raise SystemExit(str(e))
    return opt


def main(argv):
    opt = parseOptions(argv)
    #i = imagemodel.ImageModel(['/Users/dave/Pictures/Backgrounds'])
    #i.run()

if __name__ == '__main__':
    main(sys.argv)
