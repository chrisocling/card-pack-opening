---
name: card-pack-opening
description: 制作或修改可交互的卡包拆封动画，让一包卡片同时飞出再排成一排；支持替换卡面、卡名、卡包和速度，适用于“拆卡包”“抽卡动画”“仿参考视频开包”等请求。
---

# 卡包抽卡动画

使用随附 HTML 模板制作可在浏览器打开的开包体验。默认效果为暖灰舞台、彩色 foil 卡包、撕顶彩虹条带，以及五张卡片同时弹出后错峰落位。结果持续展示，直到用户重新开包。

## 生成预览

没有现有项目时先复用模板；有现有项目时，将相同的状态和动作移入项目原有结构。用户未提供卡面素材时使用内置角色示例，交付时说明卡面可以替换。

```bash
python3 <skill目录>/scripts/build_preview.py --output <交付目录>/card-pack-preview.html
```

替换内容时读取 [references/configuration.md](references/configuration.md)，准备 JSON 配置后运行：

```bash
python3 <skill目录>/scripts/build_preview.py --config <配置.json> --output <交付目录>/card-pack-preview.html
```

脚本直接复制模板并注入配置，将本地图片嵌入结果；无需 npm 或联网。`--fragment` 输出 HTML 片段，适合当前客户端支持的对话内预览。交付完整 HTML 时可直接在浏览器打开，不要将源代码当作预览贴给用户。

## 动效与交互

复现参考节奏或改动动画时读取 [references/motion-reference.md](references/motion-reference.md)，区分视频可见特征和模板的实现选择。使用 [assets/pack-opening.html](assets/pack-opening.html) 作为起点，根据新素材调整外观。

- 点击卡包、向右撕包或使用开包按钮均触发同一流程。开包期间锁定重复触发。
- 一包卡片同时飞出，再错峰排成一排；保留约两秒完成的整体节奏。展示结果后不自动收起，也不要求逐张点击揭晓。
- 卡片悬停时上抬并轻微 3D 倾斜；每张卡都是可聚焦的按钮，点击或键盘激活后高亮。
- 底部的“再开一包”复位卡包和结果，保留当前所选颜色，可以反复操作。
- 保留 `prefers-reduced-motion` 支持，减少运动后仍能完成开包并看到全部结果。
- 默认按配置顺序展示。仅在用户要求时实现随机抽取，并先明确规则；演示中的稀有度标签不表示真实概率或保底。

## 验证与交付

运行生成脚本，打开结果检查“开包 → 全部卡片落位 → 悬停／聚焦／点击卡片 → 再开一包”。检查连续触发不会重复生成卡片，窄屏可查看全部结果，替换图片实际显示。交付可打开的 HTML 和需要复用的配置，并简短说明调用方式与可替换项。
