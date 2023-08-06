"""
Framework for manipulating bundles for airgapped transfers.
"""
import sys
from pathlib import Path
from platform import python_version
from typing import List

from typer import Argument, Option, Typer, echo  # pylint: disable=unused-import

from hoppr import __version__
from hoppr.configs.credentials import Credentials
from hoppr.configs.manifest import Manifest
from hoppr.configs.transfer import Transfer
from hoppr.processor import HopprProcessor

app = Typer()


@app.command()
def bundle(
    manifest_file: Path = Argument(
        "manifest.yml",
        help="Path to manifest file file.  Default is manifest.yml in your local directory.",
        expose_value=True,
    ),
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
):
    """
    Run the stages specified in the transfer config file on the
    content specified in the manifest
    """
    metadata_files = [manifest_file, transfer_file]

    if credentials_file is not None:
        Credentials.load_file(credentials_file)
        metadata_files.append(credentials_file)

    manifest = Manifest.load_file(manifest_file)

    transfer = Transfer.load_file(transfer_file)

    processor = HopprProcessor(transfer, manifest)
    processor.metadata_files = metadata_files

    result = processor.run()
    if result.is_fail():
        sys.exit(1)


@app.command()
def version():
    """
    Print version information for `hoppr`
    """
    echo(f"Hoppr Framework Version: {__version__}")
    echo(f"Python Version: {python_version()}")


@app.command()
def validate(
    input_files: List[Path],
    credentials_config_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify authorization config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_config_file: Path = Option(
        None,
        help="Specify transfer config for services",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
):
    """
    Validate multiple manifest files for schema errors.
    """

    cred_config = None
    transfer_config = None  # pylint: disable="unused-variable"
    manifests = []  # pylint: disable="unused-variable"

    if credentials_config_file is not None:
        cred_config = Credentials.load_file(credentials_config_file)
    if transfer_config_file is not None:
        transfer_config = Transfer.load_file(transfer_config_file)

    manifests = [Manifest.load_file(file, cred_config) for file in input_files]


if __name__ == "__main__":  # pragma: no cover
    app()
