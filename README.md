# card-pack-opening · 卡包抽卡动画

一个 AI 编程助手 skill：生成可在浏览器直接打开的**拆卡包动画**。撕开卡包顶部、彩虹条带喷出、五张卡同时飞出再错峰排成一排，整体节奏约两秒；卡面、卡名、卡包和速度都能替换。

- 纯 HTML/CSS/JS 单文件成品，无需 npm、无需联网
- 点击卡包、向右撕包或按钮都能开包，开包中防重复触发
- 卡片悬停 3D 倾斜、可键盘聚焦，支持窄屏和 `prefers-reduced-motion`
- 可用本地图片替换卡面和卡包，图片会内嵌进 HTML

## 安装

把整个文件夹放进对应工具的 skills 目录：

```bash
# Codex
git clone https://github.com/chrisocling/card-pack-opening ~/.codex/skills/card-pack-opening

# Claude Code
git clone https://github.com/chrisocling/card-pack-opening ~/.claude/skills/card-pack-opening
```

然后对助手说“做一个拆卡包动画”或“用 $card-pack-opening 做抽卡动画”即可触发。

## 直接生成预览

只需要 Python 3：

```bash
python3 scripts/build_preview.py --output ./card-pack-preview.html
```

用自己的卡面和文字：

```bash
python3 scripts/build_preview.py --config ./pack.json --output ./card-pack-preview.html
```

配置字段和示例见 [references/configuration.md](references/configuration.md)；动画时序见 [references/motion-reference.md](references/motion-reference.md)。

## 目录结构

```
SKILL.md                    skill 说明（助手读取的入口）
agents/openai.yaml          Codex 界面显示信息
assets/pack-opening.html    动画模板
assets/default-config.json  默认五张卡配置
scripts/build_preview.py    注入配置、生成成品 HTML
references/                 配置与动效说明
```

> 默认按配置顺序展示卡片，`rarity` 只是展示标签，不代表真实概率或保底。

## License

[MIT](LICENSE)
