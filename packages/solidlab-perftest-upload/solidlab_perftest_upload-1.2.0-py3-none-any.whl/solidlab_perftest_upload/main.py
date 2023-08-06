import logging
import mimetypes
import sys
from typing import Optional

import requests
import click

from solidlab_perftest_common.upload_artifact import (
    upload_artifact_file,
    upload_artifact,
    validate_artifact_endpoint,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


@click.command()
@click.argument(
    "artifact_endpoint", type=click.STRING, callback=validate_artifact_endpoint
)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--mime-type",
    default=None,
    type=click.STRING,
    help="Mime-type of file (default: auto based on extension)",
)
@click.option(
    "-t",
    "--auth-token",
    required=False,
    help="Authentication token for talking to solidlab-perftest-server artifact endpoint",
)
@click.option(
    "--type",
    "attach_type",
    type=click.Choice(["GRAPH", "CSV", "LOG", "OTHER"], case_sensitive=False),
    prompt=True,
    help="Type of attachment",
)
@click.option("--sub-type", prompt=True, type=click.STRING, help="The subtype.")
@click.option("--description", prompt=True, help="Description of the file.")
def main(
    artifact_endpoint,
    filename,
    mime_type,
    attach_type,
    sub_type,
    description,
    auth_token: Optional[str],
) -> int:
    with requests.Session() as session:
        attachment_id, attachment_url = upload_artifact_file(
            session,
            artifact_endpoint=artifact_endpoint,
            attach_type=attach_type,
            sub_type=sub_type,
            description=description,
            filename=filename,
            content_type=mime_type,
            auth_token=auth_token,
        )
        click.echo(
            f"Uploaded: {sub_type} {attach_type} to {attachment_id} at {attachment_url}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix="PERFTEST_UPLOAD"))
