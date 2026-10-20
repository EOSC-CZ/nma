#!/usr/bin/env python3
"""Validate records from a JSONL file against the datasets model.

Each record's metadata is loaded through the service marshmallow schema and
all relations (vocabulary references) are dereferenced to check pid values.
"""

import json

import click
from tqdm import tqdm


def flatten_errors(errors, prefix=""):
    """Flatten nested marshmallow error messages into (path, message) pairs."""
    if isinstance(errors, dict):
        for key, value in errors.items():
            yield from flatten_errors(value, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(errors, list):
        for value in errors:
            yield from flatten_errors(value, prefix)
    else:
        yield prefix, errors


def lookup(data, path):
    """Return the value at a dotted path (list indices as numbers), or "<missing>"."""
    for key in path.split("."):
        try:
            data = data[int(key)] if isinstance(data, list) else data[key]
        except (KeyError, IndexError, ValueError, TypeError):
            return "<missing>"
    return data


def is_dump_only(schema, path):
    """Return True if the schema field at a dotted error path is dump_only.

    API responses contain dump_only fields (e.g. dereferenced affiliation
    identifiers); loading them reports "Unknown field." but they are just
    dropped, so such errors are not real problems.
    """
    from marshmallow import fields

    field = None
    for key in path.split("."):
        if key.isdigit():
            continue
        if field is not None:
            while isinstance(field, fields.List):
                field = field.inner
            if not isinstance(field, fields.Nested):
                return False
            schema = field.schema
        field = schema.fields.get(key)
        if field is None:
            return False
    return field.dump_only


def validate_record(data, service, record_cls, identity, schema):
    problems = []
    metadata = {"metadata": data.get("metadata", {})}

    _, errors = service.schema.load(metadata, context={"identity": identity}, raise_errors=False)
    for error in errors or []:
        # service schema errors come as {"field": "a.b.c", "messages": [...] or {...}}
        if isinstance(error, dict) and "field" in error:
            flat = flatten_errors(error["messages"], error["field"])
        else:
            flat = flatten_errors(error)
        problems.extend(
            f"marshmallow: {path}: {msg} value={json.dumps(lookup(metadata, path), ensure_ascii=False)}"
            for path, msg in flat
            if not is_dump_only(schema, path)
        )

    record = record_cls(metadata)
    for name in record.relations:
        try:
            # validate checks that each referenced pid exists
            record.relations.validate(fields=[name])
        except Exception as e:
            problems.append(f"relation {name}: {type(e).__name__}: {e}")

    return problems


@click.command(help=__doc__)
@click.argument("input", type=click.File("r", encoding="utf-8"))
@click.option("--model", default="datasets", show_default=True, help="Model name")
def main(input, model):
    from invenio_access.permissions import system_identity
    from invenio_app.factory import create_app
    from oarepo_runtime.proxies import current_runtime

    app = create_app()
    with app.app_context():
        service = current_runtime.models[model].service
        record_cls = service.config.record_cls
        schema = service.schema.schema()

        total = invalid = 0
        for line in tqdm(input, unit="rec"):
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            total += 1
            problems = validate_record(data, service, record_cls, system_identity, schema)
            if problems:
                invalid += 1
                tqdm.write(data.get("id", "<no id>"))
                for problem in problems:
                    tqdm.write(f"    {problem}")

        click.echo(f"{invalid}/{total} records have problems", err=True)


if __name__ == "__main__":
    main()
