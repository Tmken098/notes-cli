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


def cmd_list(args):
    notes = load_notes()
    if not notes:
        print("Заметок пока нет")
        return []
    for i in notes:
        print(f"#{i['id']}: {i['text']}")


def cmd_delete(args):
    notes = load_notes()
    index = next((i for i, n in enumerate(notes) if n["id"] == args.id), None)
    if index is None:
        print(f"Заметка #{args.id} не найдена.")
        return
    notes.pop(index)
    save_notes(notes)
    print(f"Заметка #{args.id} удалена.")


def cmd_edit(args):
    notes = load_notes()
    index = next((i for i, n in enumerate(notes) if n["id"] == args.id), None)
    if index is None:
        print(f"Заметка #{args.id} не найдена.")
        return
    notes[index]["text"] = args.text
    save_notes(notes)
    print(f"Заметка #{args.id} обновлена.")
    

def build_parser():
    parser = argparse.ArgumentParser(prog="notes", description="Простой менеджер заметок")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="добавить новую заметку")
    add_parser.add_argument("text", help="текст заметки")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="посмотреть все заметки")
    list_parser.set_defaults(func=cmd_list)
    
    delete_parser = subparsers.add_parser("delete", help="удалить заметку")
    delete_parser.add_argument("id", help="id заметки", type=int)
    delete_parser.set_defaults(func=cmd_delete)
       
    edit_parser = subparsers.add_parser('edit', help="редактировать заметку")
    edit_parser.add_argument("id", help="id заметки", type=int)
    edit_parser.add_argument("text", help="новый текст заметки")
    edit_parser.set_defaults(func=cmd_edit)   
       
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
