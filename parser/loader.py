#!/usr/bin/env python3
"""
Simple loader + validator for ConnectScript project JSON.

Usage: python parser/loader.py path/to/project.json

Performs:
- JSON schema validation using spec/project.schema.json
- Semantic checks: unique names, referential integrity

Outputs JSON-formatted diagnostics and exit code 0 on success.
"""
import json
import sys
from pathlib import Path
from jsonschema import validate, Draft7Validator, exceptions as jsexc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'spec' / 'project.schema.json'


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_schema():
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def schema_validate(instance, schema):
    validator = Draft7Validator(schema)
    errors = []
    for err in validator.iter_errors(instance):
        errors.append({
            'path': '/'.join(map(str, err.path)),
            'message': err.message
        })
    return errors


def semantic_checks(instance):
    errs = []

    # pages: unique names
    pages = instance.get('pages', [])
    page_names = [p.get('name') for p in pages]
    dup_pages = set([n for n in page_names if page_names.count(n) > 1])
    for d in dup_pages:
        errs.append({'path': 'pages', 'message': f"Duplicate page name: {d}"})

    # elements unique per page, and check element names
    for i, p in enumerate(pages):
        elems = p.get('elements', [])
        names = [e.get('name') for e in elems]
        dup = set([n for n in names if names.count(n) > 1])
        for d in dup:
            errs.append({'path': f'pages[{i}].elements', 'message': f"Duplicate element name in page {p.get('name')}: {d}"})

    # scripts unique names
    scripts = instance.get('scripts', {})
    script_names = list(scripts.keys())
    dup_scripts = set([n for n in script_names if script_names.count(n) > 1])
    for d in dup_scripts:
        errs.append({'path': 'scripts', 'message': f"Duplicate script name: {d}"})

    # triggers reference elements/pages
    page_map = {p.get('name'): p for p in pages}
    for sname, script in scripts.items():
        triggers = script.get('triggers', [])
        for t in triggers:
            ttype = t.get('type')
            target = t.get('target')
            if ttype == 'click' and target:
                # ensure element exists in some page
                found = False
                for p in pages:
                    for e in p.get('elements', []):
                        if e.get('name') == target:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    errs.append({'path': f'scripts.{sname}.triggers', 'message': f"Trigger target not found: {target}"})

    # asset references: background.imageRef and element.properties.source
    assets = instance.get('assets', {})
    asset_keys = set(assets.keys())
    for i, p in enumerate(pages):
        bg = p.get('background') or {}
        if bg.get('imageRef') and bg.get('imageRef') not in asset_keys:
            errs.append({'path': f'pages[{i}].background', 'message': f"Background imageRef not found in assets: {bg.get('imageRef')}"})
        for j, e in enumerate(p.get('elements', [])):
            props = e.get('properties') or {}
            # image source may reference asset id
            if e.get('type') == 'image' and props.get('source') and props.get('source') not in asset_keys:
                errs.append({'path': f'pages[{i}].elements[{j}]', 'message': f"Image source not found in assets: {props.get('source')}"})

    return errs


def main():
    if len(sys.argv) < 2:
        print('Usage: loader.py path/to/project.json')
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({'ok': False, 'errors': [{'message': 'File not found'}]}))
        sys.exit(2)

    try:
        instance = load_json(path)
    except Exception as e:
        print(json.dumps({'ok': False, 'errors': [{'message': f'Invalid JSON: {e}'}]}))
        sys.exit(2)

    schema = load_schema()
    s_errors = schema_validate(instance, schema)
    sem_errors = semantic_checks(instance)

    all_errors = s_errors + sem_errors
    out = {'ok': len(all_errors) == 0, 'errors': all_errors}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out['ok'] else 3)


if __name__ == '__main__':
    main()
