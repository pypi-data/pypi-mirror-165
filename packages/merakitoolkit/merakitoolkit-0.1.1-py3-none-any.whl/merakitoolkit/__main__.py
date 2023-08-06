"""
merakitoolkit main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main program executable
"""

# standard libraries
import sys

# additional libraries
import merakitoolkit
from merakitoolkitparser import parser


def main() -> int:
    '''merakitoolkit main program call'''

    mainparser,return_code = parser()
    if mainparser:
        if mainparser.command == "psk":
            merakiobj = merakitoolkit.MerakiToolkit(vars(mainparser))
            merakiobj.pskchange()
            merakiobj.send_email_psk()
    return return_code

if __name__ == "__main__":
    sys.exit(main())
