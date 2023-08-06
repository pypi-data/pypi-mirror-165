import argparse

from .server import run
from .module_manager import CadQueryModuleManager


DEFAULT_PORT = 5000
DEFAULT_DIR = '.'
DEFAULT_MODULE = 'main'
DEFAULT_OBJECT_VAR = 'result'


def parse_args():
    parser = argparse.ArgumentParser(
            description='A web server that renders a 3d model of a CadQuery script loaded dynamically.')

    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
        help='Server port (default: %d).' % DEFAULT_PORT)
    parser.add_argument('-d', '--dir', default=DEFAULT_DIR,
        help='Path of the directory containing CadQuery scripts (default: "%s").' % DEFAULT_DIR)
    parser.add_argument('-m', '--module', default=DEFAULT_MODULE, metavar='MOD',
        help='Default Python module to load (default: "%s").' % DEFAULT_MODULE)
    parser.add_argument('-o', '--object', default=DEFAULT_OBJECT_VAR, metavar='OBJ',
        help='Default rendered object variable name (default: "%s").' % DEFAULT_OBJECT_VAR)

    return parser.parse_args()


def main():
    args = parse_args()
    module_manager = CadQueryModuleManager(args.dir, args.module, args.object)
    run(args.port, module_manager)


if __name__ == '__main__':
    main()
