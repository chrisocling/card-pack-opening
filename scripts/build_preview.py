#!/usr/bin/env python3
"""Build a portable pack-opening preview from a JSON configuration."""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
RARITIES = ('common', 'rare', 'epic', 'legendary')
ARTS = ('orb', 'planet', 'cube', 'gem', 'star')
MODES = ('fixed', 'random')
LABEL_KEYS = {
    'hint', 'packAria', 'nudge', 'keyNudge', 'sealed', 'tearing', 'opening', 'revealed', 'best', 'selected',
    'again', 'rates', 'ratesTitle', 'ratesNote', 'guarantee', 'pity', 'pityLeft', 'sound', 'colors', 'summary',
}
TEXT_FIELDS = ('title', 'subtitle', 'packTitle', 'packSubtitle', 'series', 'cardLabel')
MAX_IMAGE_BYTES = 3 * 1024 * 1024
COLOR_RE = re.compile(
    r'^(#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})'
    r'|(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch)\([^;{}<>]*\)'
    r'|[a-zA-Z]{3,30})$'
)


def fail(message: str) -> None:
    raise ValueError(message)


def is_color(value: object) -> bool:
    return isinstance(value, str) and bool(COLOR_RE.match(value.strip()))


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def image_data(value: object, base: Path, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f'{where} must be a local image path.')
    if value.startswith('data:image/'):
        return value
    if '://' in value:
        fail(f'{where}: images must be local files or data:image URLs, not web links.')
    source = Path(value).expanduser()
    if not source.is_absolute():
        source = base / source
    mime = mimetypes.guess_type(source)[0]
    if not mime or not mime.startswith('image/') or mime == 'image/svg+xml':
        fail(f'{where}: use a PNG, JPEG, WebP or GIF image: {value}')
    if not source.is_file():
        fail(f'{where}: image not found: {source}')
    size = source.stat().st_size
    if size > MAX_IMAGE_BYTES:
        fail(f'{where}: {source.name} is {size / 1048576:.1f} MB; compress it below {MAX_IMAGE_BYTES // 1048576} MB.')
    return f'data:{mime};base64,' + base64.b64encode(source.read_bytes()).decode()


def rank(rarity: str) -> int:
    return RARITIES.index(rarity)


def validate(config: dict, base: Path, supplied: set[str]) -> None:
    """Check fields strictly when the user wrote them; adapt defaults quietly to the user's card pool."""
    for field in TEXT_FIELDS:
        if field in config and not isinstance(config[field], str):
            fail(f'{field} must be a string.')
    if 'speed' in config and (not is_number(config['speed']) or not 0.5 <= config['speed'] <= 2):
        fail('speed must be a number from 0.5 to 2.')
    if 'sound' in config and not isinstance(config['sound'], bool):
        fail('sound must be true or false.')

    mode = config.get('mode', 'fixed')
    if mode not in MODES:
        fail(f'mode must be one of: {", ".join(MODES)}.')
    config['mode'] = mode

    cards = config.get('cards')
    limit = 100 if mode == 'random' else 10
    if not isinstance(cards, list) or not 1 <= len(cards) <= limit:
        fail(f'Provide 1 to {limit} cards in {mode} mode.')
    for index, card in enumerate(cards, start=1):
        where = f'cards[{index}]'
        if not isinstance(card, dict) or not isinstance(card.get('name'), str) or not card['name'].strip():
            fail(f'{where} requires a non-empty name.')
        if 'tagline' in card and not isinstance(card['tagline'], str):
            fail(f'{where}.tagline must be a string.')
        card.setdefault('rarity', 'common')
        if card['rarity'] not in RARITIES:
            fail(f'{where}.rarity must be one of: {", ".join(RARITIES)} (got {card["rarity"]!r}).')
        if 'art' in card and card['art'] not in ARTS:
            fail(f'{where}.art must be one of: {", ".join(ARTS)} (got {card["art"]!r}).')
        if 'color' in card and not is_color(card['color']):
            fail(f'{where}.color must be a CSS color such as #ff6699 (got {card["color"]!r}).')
        if card.get('image'):
            card['image'] = image_data(card['image'], base, f'{where}.image')

    present = {card['rarity'] for card in cards}

    def has_at_least(rarity: str) -> bool:
        return any(rank(r) >= rank(rarity) for r in present)

    if mode == 'random':
        if 'rates' not in supplied and isinstance(config.get('rates'), dict):
            config['rates'] = {r: v for r, v in config['rates'].items() if r in present} or {r: 1 for r in present}
        if 'guarantee' not in supplied and config.get('guarantee') and not has_at_least(config['guarantee']):
            config['guarantee'] = None
        if 'pity' not in supplied and isinstance(config.get('pity'), dict) and not has_at_least(config['pity'].get('rarity', 'legendary')):
            config['pity'] = None
        size = config.get('packSize', 5)
        if not isinstance(size, int) or isinstance(size, bool) or not 1 <= size <= 10:
            fail('packSize must be an integer from 1 to 10.')
        rates = config.get('rates')
        if not isinstance(rates, dict) or not rates:
            fail('random mode needs rates, e.g. {"common": 60, "rare": 27, "epic": 10, "legendary": 3}.')
        for rarity, value in rates.items():
            if rarity not in RARITIES:
                fail(f'rates.{rarity} is not a rarity; use {", ".join(RARITIES)}.')
            if not is_number(value) or value < 0:
                fail(f'rates.{rarity} must be a number >= 0.')
            if value > 0 and rarity not in present:
                fail(f'rates.{rarity} is {value} but no card has rarity "{rarity}".')
        if not any(value > 0 for value in rates.values()):
            fail('At least one rate must be greater than 0.')
        guarantee = config.get('guarantee')
        if guarantee is not None:
            if guarantee not in RARITIES:
                fail(f'guarantee must be null or one of: {", ".join(RARITIES)}.')
            if not has_at_least(guarantee):
                fail(f'guarantee is "{guarantee}" but no card is {guarantee} or rarer.')
        pity = config.get('pity')
        if pity is not None:
            if not isinstance(pity, dict) or pity.get('rarity') not in RARITIES:
                fail('pity must be null or {"rarity": "legendary", "packs": 20}.')
            packs = pity.get('packs')
            if not isinstance(packs, int) or isinstance(packs, bool) or not 1 <= packs <= 1000:
                fail('pity.packs must be an integer from 1 to 1000.')
            if not has_at_least(pity['rarity']):
                fail(f'pity.rarity is "{pity["rarity"]}" but no card is {pity["rarity"]} or rarer.')

    colors = config.get('packColors')
    if not isinstance(colors, list) or not 1 <= len(colors) <= 6:
        fail('packColors must list 1 to 6 colors, e.g. [{"name": "blue", "label": "蓝色", "color": "#233feb"}].')
    names = set()
    for index, item in enumerate(colors, start=1):
        where = f'packColors[{index}]'
        if not isinstance(item, dict) or not isinstance(item.get('name'), str) or not item['name'].strip():
            fail(f'{where} requires a name.')
        if item['name'] in names:
            fail(f'{where}.name "{item["name"]}" is used twice.')
        names.add(item['name'])
        if not is_color(item.get('color')):
            fail(f'{where}.color must be a CSS color such as #233feb.')
        if 'label' in item and not isinstance(item['label'], str):
            fail(f'{where}.label must be a string.')
    choice = config.get('packColor', colors[0]['name'])
    if not isinstance(choice, str):
        fail('packColor must be a string.')
    if choice not in names:
        if not is_color(choice):
            fail(f'packColor must be one of {sorted(names)} or a CSS color (got {choice!r}).')
        colors.insert(0, {'name': 'custom', 'label': '自定义卡包', 'color': choice})
        choice = 'custom'
    config['packColor'] = choice

    labels = config.get('labels', {})
    if not isinstance(labels, dict):
        fail('labels must be an object of text strings.')
    for key, value in labels.items():
        if key not in LABEL_KEYS:
            fail(f'labels.{key} is not a known label; see references/configuration.md.')
        if not isinstance(value, str):
            fail(f'labels.{key} must be a string.')
    names_map = config.get('rarityNames', {})
    if not isinstance(names_map, dict) or any(k not in RARITIES or not isinstance(v, str) for k, v in names_map.items()):
        fail('rarityNames must map common/rare/epic/legendary to strings.')

    if config.get('packImage'):
        config['packImage'] = image_data(config['packImage'], base, 'packImage')


def build(config_path: Path | None, output: Path, fragment: bool) -> None:
    config = json.loads((SKILL_ROOT / 'assets' / 'default-config.json').read_text(encoding='utf-8'))
    base = SKILL_ROOT / 'assets'
    supplied_keys: set[str] = set()
    if config_path:
        supplied = json.loads(config_path.read_text(encoding='utf-8'))
        if not isinstance(supplied, dict):
            fail('Configuration must be a JSON object.')
        config.update(supplied)
        supplied_keys = set(supplied)
        base = config_path.parent
    validate(config, base, supplied_keys)
    # Escape HTML parser delimiters even though the data is never rendered as markup.
    encoded = json.dumps(config, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    content = (SKILL_ROOT / 'assets' / 'pack-opening.html').read_text(encoding='utf-8').replace('__PACK_CONFIG_JSON__', encoded)
    if not fragment:
        content = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>卡包抽卡</title><style>html,body{margin:0;min-height:100%;background:#f6f6f2}body{display:grid;place-items:center;min-height:100svh;padding:24px 0;box-sizing:border-box}</style></head><body>\n' + content + '\n</body></html>\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')
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
