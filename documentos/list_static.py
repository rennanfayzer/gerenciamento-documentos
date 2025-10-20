#!/usr/bin/env python3
import os
import sys
from collections import defaultdict

def find_static_dirs(project_root):
    candidates = [
        os.path.join(project_root, 'gestao_docs', 'static'),
        os.path.join(project_root, 'static'),
        os.path.join(project_root, 'staticfiles'),
    ]
    return [d for d in candidates if os.path.isdir(d)]

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"\nProject root: {project_root}\n")

    static_dirs = find_static_dirs(project_root)
    if not static_dirs:
        print("⚠️  Nenhuma pasta estática encontrada! Verifique os caminhos em `find_static_dirs()`.")
        sys.exit(1)

    print("Pastas estáticas detectadas:")
    for d in static_dirs:
        print("  -", d)
    print()

    # map rel_path -> [full_paths]
    duplicates = defaultdict(list)
    for st in static_dirs:
        for root, _, files in os.walk(st):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, st).replace(os.path.sep, '/')
                duplicates[rel].append(full)

    found = False
    print("Arquivos estáticos DUPLICADOS:\n")
    for rel, paths in sorted(duplicates.items()):
        if len(paths) > 1:
            found = True
            print(rel)
            for p in paths:
                print("  -", p)
            print()

    if not found:
        print("✅ Nenhum duplicado encontrado.\n")

if __name__ == '__main__':
    main()
