#!/usr/bin/env python3
"""Generate docs/catalog.json from catalog.yaml for local development.

Usage:
    python3 scripts/build-catalog.py
    cd docs && python3 -m http.server 8080
"""
import json
import os
import subprocess
import sys

try:
    import yaml
    def load_yaml(path):
        with open(path) as f:
            return yaml.safe_load(f)
except ImportError:
    # Fallback: use yq (available on NixOS / many Linux distros)
    def load_yaml(path):
        try:
            result = subprocess.run(['yq', '.', path], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (FileNotFoundError, subprocess.CalledProcessError):
            sys.exit("PyYAML or yq is required. Install one:\n  pip install pyyaml\n  brew install yq")

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src  = os.path.join(root, 'catalog.yaml')
dst  = os.path.join(root, 'docs', 'catalog.json')

data = load_yaml(src)

with open(dst, 'w') as f:
    json.dump(data, f, indent=2)

n = len(data.get('entries', []))
print(f"Wrote {n} entries → {os.path.relpath(dst, root)}")
print(f"\nServe locally:")
print(f"  cd docs && python3 -m http.server 8080")
print(f"  open http://localhost:8080")
