#!/usr/bin/env python3
"""Build a portable pack-opening preview from a JSON configuration."""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def image_data(value: str, base: Path) -> str:
    if value.startswith('data:image/'):
        return value
    if '://' in value:
        raise ValueError('Images must be local files or data:image URLs.')
    source = Path(value).expanduser()
    if not source.is_absolute():
        source = base / source
    mime = mimetypes.guess_type(source)[0]
    if not mime or not mime.startswith('image/') or mime == 'image/svg+xml':
        raise ValueError(f'Use a PNG, JPEG, WebP or GIF image: {value}')
    return f'data:{mime};base64,' + base64.b64encode(source.read_bytes()).decode()


def build(config_path: Path | None, output: Path, fragment: bool) -> None:
    config = json.loads((SKILL_ROOT / 'assets' / 'default-config.json').read_text())
    base = SKILL_ROOT / 'assets'
    if config_path:
        supplied = json.loads(config_path.read_text())
        if not isinstance(supplied, dict):
            raise ValueError('Configuration must be a JSON object.')
        config.update(supplied)
        base = config_path.parent
    cards = config.get('cards')
    if not isinstance(cards, list) or not 1 <= len(cards) <= 10:
        raise ValueError('Provide 1 to 10 cards.')
    for index, card in enumerate(cards):
        if not isinstance(card, dict) or not isinstance(card.get('name'), str) or not card['name'].strip():
            raise ValueError(f'Card {index + 1} requires a name.')
        if card.get('image'):
            card['image'] = image_data(card['image'], base)
    if config.get('packImage'):
        config['packImage'] = image_data(config['packImage'], base)
    for field in ('title', 'subtitle', 'packTitle', 'packSubtitle', 'series'):
        if field in config and not isinstance(config[field], str):
            raise ValueError(f'{field} must be a string.')
    if 'speed' in config and (isinstance(config['speed'], bool) or not isinstance(config['speed'], (int, float)) or not 0.5 <= config['speed'] <= 2):
        raise ValueError('speed must be a number from 0.5 to 2.')
    # Escape HTML parser delimiters even though the data is never rendered as markup.
    encoded = json.dumps(config, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    content = (SKILL_ROOT / 'assets' / 'pack-opening.html').read_text().replace('__PACK_CONFIG_JSON__', encoded)
    if not fragment:
        content = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>卡包抽卡</title><style>html,body{margin:0;min-height:100%;background:#edeee5}body{display:grid;place-items:center;min-height:100svh;padding:24px 0;box-sizing:border-box}</style></head><body>\n' + content + '\n</body></html>\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    print(output.resolve())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, help='Optional JSON; image paths are relative to this file.')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--fragment', action='store_true', help='Emit an inline HTML fragment instead of a full document.')
    args = parser.parse_args()
    try:
        build(args.config.resolve() if args.config else None, args.output, args.fragment)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
