# 配置

`scripts/build_preview.py` 读取 `assets/default-config.json`，再用 `--config` 的顶层字段覆盖默认值。省略的顶层字段沿用默认配置；提供 `cards` 时会替换整个卡片列表。

```bash
python3 <skill目录>/scripts/build_preview.py --config ./pack.json --output ./card-pack-preview.html
```

加 `--fragment` 可输出用于嵌入的 HTML 片段；默认输出完整网页。脚本只需要 Python 3 标准库，不依赖 npm。

## 字段

| 字段 | 类型与取值 | 用途 |
| --- | --- | --- |
| `title` | 字符串 | 舞台主标题 |
| `subtitle` | 字符串 | 主标题下的说明 |
| `packTitle` | 字符串 | 卡包上的主文字 |
| `packSubtitle` | 字符串 | 卡包上的副文字 |
| `series` | 字符串 | 系列标识 |
| `packColor` | `blue` 或 `pink` | 内置 foil 卡包的初始配色，重开时保留当前所选颜色 |
| `packImage` | 可选，本地图片路径 | 替换内置卡包图像 |
| `speed` | 数值，`0.5`–`2` | 动画播放倍率；`1` 为原速，`0.5` 耗时约翻倍，`2` 耗时约减半 |
| `cards` | 1–10 个卡片对象 | 卡片内容和展示顺序；默认 5 张，贴近参考时保留 5 张；更多卡片或窄屏下自动换行 |

每张卡片使用以下字段：

| 字段 | 类型与取值 | 用途 |
| --- | --- | --- |
| `name` | 非空字符串 | 卡名 |
| `tagline` | 字符串 | 卡片的短说明 |
| `rarity` | `common`、`rare`、`epic`、`legendary` | 稀有度标签与样式 |
| `art` | `orb`、`planet`、`cube`、`gem`、`star` | 内置角色图案 |
| `color` | CSS 颜色字符串，例如 `#e8b0ff` | 卡片主题色 |
| `image` | 可选，本地图片路径 | 使用自定义卡面图片；省略时使用 `art` |

`image` 和 `packImage` 接受 PNG、JPG/JPEG、WebP 或 GIF。相对路径以配置 JSON 所在目录为基准，也可使用绝对路径；脚本将图片嵌入 HTML，移动成品后不需要保留原图片路径。图片请传本地文件，不使用网页图片 URL。

## 示例

以下配置保留默认五卡结构；替换为自己的卡名、颜色和本地图片即可：

```json
{
  "title": "A little magic inside.",
  "subtitle": "Tear open a fresh pack.",
  "packTitle": "holo",
  "packSubtitle": "COLLECTIBLE CARDS",
  "series": "SERIES 01",
  "packColor": "blue",
  "speed": 1,
  "cards": [
    { "name": "Blip", "tagline": "A small spark of joy.", "rarity": "common", "art": "orb", "color": "#c3e9a4" },
    { "name": "Ringo", "tagline": "Around and around.", "rarity": "rare", "art": "planet", "color": "#ffc4de" },
    { "name": "Cubit", "tagline": "A different angle.", "rarity": "rare", "art": "cube", "color": "#b8d9ff" },
    { "name": "Facet", "tagline": "Made to catch the light.", "rarity": "epic", "art": "gem", "color": "#d6c4ff" },
    { "name": "Nova", "tagline": "Your brightest find.", "rarity": "legendary", "art": "star", "color": "#ffe7a3" }
  ]
}
```

需要图片时，在相应卡片对象中添加 `"image": "images/blip.png"`，或在顶层添加 `"packImage": "images/pack.png"`。默认没有真实随机抽取：`cards` 的顺序就是展示顺序，`rarity` 不定义概率。
