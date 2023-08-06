from argparse import ArgumentParser
import logging
import os.path
import os
import sys

try:
    import chevron
    from prompt_toolkit.completion.filesystem import PathCompleter
    from prompt_toolkit import PromptSession
except ImportError as e:
    raise ImportError(
        "Library or libraries needed for building Windows service not found. "
        "Make sure you have installed this library with the windows_service "
        "extras, e.g. `pip install file-trigger[windows_service]` ",
        name=e.name,
        path=e.path,
    )

logging.basicConfig(
    level=logging.INFO, stream=sys.stderr, format="%(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

from .util.prompt_toolkit import FileExists, FileExistsUnder


def main(argv=sys.argv[1:]):
    check_build_environment()

    args = parse_args(argv)

    script_dir = os.path.dirname(__file__)
    templ_dir = os.path.join(script_dir, "template")
    dist_dir = os.path.abspath(args.dist_dir)  # relative to cwd

    os.makedirs(dist_dir, exist_ok=True)
    for fname in os.listdir(dist_dir):
        os.remove(os.path.join(dist_dir, fname))

    logger.info(f"Generating service scripts to {dist_dir}")
    generate_templates(templ_dir, dist_dir)
    logger.info("Generated service scripts")

    logger.info("Done.")


def parse_args(argv):
    parser = ArgumentParser(
        description="Build Windows service scripts (for use with nssm)"
    )
    parser.add_argument(
        "--dist-dir", default="./dist", help="Distribution directory (default: ./dist)"
    )
    return parser.parse_args(argv)


def generate_templates(templ_dir, output_dir):
    session = PromptSession()

    svc_name = session.prompt("Service name: ", default="file-trigger")
    svc_display_name = session.prompt("Service display name: ", default="File Trigger")
    svc_description = session.prompt(
        "Service description: ", default="Rules-based file watching"
    )
    virtual_env = session.prompt(
        "Run under virtualenv: ",
        default=os.path.relpath(get_virtualenv_root_dir()),
        validator=(
            FileExists(file_only=False)
            & FileExistsUnder(os.path.join("Scripts", "activate"))
        ),
        completer=PathCompleter(),
    )
    config_file = session.prompt(
        "Configuration file: ",
        validator=FileExists(file_only=True),
        completer=PathCompleter(),
    )
    nssm_exe = session.prompt(
        "NSSM executable: ",
        default=os.path.join("C:\\Windows", "System32", "nssm.exe"),
        validator=FileExists(file_only=True),
        completer=PathCompleter(),
    )

    data = {
        "svc_name": svc_name,
        "svc_display_name": svc_display_name,
        "svc_description": svc_description,
        "config_file": os.path.abspath(config_file),
        "virtualenv_root_dir": os.path.abspath(virtual_env),
        "nssm_exe": os.path.abspath(nssm_exe),
    }

    for fname in os.listdir(templ_dir):
        template = os.path.join(templ_dir, fname)
        output = os.path.join(output_dir, os.path.splitext(fname)[0])

        logger.info(f"Generating {output} from {template}")
        with open(template, "r") as inp, open(output, "w") as outp:
            outp.truncate()
            outp.write(chevron.render(inp, data, warn=True))

    logger.info("Done.")


def check_build_environment():
    """Note: nothing about this script is OS-dependent, so checks not needed."""
    pass


def get_virtualenv_root_dir():
    return sys.exec_prefix


if __name__ == "__main__":
    main()
