import os
import uuid

from collections import OrderedDict
import humps
import jsonschema
import yaml

from vgs.sdk.serializers import dump_yaml
from vgs.sdk.utils import read_file
from vgscli.errors import SchemaValidationError, NoSuchFileOrDirectoryError
from vgscli.id_generator import uuid_to_base58


def dump_camelized_yaml(payload):
    """
    Transform snake_case to camelCase and dump as a yaml document.
    """
    return dump_yaml(OrderedDict(humps.camelize(payload))).rstrip()


def validate_yaml(file, schema_path, schema_root=os.path.dirname(__file__)):
    """
    Validates the file against the schema.

    Parameters
    ----------
    file: is the buffered content of the file
    schema_path: is the path relative to the working directory
    schema_root: was added to enable validating from different working directories like vgs-admin-cli-plugin
    """
    try:
        schema = read_file(schema_path, schema_root)
        file_content = yaml.full_load(file.read())

        jsonschema.validate(file_content, yaml.full_load(schema))

        return file_content
    except jsonschema.exceptions.ValidationError as e:
        raise SchemaValidationError(str(e))


def read_file(file_path, file_root=os.path.dirname(__file__)):
    full_path = os.path.join(file_root, file_path)
    try:
        with open(full_path, "r") as f:
            schema = f.read()
            f.close()
            return schema
    except FileNotFoundError:
        raise NoSuchFileOrDirectoryError(full_path)


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    # noinspection PyBroadException
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except Exception:
        return False

    return str(uuid_obj) == uuid_to_test


def format_org_id(org_id):
    if is_valid_uuid(org_id):
        org_id = uuid_to_base58(org_id, "AC")
    return org_id



