#!/usr/bin/env python3
"""
notes.py — простой CLI для заметок.

Хранилище: JSON-файл рядом со скриптом (data.json).
Пока реализована только команда "add".
"""

import argparse
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def load_notes():
    """Загружает список заметок из файла. Если файла нет — возвращает пустой список."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    """Сохраняет список заметок в файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def cmd_add(args):
    notes = load_notes()
    new_id = (max((n["id"] for n in notes), default=0)) + 1
    notes.append({"id": new_id, "text": args.text})
    save_notes(notes)
    print(f"Заметка #{new_id} добавлена.")


def build_parser():
    parser = argparse.ArgumentParser(prog="notes", description="Простой менеджер заметок")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="добавить новую заметку")
    add_parser.add_argument("text", help="текст заметки")
    add_parser.set_defaults(func=cmd_add)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
