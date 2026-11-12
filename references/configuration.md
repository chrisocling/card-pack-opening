# 配置

`scripts/build_preview.py` 读取 `assets/default-config.json`，再用 `--config` 的顶层字段覆盖默认值。省略的顶层字段沿用默认配置；提供 `cards` 时会替换整个卡片列表。脚本会校验所有字段，写错时报出具体位置。

```bash
python3 <skill目录>/scripts/build_preview.py --config ./pack.json --output ./card-pack-preview.html
```

加 `--fragment` 可输出用于嵌入的 HTML 片段；默认输出完整网页。脚本只需要 Python 3 标准库，不依赖 npm。

## 基本字段

| 字段 | 类型与取值 | 用途 |
| --- | --- | --- |
| `title` | 字符串 | 舞台左上角主标题 |
| `subtitle` | 字符串 | 主标题下的说明 |
| `packTitle` | 字符串 | 卡包上的主文字 |
| `packSubtitle` | 字符串 | 卡包上的副文字 |
| `series` | 字符串 | 卡包底部的系列标识 |
| `cardLabel` | 可选字符串 | 卡片左上角编号前的文字；省略时使用 `packSubtitle`，设为 `""` 则只显示编号 |
| `packColors` | 1–6 个 `{name, label, color}` | 右上角可选的卡包颜色；`color` 为 CSS 颜色，深色渐变自动生成；只有一种颜色时隐藏选择器 |
| `packColor` | 字符串 | 初始卡包颜色：`packColors` 里的 `name`，或直接写一个颜色（如 `#10b981`，会自动加入选择器） |
| `packImage` | 可选，本地图片路径 | 替换内置卡包图像 |
| `speed` | 数值，`0.5`–`2` | 开包演出播放倍率；`1` 为原速 |
| `sound` | `true` / `false` | 默认是否开启音效；用户在页面上切换后，以浏览器保存的偏好为准 |
| `cards` | 卡片对象列表 | 固定模式下是要展示的卡（1–10 张）；随机模式下是卡池（1–100 张） |

每张卡片使用以下字段：

| 字段 | 类型与取值 | 用途 |
| --- | --- | --- |
| `name` | 非空字符串 | 卡名 |
| `tagline` | 字符串 | 卡片的短说明 |
| `rarity` | `common`、`rare`、`epic`、`legendary`；省略为 `common` | 稀有度：决定卡面样式、出场特效和随机模式下的概率分组 |
| `art` | `orb`、`planet`、`cube`、`gem`、`star` | 内置角色图案 |
| `color` | CSS 颜色字符串，例如 `#e8b0ff` | 卡片主题色；所有稀有度都会以它为底色调 |
| `image` | 可选，本地图片路径 | 使用自定义卡面图片；省略时使用 `art` |

`image` 和 `packImage` 接受 PNG、JPG/JPEG、WebP 或 GIF，单张不超过 3 MB。相对路径以配置 JSON 所在目录为基准，也可使用绝对路径；脚本将图片嵌入 HTML，移动成品后不需要保留原图片。图片请传本地文件，不使用网页图片 URL。

## 抽卡规则

| 字段 | 类型与取值 | 用途 |
| --- | --- | --- |
| `mode` | `random`（默认）或 `fixed` | `random`：每包从卡池随机抽取；`fixed`：按 `cards` 顺序展示全部卡片 |
| `packSize` | 整数 `1`–`10`，默认 `5` | 随机模式下每包张数 |
| `rates` | `{稀有度: 权重}` | 每张卡独立抽取时各稀有度的权重，自动换算为百分比；同一稀有度内的卡等概率 |
| `guarantee` | 稀有度或 `null` | 每包至少一张该稀有度或更高；没有时替换本包最低的一张 |
| `pity` | `{"rarity": "legendary", "packs": 20}` 或 `null` | 连续 `packs` 包都没出该稀有度时，第 `packs` 包必出；计数保存在浏览器 localStorage |
| `rarityNames` | `{common, rare, epic, legendary}` 映射到字符串 | 卡面、状态栏和概率公示中显示的稀有度名称，例如改成“普通／稀有／史诗／传说” |

随机模式下，右上角“概率”按钮会公示单张概率、`guarantee` 和 `pity` 规则；底部显示距离保底还有几包。结果按稀有度从低到高排列。

只换卡池、没有写 `rates` 时，默认概率会自动去掉卡池里没有的稀有度；`guarantee`、`pity` 不满足时自动关闭。自己写了 `rates` 时，脚本会严格检查：权重大于 0 的稀有度必须在卡池里有卡。

## 文案 `labels`

`labels` 只需写要改的项，其余沿用默认中文。`{…}` 是会被替换的变量。

| 键 | 默认值 | 出现位置 |
| --- | --- | --- |
| `hint` | 向右滑动，撕开卡包 | 卡包下方提示 |
| `packAria` | 卡包。按住向右滑动撕开，也可以按右方向键 | 读屏软件读到的卡包说明 |
| `nudge` | 点一下撕不开哦，按住向右滑动试试 | 单击卡包后的状态栏 |
| `keyNudge` | 按右方向键 → 就能撕开 | 键盘 Enter/空格后的状态栏 |
| `sealed` | {count} 张小小惊喜，等你拆开 | 未开包时的状态栏 |
| `tearing` | 继续向右，快撕开了 | 撕到一半时 |
| `opening` | 撕开一点，快乐多一点 | 开包演出中 |
| `revealed` | {count} 张小小惊喜，全部收好 | 结果中没有史诗及以上时 |
| `best` | 出现了 {rarity} · {name}！ | 结果中有史诗或传说时 |
| `selected` | {name} · {rarity} | 选中卡片时 |
| `again` | 再开一包 | 结果下方按钮 |
| `rates` | 概率 | 右上角按钮 |
| `ratesTitle` | 概率公示 | 概率面板标题 |
| `ratesNote` | 每张卡独立抽取，以上为单张概率；保底会提高实际出率。 | 概率面板说明 |
| `guarantee` | 每包至少 1 张 {rarity} 或更高 | 概率面板 |
| `pity` | 连续 {packs} 包内必出 {rarity} | 概率面板 |
| `pityLeft` | 距离 {rarity} 保底还有 {left} 包 | 底部保底进度 |
| `sound` | 音效 | 音效按钮的无障碍名称 |
| `colors` | 卡包颜色 | 颜色选择器的无障碍名称 |
| `summary` | 本包卡片：{names}。 | 读屏软件播报的结果 |

## 示例

随机抽卡、自定义卡池与中文稀有度：

```json
{
  "title": "星光卡包",
  "subtitle": "每包 5 张，祝你好运",
  "packTitle": "STAR",
  "packSubtitle": "STAR FRIENDS",
  "series": "SERIES 02",
  "packColors": [
    {"name": "night", "label": "夜空蓝", "color": "#1f3fd1"},
    {"name": "sakura", "label": "樱花粉", "color": "#e94a93"},
    {"name": "mint", "label": "薄荷绿", "color": "#10b981"}
  ],
  "packColor": "night",
  "mode": "random",
  "packSize": 5,
  "rates": {"common": 62, "rare": 28, "epic": 8, "legendary": 2},
  "guarantee": "rare",
  "pity": {"rarity": "legendary", "packs": 30},
  "rarityNames": {"common": "普通", "rare": "稀有", "epic": "史诗", "legendary": "传说"},
  "labels": {"hint": "按住向右撕开", "again": "再来一包"},
  "cards": [
    {"name": "Blip", "tagline": "A small spark of joy.", "rarity": "common", "art": "orb", "color": "#ffb59e"},
    {"name": "Cubit", "tagline": "A different angle.", "rarity": "common", "art": "cube", "color": "#c3e9a4"},
    {"name": "Ringo", "tagline": "Around and around.", "rarity": "rare", "art": "planet", "color": "#6372f1"},
    {"name": "Facet", "tagline": "Made to catch the light.", "rarity": "epic", "art": "gem", "color": "#a472df"},
    {"name": "Nova", "tagline": "Your brightest find.", "rarity": "legendary", "art": "star", "color": "#f3d26c", "image": "images/nova.png"}
  ]
}
```

固定展示、不随机（贴近参考视频）：

```json
{
  "mode": "fixed",
  "cards": [
    {"name": "Blip", "rarity": "common", "art": "orb", "color": "#ff987b"},
    {"name": "Ringo", "rarity": "rare", "art": "planet", "color": "#6372f1"},
    {"name": "Cubit", "rarity": "common", "art": "cube", "color": "#b7e75c"},
    {"name": "Facet", "rarity": "epic", "art": "gem", "color": "#a472df"},
    {"name": "Nova", "rarity": "legendary", "art": "star", "color": "#f3d26c"}
  ]
}
```

默认配置中的概率与保底仅用于演示。用于真实抽卡商品时，请让用户确认概率并如实公示。
