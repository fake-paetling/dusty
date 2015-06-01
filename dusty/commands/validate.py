import logging

from schemer import Schema

from ..compiler.spec_assembler import get_specs_path, get_specs_from_path
from ..schemas import app_schema, bundle_schema, lib_schema

def _ensure_app_build_or_image(app):
    if 'image' in app and 'build' in app:
        raise ValidationException("Keys `image` and `build` are mutually exclusive")
    elif 'image' not in app and 'build' not in app:
        raise ValidationException("Each app must contain either an `image` or a `build` field")

def _validate_fields_with_schemer(specs):
    for app in specs.get('apps', []).values():
        app_schema.validate(app)
        _ensure_app_build_or_image(app)
    for bundle in specs.get('bundles', []).values():
        bundle_schema.validate(bundle)
    for lib in specs.get('libs', []).values():
        lib_schema.validate(lib)

def _validate_spec_names(specs):
    pass

def _validate_cycle_free(specs):
    pass

def validate_specs_from_path(specs_path):
    logging.info("Validating specs at path {}".format(specs_path))
    specs = get_specs_from_path(specs_path)
    _validate_fields_with_schemer(specs)
    _validate_spec_names(specs)
    _validate_cycle_free(specs)

def validate_specs():
    validate_specs_from_path(get_specs_path())
