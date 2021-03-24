"""HIDSEGUS: A Host Intrusion Detection Systems made in python by INSEGUS ST 12 2020-21"""
import cmd2
from cmd2.constants import (
    MULTILINE_TERMINATOR,
)

class HIDSegus(cmd2.Cmd):
    """HIDSEGUS: A Host Intrusion Detection Systems made in python by INSEGUS ST 12 2020-21"""
    
    def __init__(self):
        """Initialize the base class as well as this one"""
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        super().__init__(multiline_commands=[], terminators=[], shortcuts={})

        # prompts and defaults
        self.prompt = 'HIDSEGUS >'
    
    def do_pdp_hash(self, args):
        """Generate a homomorphic hash of a file"""

        arg_parser = argparse.ArgumentParser()
        yo_parser.add_argument('filepath', help='filepath')
        self.poutput("Quiterrr!")


if __name__ == '__main__':
    import sys
    cli = HIDSegus()
    sys.exit(cli.cmdloop())