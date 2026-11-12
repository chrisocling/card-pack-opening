# card-pack-opening · 卡包抽卡动画

一个 AI 编程助手 skill：生成可在浏览器直接打开的**拆卡包抽卡动画**。卡包从右边飘进来，眼睛跟着鼠标转；按住向右滑动，撕痕跟着手指走，卡包用力闭眼，撕开的口子喷出彩虹，卡片围成一圈转一圈后撒花落位。

- **手感**：悬停时卡包上浮发光、显示撕口；单击只会震动提示；只有向右滑动才能撕开，中途松手可以接着撕
- **有表情的角色**：卡包角色会看着鼠标、眨眼，撕包时使劲闭眼冒汗；卡片角色悬停会眨眼，点击会变爱心眼、星星眼、眨单眼等表情
- **卡通立体卡牌**：厚边框和卡片厚度、波点条纹底纹、贴纸描边角色、周期闪光与星点
- **随机抽卡**：按稀有度概率从卡池抽取，支持每包保底和连续 N 包必出，页面内公示概率
- **稀有度演出**：撕口光色提前暗示好卡；史诗、传说卡落位时有光晕、星光和闪光，传说卡压轴出场
- **音效**：撕纸、开包、落卡、传说和弦全部由浏览器实时合成，可一键静音
- **可配置**：卡面图片、卡名、稀有度、卡包颜色、所有提示文案、稀有度名称和播放速度；也可切回固定顺序展示
- 纯 HTML/CSS/JS 单文件成品，无需 npm、无需联网；支持键盘（右方向键撕包）、窄屏和 `prefers-reduced-motion`

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
assets/default-config.json  默认卡池与抽卡规则
scripts/build_preview.py    注入配置、生成成品 HTML
references/                 配置与动效说明
```

> 默认配置里的概率和保底只是演示。用于真实抽卡商品时，请确认概率并如实公示。

## License

[MIT](LICENSE)
