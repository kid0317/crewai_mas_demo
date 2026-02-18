# 官方skill的设计分析报告

## Algorithmic Art Skill 设计分析报告

### 1. Skill 名字

- **name**: `algorithmic-art`

`algorithmic-art` 这个命名非常直观，把「算法」与「艺术」直接组合在一起，既传达了领域（generative / algorithmic art），也暗示了技能是偏「方法论 + 工程化」的，而不是单纯输出一张图片。短而有辨识度，利于在一组 skills 中快速被检索和触发。

### 2. Skill 功能概述

- **核心能力**：围绕「算法艺术 / 生成艺术」提供一个从概念到实现的完整生产线，包括：
  - 抽象出「Algorithmic Philosophy」（算法美学 / 算法哲学）文本，作为生成艺术运动的宣言；
  - 基于这一哲学，用 p5.js 实现可交互的生成艺术作品（含种子随机性、参数探索 UI、seed 导航等）；
  - 产出三类成果：`哲学 .md` + `交互 HTML artifact`（内联 p5.js 代码）+（隐含的）可反复探索的生成空间。
- **典型触发场景**：当用户提到「用代码创作艺术 / generative art / algorithmic art / flow field / particle system」等需求时，这个 skill 负责把松散的艺术诉求，转译成高度结构化的算法哲学 + 工程实现方案，并输出可直接在浏览器或 Claude artifact 中运行的交互作品。

从功能边界上看，这个 skill 明确不是「随便画一张图」，而是「建立一个生成艺术世界观，并工程化实现为可交互的作品」，强调：
- 过程优先于结果（process over product）；
- 可复现与参数可调（seed / params / UI）；
- 生成的是「活的算法系统」，而不是一次性静态图像。

### 3. Skill 元数据中的 description

`description` 字段原文如下（英文）：

> Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.

### 4. 对 description 的信息结构与 prompt 技巧分析

#### 4.1 信息结构拆解

可以拆成三个层次的信息单元：

1. **核心能力声明（What it does）**
   - “Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration.”
   - 明确指出：
     - 使用技术栈：p5.js；
     - 关键特性：seeded randomness（可复现随机）、interactive parameter exploration（交互参数探索）；
     - 产出类型：algorithmic art（生成艺术）。
   - 对模型来说，这一段直接定义了「调用该 skill 时默认的技术与产出形态」，降低了后续歧义。

2. **触发条件与使用时机（When to use）**
   - “Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems.”
   - 给出一组典型触发语义：
     - creating art using code
     - generative art / algorithmic art
     - flow fields / particle systems
   - 这在路由层面非常重要：模型在解析用户请求时，只要检测到这些语义，就可以高置信度地选择该 skill。

3. **合规与风格约束（Constraints & Safety）**
   - “Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.”
   - 明确一条行为边界：只创作原创生成艺术，不模仿或复制现有艺术家的作品。
   - 这既是安全约束，也是风格倾向（鼓励原创 algorithm 设计）。

整体信息结构遵循了一个非常经典的 skill 描述模式：
- **能力 → 触发条件 → 约束 / 安全**。

#### 4.2 从 prompt 设计角度的技巧与亮点

- **明确技术栈与关键特性，缩小搜索空间**
  - 把「p5.js / seeded randomness / interactive parameter exploration」直接写在 description 中，相当于把「如何做」预先绑定到这个 skill。
  - 当模型决定调用该 skill 时，不需要再在「用哪种图形库 / 要不要考虑随机种子 / 要不要做交互 UI」上摇摆，减少了推理分支。

- **用典型查询语义定义触发边界**
  - 通过列举「art using code / generative art / flow fields / particle systems」等短语，让模型在自然语言匹配时更容易路由：
    - 既覆盖了通用需求（generative art），也覆盖了专业术语（flow fields, particle systems）。
  - 这种「用一组代表性短语来刻画边界」是非常有效的 skill 路由技巧，可复制到其他 skills。

- **把合规要求内嵌为默认偏好而非单独警告**
  - description 不是简单说「不要侵权」，而是「Create original algorithmic art rather than copying…」：
    - 语言上是「鼓励原创」+「顺带说明原因是版权」；
    - 这类正向 framing 更容易被模型当作创作目标，而不是被动限制。

- **紧凑而信息密度高**
  - 三句话覆盖：技术栈 + 能力 + 使用场景 + 安全约束；
  - 没有多余叙述，便于路由模块解析与记忆。

#### 4.3 如何帮助模型更好理解与触发

- **语义锚点丰富**：多个关键词（p5.js, generative art, flow fields, particle systems）在不同用户表述下都能被覆盖，提高触发 recall。
- **目标足够具体**：不是笼统的「visual art」，而是限定「algorithmic art using p5.js」，有利于模型在工具选择时更有信心。
- **内嵌安全与风格**：让模型在调用 skill 的同时，自动带着「原创 generative algorithm」的意图进行设计，减少需要额外补充的安全 prompt。

总体来看，这个 description 体现的是一种「高密度、路由导向、带安全倾向」的元描述写法，属于可复用的优秀范式。

### 5. skill.md 内容结构与整体 prompt 亮点分析

#### 5.1 文档宏观结构概览

`SKILL.md` 整体可以分为若干逻辑段落：

1. **总体介绍与两步流程**
   - 定义「Algorithmic philosophies」的概念；
   - 给出两步流程：Algorithmic Philosophy Creation → p5.js generative art（.md → .html + .js）。

2. **Algorithmic Philosophy Creation**
   - 说明「哲学」是什么、应该包含什么；
   - 给出生成步骤（命名 movement、撰写 4-6 段落哲学）；
   - 提供示例哲学（Organic Turbulence / Quantum Harmonics 等）；
   - 总结 Essential Principles。

3. **Deducing the Conceptual Seed**
   - 把「原始用户请求」提炼为「微妙的概念种子」，作为作品的隐性 DNA。

4. **p5.js Implementation**
   - 强制 Step 0：读取 `templates/viewer.html`，并严格区分「固定」与「可变」部分；
   - Technical Requirements：seeded randomness、参数结构、核心算法与哲学的映射、canvas 结构；
   - Craftsmanship Requirements：平衡 / 色彩 / 构图 / 性能 / 可复现；
   - Output Format：哲学 + HTML artifact。

5. **Interactive Artifact Creation**
   - 细化「固定 vs 可变」；
   - 要求参数控制、seed 导航、单一 HTML artifact 结构；
   - 规定 sidebar / 控件 / 下载按钮等细节。

6. **Variations & Exploration**
   - 说明如何通过 seed 与 gallery mode 探索多样性。

7. **The Creative Process**
   - 抽象出统一 pipeline：User request → Philosophy → Implementation → Params → UI。

8. **Resources**
   - 明确提供的模板文件与用途：`viewer.html` 与 `generator_template.js`；
   - 强调「模板是起点而非菜单」。

整体是一个「从理念 → 概念 → 技术 → UI → 工程落地 → 再抽象为流程与资源」的完整闭环。

#### 5.2 从 prompt 视角看结构设计的亮点

- **先抽象，再实现：强制两阶段思考**
  - 通过「Algorithmic Philosophy Creation」→「P5.JS Implementation」的硬拆分，避免模型直接跳到代码层：
    - 第一阶段专注于世界观、算法哲学、计算美学；
    - 第二阶段再让代码成为这一哲学的表达。
  - 这是一个非常典型、且有效的「分阶段 prompt」设计，有助于提高作品的一致性与深度。

- **用命名与示例构建「风格空间」**
  - movement 命名示例（Organic Turbulence / Quantum Harmonics / Recursive Whispers / Field Dynamics / Stochastic Crystallization）：
    - 风格统一（物理 / 数学隐喻）；
    - 对模型来说，这些例子在 embedding 空间中形成一个 cluster，引导后续生成的新 movement 也带有类似气质。
  - 示例哲学段落同时展示「如何用语言描述算法 + 视觉 + emergent behavior」，是非常好的 few-shot 模板。

- **大量使用「强调 + 重复」来固化关键偏好**
  - 多处重复强调：
    - Algorithmic expression / Emergent behavior / Computational beauty / Seeded variation；
    - Expert craftsmanship / meticulously crafted / deep expertise 等；
  - 这种「高频重复 + 同义表达」是典型的 LLM 提示技巧，可以显著提高模型对这些概念的权重，减少跑偏。

- **明确「不要什么」：反模式列举**
  - 例如：
    - 不要 static images；
    - 不要创建 HTML from scratch，不要改 Anthropic branding；
    - 不要把 `generator_template.js` 当 pattern menu；
  - 清晰的「反模式」辅以「正向目标」，有助于收缩输出空间。

- **精细化工程约束转化为自然语言 checklist**
  - 像 seed 导航、参数 sliders、reset / regenerate、download PNG 等需求，本质上是产品/前端需求；
  - 文中用分点 + 小标题的方式，转译成自然语言 checklist，模型按部就班地实现即可。

- **将「创作过程」抽象为通用 pipeline**
  - 「User request → Algorithmic philosophy → Implementation → Parameters → UI」这段总结：
    - 不仅是对本 skill 的说明，也是一个可迁移的 prompt 设计范式；
    - 让模型在未来的调用中更容易按这个顺序思考与输出。

#### 5.3 可抽象出的 prompt 编写技巧

1. **两阶段甚至多阶段思维引导**
   - 阶段 1：形成抽象哲学（文本层）；
   - 阶段 2：把哲学翻译为算法与 UI（代码层）；
   - 阶段 3：定义 parameters 与交互逻辑。
   - 这种把复杂任务分阶段明示的做法，可以显著提升输出质量。

2. **示例驱动 + 明确长度要求**
   - 通过多个精简示例 + 要求「4-6 段 substantial paragraphs」，控制输出的内容密度与篇幅；
   - 避免模型输出过短 / 过长的哲学描述。

3. **「固定 vs 可变」结构显式化**
   - 明确定义哪些部分是固定（UI 框架 / 品牌样式 / seed 控件），哪些是可变（算法 / 参数 / 颜色 / 控件数量）；
   - 这种分法非常适合所有「在模板上定制」的应用场景。

4. **将工程实践转为可复用 prompt 模板**
   - 把 seeded randomness、参数设计维度（数量 / 比例 / 概率 / 阈值等）写成通用原则；
   - 这让模型跨不同艺术作品都能复用同一套「如何 design params」的思路。

5. **反复强调「工匠精神 / 专家级实现」**
   - 多次用语言暗示「master-level implementation / painstaking optimization」；
   - 这是一种对模型行为的软约束：鼓励更复杂、更有条理的算法设计，而不是草率随机噪声。

### 6. 设计模式层面的整体分析：范式与（反）最佳实践

#### 6.1 可抽象的设计范式 / 模式

- **范式一：理念先行（Philosophy-First Pattern）**
  - 先构建「算法哲学 / 审美运动宣言」，再写代码：
    - 优点：保证作品在形式多样的同时，有统一的内在逻辑与美学方向；
    - 对其他领域的启发：例如数据可视化、建筑生成、音乐生成等，也可以先写「美学与结构哲学」，再做实现。

- **范式二：固定 UI / 模板 + 可变算法 / 参数**
  - 保持一致的 UI 与交互逻辑（品牌、布局、控件结构），用算法与参数表达多样性：
    - 便于产出大量风格一致的 artifact；
    - 复用工程资产（模板 / 代码框架）。
  - 这是通用的「Template + Plugin」模式，skill 把「插件部分」交给模型自由发挥。

- **范式三：Seeded System Pattern（有种子系统的生成宇宙）**
  - 把随机性全部收敛为「有 seed 的系统」，并强制：
    - `randomSeed` / `noiseSeed` 同步；
    - seed 导航 UI；
    - 可复现输出。
  - 在任何涉及随机性的应用中，这都是非常值得借鉴的设计模式。

- **范式四：Conceptual Seed Pattern（概念种子嵌入算法）**
  - 通过「Deducing the Conceptual Seed」部分，把用户的隐性概念变成算法参数与行为的细节嵌入：
    - 既满足了用户需求的「隐喻表达」，又不牺牲 generative art 的抽象性；
    - 对其它创意领域同样适用（例如：小说主题隐喻、音乐动机等）。

- **范式五：过程导向的创作流水线**
  - 明确 pipeline：Interpret intent → Philosophy → Implementation → Params → UI；
  - 这个 pipeline 可以直接套用在任何「从自然语言需求到交互系统」的构建任务上。

#### 6.2 值得参考的最佳实践

- **高信息密度的 description 定义技能边界**
  - 把技术栈 + 能力 + 触发条件 + 安全约束浓缩在 2–3 句中，是非常好的技能元数据写法。

- **广义 few-shot：用完整 section 作为行为模版**
  - `PHILOSOPHY EXAMPLES` 不只是例子，也是行为示范；
  - 通过完整的段落风格，教会模型「什么叫合格的哲学描述」。

- **对「固定 vs 可变」进行结构化标记**
  - 在模板型任务中，明确标注「不可改动」与「可定制」区域，这个模式可用于：
    - 邮件框架；
    - API 响应结构；
    - UI 模板等。

- **多层级的强调与安全防护**
  - description 层说「原创生成艺术」；
  - 正文层说「不要复制已有艺术家风格」；
  - 模板层强调「算法需要原创设计」。
  - 多层提醒可大幅降低越界风险。

- **用「工匠精神」标签驱动复杂度与质量**
  - 强调作品应看起来「经过无数迭代、专家精心打磨」，有效鼓励模型：
    - 使用更丰富的参数；
    - 更讲究的结构设计与可读性；
    - 更好的性能与可复现性。

#### 6.3 潜在的反模式或需要留意的点

- **复杂度较高，可能增加执行成本**
  - 对于简单用户请求（比如「给我一个简单的 generative background」），整个两阶段哲学 + 完整交互 UI 流程可能过重；
  - 在技能设计层面，未来可以考虑：
    - 增加一个「轻量模式」分支；
    - 或通过元数据标注「适用于深度 generative art 需求」。

- **对模板文件的强依赖**
  - Skill 强制要求先读 `viewer.html`，这是良好的工程实践；
  - 但从系统集成角度，如果模板路径改变或不可用，skill 会整体失效；
  - 在更通用的设计中，可以考虑在 `SKILL.md` 内附一个「降级版 minimal template」，以提高鲁棒性。

---

### 7. 脚本 / 模板工具文案与设计模式（如有）

`algorithmic-art` 的脚本与模板主要体现在：
- `templates/viewer.html`：作为 HTML + UI 的**硬模板**；
- `templates/generator_template.js`：作为 p5.js 代码结构与参数组织方式的**示范脚本**。

从文案与设计模式上看，有几个特点：

- **「模板是起点，不是菜单」的强提示文案**
  - 文中反复强调：`viewer.html` 要「原样复制」作为基础，`generator_template.js` 只是结构参考，不是「可选样式菜单」。
  - 这属于一种重要的反模式防御：避免模型把示例脚本当作固定 pattern 库，导致所有作品高度同质化。

- **固定 vs 可变区域通过自然语言严格标注**
  - 对于 `viewer.html`，SKILL.md 用「FIXED / VARIABLE」分组列出哪些 DOM 结构、品牌样式和控制区域必须保留，哪些是可以替换的算法与参数 UI。
  - 这相当于为「工具 / 模板」定义了参数：不是通过函数签名，而是通过「可变片段」的文字协议，指导模型如何安全修改。

- **脚本调用层采用「约束 +示例」而非 API 文档式参数表**
  - 对 seeded randomness、参数对象、canvas setup 等部分，文档用简短代码块 + 上下文说明方式给出，而不是正式函数文档：
    - 例如 `let params = { seed: 12345, ... }` 后跟一串「如何设计参数维度」的自然语言说明。
  - 这种写法的设计模式是：**先给最小可行代码骨架，再用文字描述可扩展维度**，尤其适用于面向 LLM 的「半结构化 API」。

- **最佳实践**
  - 模板文件的说明文案聚焦在「哪些可以动 / 哪些不能动」和「为什么要这样约束」上，而不是详述每个 DOM 细节；
  - 对 p5.js 模板，通过少量核心模式（seed、params、setup/draw）+ 原则性语言，既建立了统一风格，又给足创作自由。

- **潜在反模式**
  - 由于 `generator_template.js` 的具体函数和类没有在 SKILL.md 内做显式逐项文档，如果模型倾向于「只看 SKILL.md 不读脚本」，可能会遗漏一些结构细节；
  - 在更复杂的脚本场景中，可以考虑为关键函数在 SKILL.md 增补极简「用途 + 关键参数」的一行说明，既不占太多 tokens，又提升工具可发现性。

---

## XLSX Skill 设计分析报告

### 1. Skill 名字

- **name**: `xlsx`

这个名字直接用主扩展名来命名，涵盖 .xlsx/.xlsm/.csv/.tsv 等一整类「表格 / 表型数据」任务，易于记忆和路由，但也通过 description 进一步收紧到「以电子表格为主要交付物」这一清晰边界。

### 2. Skill 功能概述

- **核心能力**：围绕各种电子表格文件（Excel 及兼容格式）的创建、读取、编辑、分析和清洗，包括：
  - 创建或修改工作簿、工作表、单元格内容、格式、公式；
  - 使用 `pandas` 做数据分析与导入导出；
  - 使用 `openpyxl` 做精细格式和公式编辑；
  - 利用 `scripts/recalc.py` + LibreOffice 做公式重算与错误检查；
  - 针对财务模型提供行业标准的颜色编码、数值格式和公式构造规范；
  - 提供全面的 QA checklist 和最佳实践，确保「零公式错误」。
- **边界**：当主要交付物不是电子表格（例如 Word 报告、HTML 报表、数据库流水线、Google Sheets API 集成）时，明确不应触发。

### 3. Skill 元数据中的 description

`description` 原文（英文）：

> Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

### 4. 对 description 的信息结构与 prompt 技巧分析

#### 4.1 信息结构

可以拆为四层：

1. **触发总原则**：当「spreadsheet file is the primary input or output」。
2. **典型任务枚举**：打开 / 编辑 / 修复现有表格、从零创建、格式转换、清洗脏数据。
3. **触发信号增强**：当用户随口提到某个 xlsx 路径或文件名时也要触发。
4. **硬边界排除**：当主要交付是 Word / HTML / 脚本 / 数据库 / Google Sheets API 时禁止触发。

#### 4.2 Prompt 技巧与亮点

- **以「primary input/output」定义职责范围**：不是凡是出现表格就触发，而是当表格是任务核心，这种定义非常清晰，减少与 `pdf`、`docx` 等技能的冲突。
- **大量例举自然语言触发短语**：列出多种文件类型与场景，同时强调「even casually」的提法，帮助路由模型在模糊表达下也能匹配。
- **正向触发 + 反向排除组合**：最后一长句用「Do NOT trigger when...」明确技能不负责的场景，形成封闭空间。
- **把「deliverable must be a spreadsheet file」作为核心约束重复强调**：在描述结尾再次固化这个条件，有利于在边界场景（如「把表格内容写成报告」）时选用别的技能。

#### 4.3 对模型理解与触发的帮助

- 通过丰富的例子与排除条件，让 skill 路由既有高 recall，又避免误触；
- 「primary input or output」这样的简短抽象短语，使同一规则可以泛化到未枚举的场景；
- 将「清洗脏表」单独点名，避免模型只在「格式漂亮」场景下才想到用这个 skill。

### 5. SKILL.md 其余内容的结构与 prompt 亮点

#### 5.1 结构概览

1. 输出要求（字体、零公式错误、模板继承）；
2. 财务模型专用规范（颜色编码、数字格式、公式构造规则、硬编码标记方式）；
3. 概览 & 重要要求（LibreOffice + recalc 流程）；
4. 读写数据：`pandas` 代码示例；
5. 使用公式而非硬编码的反例 & 正例；
6. 常见工作流步骤（选择工具 → 加载 → 修改 → 重算 → 校验）；
7. 新建文件与编辑现有文件的 `openpyxl` 示例；
8. 公式重算脚本使用方法 + 错误 JSON 解析；
9. 公式验证 checklist + 常见陷阱；
10. 最佳实践：库选择、性能与类型处理；
11. 代码风格指南。

#### 5.2 Prompt 设计亮点与可抽象技巧

- **「输出质量标准」前置**：一上来就声明字体与「ZERO formula errors」，为后文所有操作设定质量 baseline，是典型的「先立标准，再谈方法」模式。
- **使用「❌ WRONG / ✅ CORRECT」对比示例**：通过成对代码片段展示错误模式与正确模式，非常有助于 LLM 内化习惯（特别是禁止在 Python 中预计算再硬编码到单元格）。
- **财务领域的行业标准编码内化为规则列表**：把蓝/黑/绿/红/黄等颜色约定写清楚，使模型生成的模型更符合现实从业者习惯。
- **脚本工作流抽象为固定步骤**：Choose tool → Create/Load → Modify → Save → Recalc → Verify，这种纲要式流程可直接迁移到其它文件类 skill。
- **大量 checklist 化**：Verification Checklist / Common Pitfalls / Testing Strategy 等，以打勾清单的形式明示 QA 行为，有利于模型在结尾自动做「自查」。

### 6. 设计模式与（反）最佳实践

- **范式：质量门槛优先（Quality-Gate-First Pattern）**：先定义「零公式错误 / 保留模板风格」等底线，再给操作步骤，适用于任何「工程产物」类技能。
- **范式：反例驱动行为纠偏**：通过 WRONG vs CORRECT 的并列代码段，明确禁止模式（硬编码计算结果），帮助模型避免常见捷径。
- **范式：领域规范内嵌**：把财务行业的颜色/格式约定深度写进 skill，使输出自然贴合专家习惯，而不是通用 Excel 模板。
- **潜在反模式**：文档篇幅较长、细节极多，若一次性全载入上下文，可能占用大量 tokens；但其本身采用了大量小节与标题，有助于模型只聚焦需要的部分。对于未来 skill，可考虑再将财务专用内容拆到 references，以进一步「渐进披露」。

### 7. 脚本 / 工具调用文案与设计模式（如有）

`xlsx` skill 本身依赖多种脚本与库（如 `scripts/recalc.py`、`scripts/office/soffice.py`、`scripts/office/unpack.py` 等），但 SKILL.md 中并没有为每个脚本写传统意义上的「函数级 API 文档」，而是采用了更适合 LLM 的几种设计模式：

- **命令级用法优先，而不是函数签名**
  - 文档更侧重给出「任务导向」的命令示例，例如：
    - `python scripts/recalc.py output.xlsx 30`
    - `python scripts/office/soffice.py --headless --convert-to docx document.doc`
  - 每条命令的参数含义通过上下文自然语言解释（如 timeout、excel_file），而不是形式化参数表，这种写法对「读一眼就照抄」的 LLM 行为很友好。

- **通过「错误 JSON 结构」定义脚本输出契约**
  - 对 `recalc.py`，SKILL.md 不是解释函数内部实现，而是给了典型输出 JSON：
    - `status / total_errors / error_summary` 等字段的语义；
  - 这相当于为脚本定义了「输出 schema」，使模型可以基于该结构写后续处理代码，这是 LLM 友好的「契约式设计」模式。

- **参数语义靠任务上下文而非堆栈式说明**
  - 例如 `validate_gif(is_emoji=True, verbose=True)` 或 `python scripts/recalc.py <excel_file> [timeout_seconds]`，均通过几句简单文案说明「什么时候需要该参数」而不是列出所有可能值；
  - 这种设计减少了冗长 API 说明，同时保留了与实际任务最相关的用法分支，对上下文有限的 LLM 十分友好。

- **最佳实践**
  - 面向 LLM 的脚本文档不必像人类 API 文档那样详尽枚举所有参数和边缘 case，而应：
    - 用 1–2 个「推荐调用方式」覆盖 80% 场景；
    - 清楚说明关键参数如何影响行为（比如 timeout、目标文件路径、是否 emoji 模式等）；
    - 对输出结构给出一个完整示例，使模型可以据此解析与分支。

- **潜在反模式**
  - 若未来在 SKILL.md 中开始为脚本堆叠大量底层参数细节，可能会稀释当前这种「任务导向 + 示例驱动」风格，让模型更难抓到真正重要的调用方式；
  - 因此在增加参数说明时，应优先考虑：「这个信息是否真的会影响大多数调用路径？」如果不是，就应该保留在更底层的 REFERENCE 中，而不是塞进 SKILL.md。

---

## Webapp Testing Skill 设计分析报告

### 1. Skill 名字

- **name**: `webapp-testing`

命名直接对应「Web 应用测试」，配合 description 中的 Playwright 与 with_server 脚本，定位在「测试本地 Web 应用」的自动化脚本编写场景。

### 2. Skill 功能概述

- **核心能力**：
  - 使用 Python + Playwright 对本地或开发环境 Web 应用进行端到端交互测试；
  - 借助 `scripts/with_server.py` 管理一个或多个服务的生命周期，包装测试脚本；
  - 指导采用「侦察后行动（reconnaissance-then-action）」模式：先截图/抓 DOM，再推导选择器与操作；
  - 提供最佳实践与常见陷阱（例如必须等待 `networkidle` 再看 DOM）。

### 3. Skill 元数据中的 description

> Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

信息密度适中，清楚点出：工具栈（Playwright）、主要用途（交互 + 测试本地 Web 应用）、典型任务（功能验证、UI 调试、截图、日志查看）。

### 4. 对 description 的信息结构与 prompt 技巧分析

- **一句话概括技术栈 + 任务类别**：明确「本地 + Web 应用 + Playwright」，便于与 `frontend-design` 等区分（设计 vs 测试）。
- **列举能力而非触发短语**：description 偏「能力描述」，路由上依赖「测试/验证/调试」等语义匹配。
- **简洁无排除**：该 skill 在 Web 测试语义明显时触发即可。

### 5. SKILL.md 内容结构与 prompt 亮点

- **决策树文本化**：用 ASCII tree 明确「静态 HTML vs 动态应用 / 服务器是否已运行」下的推荐路径，是多分支工作流的典型 prompt 设计。
- **黑盒脚本优先**：「Always run scripts with `--help` first」「DO NOT read the source until...」约束模型避免加载大型脚本污染上下文，属于上下文预算管理。
- **Reconnaissance-Then-Action 模式**：先 inspect（screenshot/content/locator），再 identify selectors，再 execute，可迁移到任何 UI 自动化场景。
- **反例 + 正例**：Common Pitfall 用 ❌/✅ 对比「先 networkidle 再 inspect」，高信号密度。

### 6. 设计模式与（反）最佳实践

- **范式：黑盒脚本优先（Black-Box-Script Pattern）**：通过 `--help` + 直接调用使用脚本，不读源码。
- **范式：文本决策树**：为多条件分支提供清晰路径选择。
- **范式：Recon → Act**：UI 探索与行为执行分步，通用自动化模式。
- **反模式风险**：description 未写「when not to use」，与其它前端类 skill 的边界依赖语义区分。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **单脚本 + 命令级用法**：仅突出 `scripts/with_server.py`，用法以完整命令行示例为主：
  - 单服务：`--server "npm run dev" --port 5173 -- python your_automation.py`
  - 多服务：多个 `--server ... --port ...` 后跟 `-- python ...`
  - 参数语义通过「Single server / Multiple servers」等小标题与示例自然解释，无单独参数表。
- **「先 --help，勿读源码」的强约束**：明确写「DO NOT read the source until...necessary」「black-box scripts」，属于**反模式防御**：避免模型把大脚本读入上下文。
- **设计模式**：**入口单一 + 示例覆盖主路径**；参数（如 port、server 命令）通过示例中的占位符传达，而非枚举。
- **最佳实践**：对复杂 CLI 脚本，在 SKILL.md 中只保留 1～2 种典型调用 + 一句「run with --help」，既省 token 又引导正确使用。
- **反模式**：若在正文中开始逐参数字段说明，会削弱「黑盒」定位，增加 token 且易导致模型去读源码。

---

## Web Artifacts Builder Skill 设计分析报告

### 1. Skill 名字

- **name**: `web-artifacts-builder`

名称表意「构建 Web artifacts」，目标是为 Claude 会话生成单文件 HTML artifact（React + 打包），而非长期运行站点。

### 2. Skill 功能概述

- **核心能力**：使用 React 18 + TS + Vite + Tailwind + shadcn/ui 构建复杂、带状态与路由的前端 artifact；提供 `init-artifact.sh` 与 `bundle-artifact.sh` 完成初始化与打包；指导开发、打包、展示及可选测试；并给出设计反建议（避免 AI slop）。
- **适用场景**：需要复杂交互、状态管理、路由或 shadcn 组件的 artifact，而非简单单文件 HTML/JSX。

### 3. Skill 元数据中的 description

> Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.

结构：能力（elaborate multi-component artifacts）+ 技术栈枚举 + 触发条件（state management, routing, shadcn）+ **明确排除**（not for simple single-file），用复杂度阈值做路由。

### 4. 对 description 的信息结构与 prompt 技巧分析

- **技术栈 + 复杂度阈值** 共同定义边界；「not for simple artifacts」强排除，避免与 frontend-design 或简单 HTML 冲突。
- **「Suite of tools」** 暗示多脚本/步骤，与正文两步脚本呼应。

### 5. SKILL.md 内容结构与 prompt 亮点

- **5 步流程**：Initialize → Develop → Bundle → Display → (Optional) Test，极简 pipeline。
- **Design & Style Guidelines** 单句反 AI slop，具体设计交给 frontend-design 等 skill。
- **Step 内「What the script does」**：用 bullet 说明 bundle 脚本的依赖安装、Parcel 配置、html-inline 等，帮助模型理解而不必读脚本。
- **明确「不要先测试」**：减少延迟、先呈现再测，属于体验导向的 prompt。

### 6. 设计模式与（反）最佳实践

- **范式：任务流水线型**：numbered steps 指定完整 pipeline。
- **范式：复杂度阈值路由**：用「complex / state management / routing」做门槛。
- **风险**：设计指导较轻，需与 frontend-design 等组合使用。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **两个脚本、各一段说明**：
  - `scripts/init-artifact.sh <project-name>`：仅说明「创建新 React 项目」及产出清单（React/TS/Vite/Tailwind/shadcn/路径别名等），**无参数表**，参数即占位符 `<project-name>`。
  - `scripts/bundle-artifact.sh`：无参数；用「What the script does」列表说明行为（安装依赖、.parcelrc、构建、html-inline），**以行为描述替代参数说明**。
- **设计模式**：**脚本即步骤**；每个脚本对应 pipeline 中一步，文案侧重「输入/输出与作用」而非 CLI 选项。
- **最佳实践**：对无复杂参数的 shell 脚本，用「命令 + 产出说明 + 可选约束」（如「必须有 index.html」）即可，避免冗长选项列表。
- **反模式**：若为 init 脚本增加大量可选参数并在 SKILL.md 枚举，会偏离当前「简单两步」的心智模型。

---

## Theme Factory Skill 设计分析报告

### 1. Skill 名字

- **name**: `theme-factory`

「工厂」隐喻强调可复用主题的批量应用，作为跨 artifact 的视觉主题层。

### 2. Skill 功能概述

- 提供 10 套预设主题（颜色 + 字体），适用于 slides/docs/reports/landing pages；
- 通过 `theme-showcase.pdf` 展示，用户选择后再应用到已有 artifact；
- 支持在预设不满足时根据描述生成自定义主题并应用。

### 3. Skill 元数据中的 description

> Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.

结构：能力（styling with a theme）+ 适用类型 + 10 preset + on-the-fly 新主题；无硬排除，通过「styling artifacts」隐含边界。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 用抽象概念「theme」统一跨格式样式任务；「10 pre-set」与「generate on-the-fly」并置，覆盖预设与自定义两种路径。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Usage Instructions 4 步**：展示 theme-showcase → 询问选择 → 等待确认 → 应用；把**人机协作顺序**写进流程，避免模型擅自选主题。
- **Themes Available**：10 个主题名 + 一句话描述，既是枚举也是 few-shot 命名风格。
- **Application Process**：从 `themes/` 读文件、应用颜色与字体、保持对比度与一致性，抽象层高、不写具体实现细节。
- **Create your Own Theme**：简短说明「无匹配时生成类似风格的新主题、命名方式、先展示再应用」。

### 6. 设计模式与（反）最佳实践

- **范式：视觉风格层 Skill**：与 pptx/docx/canvas 等解耦，只负责主题。
- **范式：人机协同决策**：强制「展示 → 用户选 → 再应用」。
- **范式：预设 + 自定义**：多数用预设，长尾用生成。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无命令行脚本**：skill 依赖的是 `theme-showcase.pdf` 与 `themes/` 目录下的主题文件，无可执行脚本。
- **「工具」即资源**：对 `themes/` 下文件的「调用」通过自然语言描述（Read the corresponding theme file → Apply colors and fonts），未给出函数或 API；相当于**资源型协议**：按主题名选文件、按文件规范应用。
- **设计模式**：**资源清单 + 应用流程**；无需参数表，只需清单（主题名列表）与步骤（如何读、如何用）。
- **最佳实践**：对纯资源型 skill，在 SKILL.md 中列清资源列表与使用顺序即可，无需脚本/函数级文档。
- **反模式**：若为「应用主题」虚构或引入复杂脚本接口，会破坏当前「读文件 + 应用」的简单心智。

---

## Slack GIF Creator Skill 设计分析报告

### 1. Skill 名字

- **name**: `slack-gif-creator`

命名点出平台（Slack）与产物（GIF），窄而深的用例：为 Slack 创建符合规格、体积可控的动图。

### 2. Skill 功能概述

- 提供 Slack 动图约束（尺寸、FPS、颜色数、时长）；
- 封装 GIFBuilder、validators、easing、frame_composer 等工具；
- 指导用 PIL 绘制高质量动画（线宽、层次、色彩、组合形状）；
- 提供动画概念（shake/pulse/bounce/zoom/particle burst 等）与优化策略。

### 3. Skill 元数据中的 description

> Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."

技巧：能力 + 约束 + 触发句式合一；「for Slack」强化平台；示例触发句「make me a GIF of X doing Y for Slack」作为 few-shot 触发。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 用「Knowledge and utilities」「constraints, validation tools, animation concepts」概括提供物；用典型用户句锚定触发，便于路由。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Slack Requirements 前置**：尺寸/FPS/颜色/时长先给出，避免生成不合规。
- **Core Workflow**：GIFBuilder 创建 → add_frame/add_frames → save（含 num_colors、optimize_for_emoji 等），三步代码示例。
- **Drawing Graphics**：用户图 vs 自绘、PIL 基本图形、Making Graphics Look Good（线宽、层次、色彩、复杂形状）等设计向指导。
- **Available Utilities**：分小节给出 GIFBuilder、Validators、Easing、Frame Helpers，每节「一句话用途 + 代码示例 + 关键参数内联注释」。
- **Animation Concepts**：按概念（Shake/Pulse/Bounce/Spin/Fade/Slide/Zoom/Explode）给出思路与公式/easing 用法，便于组合创新。
- **Philosophy**：明确提供什么（Knowledge / Utilities / Flexibility）、不提供什么（模板/emoji 字体/预制图库），边界清晰。

### 6. 设计模式与（反）最佳实践

- **范式：平台优化 Skill**：针对 Slack 深度优化。
- **范式：工具 + 知识**：既有 API（GIFBuilder 等）又有动画与设计理念。
- **范式：创意提示**：用文案驱动视觉质量（线宽、颜色、叠加），而非只给代码。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **以「模块 + 函数」为单位的说明**：每个 utility 一小节（GIFBuilder / validators / easing / frame_composer），结构统一：
  - **用途一句**：如「Assembles frames and optimizes for Slack」「Check if GIF meets Slack requirements」。
  - **代码示例**：典型调用 3～5 行，参数直接写在调用里。
  - **参数语义**：通过示例内注释或紧跟的「Available: linear, ease_in, ease_out...」等短列表传达，**无独立参数表**。
- **GIFBuilder**：`width, height, fps` 在构造函数；`add_frame(frame)` / `add_frames(frames)`；`save(path, num_colors=..., optimize_for_emoji=..., remove_duplicates=...)`，关键参数在示例中体现，另在 Optimization Strategies 中集中说明。
- **Validators**：`validate_gif(path, is_emoji=..., verbose=...)` 与 `is_slack_ready(path)` 仅通过示例与「Detailed validation / Quick check」区分用途。
- **Easing**：`interpolate(start, end, t, easing=...)`，easing 可选值用一行枚举，无类型或默认值表。
- **Frame Helpers**：以导入列表 + 函数名呈现（create_blank_frame, create_gradient_background, draw_circle...），无每个函数的参数说明，依赖「Convenience functions for common needs」+ 命名自解释。
- **设计模式**：**按模块分组 + 示例承载参数语义 + 可选值短列表**；避免大段 API 文档，保持「看到就会用」的密度。
- **最佳实践**：对 Python 工具模块，在 SKILL.md 用「模块名 + 一句用途 + 1 个示例 + 关键参数或枚举值」即可；复杂参数可放在「Optimization Strategies」等按场景说明。
- **反模式**：若为每个 helper 函数写完整签名与所有参数，会拉长正文、分散对「动画概念」与设计建议的注意力；保持工具说明紧凑、概念与创意说明突出更符合本 skill 定位。

---

## Skill Creator Skill 设计分析报告

### 1. Skill 名字

- **name**: `skill-creator`

用于「创建 skill」的元技能，提供 skill 设计与实现指南。

### 2. Skill 功能概述

- 定义 Skill 及其提供物（工作流、工具集成、领域知识、资源）；
- 核心原则：简洁、自由度设置、渐进披露；
- Skill 解剖：SKILL.md + scripts/references/assets；
- 设计模式：高/中/低自由度、引用拆分、渐进披露三层加载；
- 六步创建流程：理解需求 → 规划资源 → 初始化 → 编辑 → 打包 → 迭代。

### 3. Skill 元数据中的 description

> Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

触发条件明确（create/update skill）；强调 effective 与扩展能力（知识、工作流、工具集成）。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 「when users want to create a new skill」精确对应使用场景；含「update existing」覆盖维护；「effective」暗示质量与最佳实践。

### 5. SKILL.md 内容结构与 prompt 亮点

- **About Skills / Core Principles**：简洁、自由度、解剖与 Progressive Disclosure，从「context window 预算」角度强调精简。
- **自由度分级**：高/中/低对应不同任务脆弱度，用「narrow bridge vs open field」比喻，便于模型选择粒度。
- **Progressive Disclosure 模式**：Metadata 常驻 → Body 触发后加载 → Resources 按需；并给出「高层 guide + references」「按领域/按变体拆分」等具体模式。
- **Skill Creation Process 六步**：每步有跳过条件、示例（PDF/frontend/BigQuery）、以及 init_skill.py / package_skill.py 等脚本说明。
- **Frontmatter/Body 写作指南**：description 必须含「what + when」，且 when 放在 description 而非 body；Body 用祈使/不定式。

### 6. 设计模式与（反）最佳实践

- **范式：元技能（Meta-Skill）**：指导如何定义其他技能。
- **范式：渐进披露与引用拆分**：按需加载 references，保持 SKILL.md 精简。
- **范式：流程化创建**：六步保证可维护与可扩展。
- **反模式**：在 SKILL.md 堆叠与 skill 创建无关的辅助文档（README/CHANGELOG 等）被明确禁止。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **两个核心脚本**：`scripts/init_skill.py`、`scripts/package_skill.py`。
- **init_skill.py**：用法 `scripts/init_skill.py <skill-name> --path <output-directory>`；说明以「The script:」列表形式给出（创建目录、生成 SKILL.md 模板、创建 scripts/references/assets、示例文件），**无每个参数的独立说明**，参数通过命令行示例传达。
- **package_skill.py**：用法 `scripts/package_skill.py <path/to/skill-folder> [./dist]`；说明为「Validate then Package」两步，以及验证项（frontmatter、命名、description、文件组织）、打包产物（.skill 文件）。**无参数表**，可选输出目录通过示例体现。
- **设计模式**：**脚本 = 流程节点**；每个脚本对应「创建流程」中的一步，文案侧重「做什么、产出什么、何时用」，而非完整 CLI 参考。
- **最佳实践**：对 init/package 类脚本，在 SKILL.md 中「命令 + 行为列表 + 可选参数示例」即可，详细用法可依赖 `--help` 或单独文档。
- **反模式**：若在 SKILL.md 为 init_skill 的每个 flag 写说明，会与「Concise is Key」原则冲突；保持脚本说明与原则一致。

---

## PPTX Skill 设计分析报告

### 1. Skill 名字

- **name**: `pptx`

直接对应 PowerPoint 文件，description 将「deck/slides/presentation」等说法归入。

### 2. Skill 功能概述

- 支持 .pptx 的读写、分析、创建、编辑、拆分合并、模板、notes、comments；
- 工具链：markitdown 抽文本、thumbnail.py 缩略图、unpack 操作 XML、pptxgenjs 从零创建；
- 设计理念：配色、布局、排版、间距及「Avoid」清单，避免 AI 味与低对比；
- 强制 QA：内容 QA + 视觉 QA（含子代理检查 prompt 模板）、验证循环、转图片脚本。

### 3. Skill 元数据中的 description

长 description：任何涉及 .pptx 的场景都触发（创建/读/编辑/合并拆分/模板/notes/comments）；用户提到「deck」「slides」「presentation」或 .pptx 文件名即触发；即使内容后续用于邮件/摘要，只要触及 pptx 也用此 skill。**强触发优先权**。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 「any time a .pptx file is involved in any way」建立强支配范围；大量短语枚举 + 「regardless of what they plan to do afterward」避免被其它技能抢占。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Quick Reference 表**：任务 → 指南/命令（markitdown / editing.md / pptxgenjs.md），快速路由。
- **Reading / Editing / Creating** 分块，细节引向 editing.md、pptxgenjs.md，保持主文档为索引 + 设计 + QA。
- **Design Ideas**：Before Starting（配色/主从/明暗/视觉母题）、Color Palettes 表、For Each Slide（布局/数据展示/视觉打磨）、Typography 表、Spacing、**Avoid** 清单（含「NEVER use accent lines under titles」等反 AI 模式）。
- **QA (Required)**：假定有问题、以找 bug 心态；Content QA（markitdown + grep placeholder）；Visual QA 强调用子代理、并给出完整检查 prompt 模板（Read and analyze these images... Report ALL issues）；Verification Loop（生成→转图→检查→修复→再验证）；「Do not declare success until at least one fix-and-verify cycle」。
- **Converting to Images**：soffice 转 PDF、pdftoppm 转 JPG，命令与单页重渲染示例。

### 6. 设计模式与（反）最佳实践

- **范式：内容 + 视觉双标准**：既管文本结构又管视觉与反 AI 痕迹。
- **范式：测试驱动验证**：转图 → 子代理检查 → 反馈修复。
- **范式：跨工具串联**：markitdown + soffice + pdftoppm 等组合。
- **反模式**：文档中明确列出的 Avoid 项（如标题下装饰线、低对比、纯文字幻灯片）即反模式清单。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **命令行/脚本**：`python -m markitdown presentation.pptx`、`python scripts/thumbnail.py presentation.pptx`、`python scripts/office/unpack.py presentation.pptx unpacked/`、`python scripts/office/soffice.py --headless --convert-to pdf output.pptx`、`pdftoppm -jpeg -r 150 output.pdf slide` 等。
- **文案特点**：每条以「用途 + 命令」形式出现（如 Reading Content、Converting to Images）；参数（文件路径、输出目录、-r 150、-f N -l N）均在示例中体现，**无单独参数表**；依赖「Quick Reference」表做任务→命令映射。
- **设计模式**：**任务→命令 + 示例**；多脚本多工具时，用表格与分节组织，避免逐脚本长说明。
- **最佳实践**：对「读/转/检」类流水线，在 SKILL.md 中按阶段（Reading / Editing / Creating / QA / Converting）给命令与示例即可，细节放 editing.md、pptxgenjs.md。
- **反模式**：若在主文档为 markitdown/soffice/pdftoppm 每个选项写文档，会冲淡设计理念与 QA 流程的权重。

---

## PDF Skill 设计分析报告

### 1. Skill 名字

- **name**: `pdf`

泛用型命名，配合 description 覆盖所有 PDF 相关任务。

### 2. Skill 功能概述

- 读写、抽取文本/表格、合并拆分、旋转、水印、加密解密、OCR、创建 PDF、提取图片等；
- Python：pypdf、pdfplumber、reportlab、pytesseract 等；命令行：pdftotext、qpdf、pdftk、pdfimages；
- 常见任务有代码示例；Quick Reference 表做「任务→最佳工具」映射；高级内容引向 REFERENCE.md、FORMS.md。

### 3. Skill 元数据中的 description

> Use this skill whenever the user wants to do anything with PDF files. ... If the user mentions a .pdf file or asks to produce one, use this skill.

「anything with PDF」强支配；长枚举覆盖水印/OCR 等偏门任务；触发条件简短（mention .pdf or produce one）。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 文件类型总管式描述；枚举保证偏门任务也能触发；简洁触发句便于记忆。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Overview + Quick Start**：pypdf 读取示例立即可用。
- **按库/工具分节**：pypdf（merge/split/metadata/rotate）、pdfplumber（text/tables、进阶表→DataFrame）、reportlab（canvas、多页、sub/super 标签）、pdftotext/qpdf/pdftk、Common Tasks（OCR、水印、提图、密码）。
- **重要警告**：reportlab 不用 Unicode 上下标、用 `<sub>`/`<super>` 标签，避免黑块。
- **Quick Reference 表**：Task → Best Tool → Command/Code，便于路由。
- **Next Steps**：指向 REFERENCE.md、FORMS.md，主文档保持「常用 + 索引」。

### 6. 设计模式与（反）最佳实践

- **范式：文件类型万能工具**：对 PDF 全栈操作。
- **范式：任务→工具矩阵**：Quick Reference 表可复用到其它 skill。
- **范式：Python + CLI 双轨**：脚本化与命令行并存。
- **反模式**：在正文中堆砌各库的全部 API 会稀释「常用路径」；当前以示例 + 表 + 外链平衡。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无独立「脚本」目录**：主要依赖第三方库与系统命令；调用单位是「库方法」或「命令行」。
- **库调用**：以「用途小节 + 代码块」呈现，如 Merge PDFs、Extract Tables；函数与参数通过示例体现（`PdfReader/PdfWriter`、`page.extract_text()`、`writer.encrypt(...)`），无单独 API 表。
- **命令行**：`pdftotext -layout input.pdf output.txt`、`qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf` 等，参数随示例给出，部分用注释说明（如 `-f 1 -l 5`）。
- **设计模式**：**按任务/按库组织 + 示例即文档**；参数语义融入示例与短注释。
- **最佳实践**：对多库多命令的 skill，用「任务→工具」表 + 每类 1～2 个示例即可，关键坑点（如 reportlab 上下标）单独强调。
- **反模式**：若为每个库写完整 API 列表，会与「Quick Start + Reference 外链」的定位冲突。

---

## MCP Builder Skill 设计分析报告

### 1. Skill 名字

- **name**: `mcp-builder`

针对 MCP server 开发的元技能，指导构建高质量 MCP 服务器。

### 2. Skill 功能概述

- 四阶段流程：Deep Research and Planning → Implementation → Review and Test → Create Evaluations；
- 覆盖协议理解、工具设计（命名、可发现性、错误信息、分页）、TS/Python 双栈、评估题库与 XML 格式；
- 通过 reference 文件与外部文档（sitemap、SDK README）组织详细内容。

### 3. Skill 元数据中的 description

> Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

强调 high-quality、LLM 与外部服务交互；明确 Python 与 Node/TS 两栈。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 「high-quality」与「well-designed tools」设定质量预期；「when building MCP servers」精确触发；双栈点名便于路由。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Process 四阶段**：每阶段下分子步骤（如 1.1 Understand Modern MCP Design、1.2 Study Protocol、1.3 Study Framework、1.4 Plan）；Phase 2 含 Set Up、Core Infrastructure、Tools（Input/Output Schema、Description、Implementation、Annotations）、Phase 3 代码质量与测试、Phase 4 评估（10 题、独立/只读/复杂/可验证/稳定、XML 格式）。
- **Reference Files**：按「何时加载」分组（Core / SDK / Language-Specific / Evaluation），用「Load First / During Phase 1/2 / During Phase 4」等说明，**渐进披露**。
- **Tool 设计要点**：命名、可发现性、错误信息可操作、分页、Schema（Zod/Pydantic）、readOnlyHint/destructiveHint 等，面向 agent 的设计明确。

### 6. 设计模式与（反）最佳实践

- **范式：LLM 集成中间层设计**：适用于「让 LLM 调外部 API」的通用蓝图。
- **范式：评估驱动**：Phase 4 要求 evaluation，形成闭环。
- **范式：多语言 + 主栈推荐**：TS 优先但保留 Python 路径。
- **反模式**：若跳过 Phase 1 直接写代码，易忽略协议与工具设计原则。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无 skill 自带可执行脚本**：skill 主要指导「如何写 MCP server」与「如何写 evaluation」，调用的是外部资源（WebFetch 拉 sitemap、SDK README、reference/*.md）。
- **「工具」即 MCP 协议中的 tools**：SKILL.md 中对「每个 tool」的说明体现在 Phase 2.3 Implement Tools：Input Schema（Zod/Pydantic、constraints、examples in descriptions）、Output Schema、Tool Description、Implementation（async、error handling、pagination）、Annotations（readOnlyHint 等）。**这是对「将要实现的工具」的规范说明**，而非对现有脚本的调用文档。
- **设计模式**：**规范型文档**；参数与字段通过「应包含」「Use Zod/Pydantic」「Include examples in field descriptions」等要求描述，无具体函数签名表，适合作为实现 checklist。
- **最佳实践**：对元技能/协议类 skill，工具说明写成「实现规范 + 示例结构」（如 evaluation XML 示例），而非 CLI/API 调用文档。
- **反模式**：若在 SKILL.md 中为不存在的脚本写参数表，会误导；本 skill 正确地将「工具」限定为 MCP server 暴露的 tools，其文档形态为规范与示例。

---

## Internal Comms Skill 设计分析报告

### 1. Skill 名字

- **name**: `internal-comms`

内部沟通类写作助手，配合公司偏好的格式与文体。

### 2. Skill 功能概述

- 为多种内部沟通文体（3P 更新、newsletter、FAQ、status report、incident report、project update 等）提供结构与风格指南；
- 通过 `examples/` 目录下的模板（3p-updates.md、company-newsletter.md、faq-answers.md、general-comms.md）指导写作；
- 根据用户请求识别沟通类型 → 加载对应 guideline → 按指南撰写。

### 3. Skill 元数据中的 description

> A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

强触发「whenever asked to write internal communications」；枚举文体；强调「formats that my company likes」体现公司定制。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 能力（resources for internal comms）+ 约束（company formats）+ 触发（whenever write...）+ 文体枚举，结构清晰。

### 5. SKILL.md 内容结构与 prompt 亮点

- **When to use / How to use**：先列场景，再 3 步（识别类型 → 加载对应 examples 文件 → 按该文件指示写）；无匹配时要求澄清或更多上下文。
- **Keywords**：3P updates, company newsletter, faqs... 便于检索与路由。
- **极简正文**：逻辑主要在 examples/ 中，SKILL.md 做路由与入口，是**轻量 Router Skill** 典型。

### 6. 设计模式与（反）最佳实践

- **范式：轻量 Router**：识别场景 + 选用哪个 reference；主体在 reference。
- **范式：按文体分文件**：每种沟通形式对应一个 example 文件，扩展点清晰。
- **反模式**：在 SKILL.md 重复 examples 中的详细格式会破坏「单源真相」。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无可执行脚本**：skill 依赖的是 `examples/*.md` 资源文件。
- **「调用」即加载文件**：Identify communication type → Load the appropriate guideline file from `examples/`（列文件名与对应场景）→ Follow instructions in that file。无函数或参数，**纯资源路由协议**。
- **设计模式**：**类型→文件映射 + 流程三步**；每个「工具」实为一份 guideline 文件，无需参数表。
- **最佳实践**：对文体/模板型 skill，SKILL.md 只保留「何时用哪份文件 + 怎么用」即可。
- **反模式**：若在 SKILL.md 内嵌各文体的完整写作细则，会与 examples 重复且拉长正文。

---

## Frontend Design Skill 设计分析报告

### 1. Skill 名字

- **name**: `frontend-design`

前端 UI 设计与实现质量，偏美学与布局，与 web-artifacts-builder 的工程/打包侧重区分。

### 2. Skill 功能概述

- 指导创建高设计质量、有辨识度、避免「AI slop」的前端界面；
- 适用于 component、page、app、poster、HTML/CSS/React 等；
- 提供设计思考框架（purpose/tone/constraints/differentiation）及排版、色彩、动效、布局、背景与细节、反 AI 审美等原则。

### 3. Skill 元数据中的 description

> Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications... Generates creative, polished code and UI design that avoids generic AI aesthetics.

用 distinctive、production-grade、high design quality、avoids generic AI aesthetics 连续限定风格；触发场景枚举（components/pages/applications...）；强调既出代码又出设计。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 能力与风格强绑定；大量触发场景提高召回；「avoids generic AI aesthetics」与正文反 AI 清单一致。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Design Thinking**：Purpose、Tone（极简/极繁/复古/有机/奢华/ playful/editorial/brutalist...）、Constraints、Differentiation；强调选一个明确方向并执行。
- **实现要求**：production-grade、functional、visually striking、cohesive、meticulously refined。
- **Frontend Aesthetics Guidelines**：Typography、Color & Theme、Motion、Spatial Composition、Backgrounds & Visual Details；**NEVER** 清单（Inter/Roboto、紫渐变、常见布局等）。
- **匹配复杂度与愿景**：极繁需要更多动画与效果代码，极简需要克制与细节。
- **鼓励多样化**：不同主题用不同字体与美学，避免都收敛到 Space Grotesk 等。

### 6. 设计模式与（反）最佳实践

- **范式：创作风格约束 Skill**：集中管审美与风格，与工程 skill 叠加使用。
- **范式：正反结合**：既要 bold aesthetics，又明确禁止 AI slop 元素。
- **反模式**：默认 Inter、紫渐变、居中布局等被明确标为禁止。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无脚本或工具调用**：skill 纯为指导性文档，无 CLI、无 Python/JS 工具模块，产出为「模型生成的前端代码与设计决策」。
- **不适用**：无函数/参数说明；设计模式与最佳实践已体现在第 5、6 节（原则与反例）。可在报告中注明「本 skill 无脚本或工具调用，第 7 节不适用」。

---

## DOCX Skill 设计分析报告

### 1. Skill 名字

- **name**: `docx`

Word 文档总管，绑定 .docx 的创建、读、编辑与专业排版。

### 2. Skill 功能概述

- 创建：docx 库（JS）、页面尺寸、样式、列表、表格、图片、TOC、页眉页脚及 Critical Rules；
- 编辑：unpack → edit XML → pack，支持 tracked changes、comments、图片嵌入；office 脚本（soffice/unpack/accept_changes/comment/validate/pack）；
- 大量 DOCX/XML 规范与常见坑（smart quotes、RSIDs、comment 标记等）。

### 3. Skill 元数据中的 description

长 description：任何涉及 Word/.docx 或要求目录/页眉页脚/letterhead 等专业排版的都触发；涵盖抽取、重组、插图、替换、tracked changes/comments；触发词含 report/memo/letter/template 等；排除 PDF/表格/Google Docs/无关编程。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 触发面广 + 触发词枚举 + 排除项明确，形成封闭边界。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Quick Reference 表**：Task → Approach（pandoc/unpack、docx-js、unpack-edit-pack）。
- **Creating**：docx-js 的 page size（DXA 表）、styles、lists（LevelFormat.BULLET/DECIMAL，禁止 Unicode bullet）、tables（双宽度、ShadingType.CLEAR、margins）、images（type 必填、altText）、PageBreak、TOC、Headers/Footers、**Critical Rules** 清单。
- **Editing**：三步顺序、smart quotes 实体表、comment.py 用法（unpacked/ 0 "Comment text"、--parent、--author）；Step 2 中「Use the Edit tool directly」「Do not write Python scripts」；Tracked changes/Comments 的 XML 示例与嵌套规则。
- **XML Reference**：schema 顺序、whitespace、RSIDs、insertion/deletion/minimal edits、删除整段、reject/restore 他人修改、comment 标记与嵌套、图片 relationship 与 EMU。

### 6. 设计模式与（反）最佳实践

- **范式：低自由度、强规范**：对易碎格式（docx XML）采用严密规则与清单。
- **范式：脚本 + XML 双轨**：高层 docx-js API 与底层 XML 编辑并存。
- **范式：错误恢复**：pack 时 auto-repair 部分问题。
- **反模式**：用 `\n`、Unicode bullet、WidthType.PERCENTAGE、ShadingType.SOLID 等被明确禁止。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **脚本**：`scripts/office/soffice.py`、`scripts/office/unpack.py`、`scripts/office/pack.py`、`scripts/office/validate.py`、`scripts/accept_changes.py`、`scripts/comment.py`。
- **soffice.py**：示例 `--headless --convert-to docx document.doc` 或 `--convert-to pdf`；参数通过用途（Converting .doc to .docx / Converting to Images）与示例传达，无完整选项表。
- **unpack/pack**：`unpack.py document.docx unpacked/`、`pack.py unpacked/ output.docx --original document.docx`；`--merge-runs false`、`--validate false` 等仅在需要时提及；**文案以「步骤 + 命令 + 行为说明」为主**（如 Unpack 会 pretty-print、merge runs、smart quotes 转实体）。
- **comment.py**：`comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"`、`--parent 0`、`--author "Custom Author"`；参数（目录、comment id、正文、parent、author）通过示例与短句说明，无单独参数表。
- **accept_changes.py**：`accept_changes.py input.docx output.docx`，无参数说明。
- **设计模式**：**按工作流步骤组织脚本**；每条命令对应 unpack/edit/pack/validate/accept/comment 中的一步；参数语义融入示例与「CRITICAL」类提示（如 XML 中 author 用 "Claude"、comment 标记为 w:p 的直接子节点）。
- **最佳实践**：对多脚本流水线，在 SKILL.md 中为每个脚本保留 1 个主用法示例 + 关键选项或约束即可，细节放在 XML Reference 与步骤说明中。
- **反模式**：若为 comment.py 的每个 flag 写独立小节，会冲淡「Edit tool 直接改、comment.py 处理 Boilerplate」的分工。

---

## Doc Coauthoring Skill 设计分析报告

### 1. Skill 名字

- **name**: `doc-coauthoring`

强调「共创」的文档写作流程，适用于 proposal、spec、decision doc、RFC 等长文档。

### 2. Skill 功能概述

- 三阶段：Context Gathering → Refinement & Structure → Reader Testing；
- 各阶段有详细步骤、提问策略、用户引导话术、artifact/文件使用方式；
- 支持用子代理或用户在新会话中做 Reader Testing，验证文档对「无上下文读者」的可读性。

### 3. Skill 元数据中的 description

> Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.

定义为 workflow 指南；触发短语枚举（write a doc、draft a proposal、create a spec...）。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 「structured workflow」「co-authoring」定位清晰；触发句覆盖常见说法。

### 5. SKILL.md 内容结构与 prompt 亮点

- **When to Offer / Initial offer**：说明三阶段并询问是否采用流程，若拒绝则 freeform。
- **Stage 1**：Initial Questions（文档类型、受众、影响、模板、约束）、Info Dumping、澄清问答（5–10 题）、exit condition、integrations 与 connector 提示。
- **Stage 2**：Section-by-section（clarifying questions → brainstorm 5–20 → curation → gap check → drafting → iterative refinement）、artifact 与 str_replace 使用、Quality Checking、Near Completion 时全文审阅。
- **Stage 3**：Reader Testing（有子代理则直接调用；无则指导用户新会话 + 问题列表）；Predict Reader Questions、Setup、Additional Checks、Report and Fix；Exit 条件为 Reader 能正确回答且无新 gap。
- **Final Review / Tips**：Tone、Handling Deviations、Context Management、Artifact Management、Quality over Speed。
- **高度流程化**：把写文档抽象为可重复协作过程；**Reader Claude 测试**体现对「别人拿文档再问 Claude」的优化。

### 6. 设计模式与（反）最佳实践

- **范式：工作流 Skill**：教模型如何引导人执行流程，而非仅自己生成。
- **范式：读者测试驱动质量**：用新 Claude 或新会话模拟读者。
- **范式：结构化对话模板**：每节「问题 → 头脑风暴 → 选择 → 起草 → 精修」循环。
- **反模式**：若跳过 Reader Testing 直接收尾，会违背「doc works for readers」的目标。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无 skill 自带脚本**：依赖的是通用能力（create_file、str_replace、子代理调用）与用户行为（粘贴、新会话测试）。
- **「工具」在正文中的体现**：Create artifact（create_file）、Edits（str_replace）、Provide artifact link after every change；子代理调用为「Invoke sub-agent with document + question」。无函数签名或参数表，**操作以自然语言步骤 + 原则**描述（如「Use str_replace for all edits」「Never reprint the whole doc」）。
- **设计模式**：**流程型 skill**；「工具」即 create_file/str_replace/子代理，其用法已融入各 Stage 的步骤说明，无需单独「脚本/工具调用」小节。
- **最佳实践**：对纯流程型 skill，在报告中注明「无独立脚本或工具 API；所用工具为通用编辑与子代理，其用法已嵌入流程描述」即可。
- **反模式**：若虚构「doc_coauthoring_run_stage.py」等脚本并写参数表，会与当前「引导式流程」设计不符。

---

## Canvas Design Skill 设计分析报告

### 1. Skill 名字

- **name**: `canvas-design`

画布式静态视觉设计（.png/.pdf），与 algorithmic-art（代码生成艺术）、pptx/docx（文档）区分。

### 2. Skill 功能概述

- 两阶段：Design Philosophy Creation（.md）→ Canvas Creation（.pdf/.png）；
- 强调极简文字、重视觉、原创与博物馆级工艺；提供设计哲学示例与原则、Deducing the Subtle Reference、多页选项与 Final Step 二次打磨。

### 3. Skill 元数据中的 description

> Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.

design philosophy 关键词呼应两阶段；触发场景（poster, art, design, static piece）；原创与版权约束。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 能力 + 触发场景 + 合规内嵌；与 algorithmic-art 的 description 结构类似（技术/哲学 + 触发 + 原创）。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Design Philosophy Creation**：命名 movement、4–6 段哲学、CRITICAL GUIDELINES（避免冗余、强调 craftsmanship、留创作空间）、Philosophy Examples（Concrete Poetry、Chromatic Language、Analog Meditation 等）、Essential Principles。
- **Deducing the Subtle Reference**：将用户主题作为隐性概念嵌入作品，不直白宣告。
- **Canvas Creation**：设计哲学 + 概念框架 → 画布表达；单页为主、重复图案与完美形状、稀疏排版与系统感、文字为语境元素、canvas-fonts、边界与留白、CRITICAL 工艺要求；输出 .pdf 或 .png + 哲学 .md。
- **FINAL STEP**：用户已要求「pristine, masterpiece」；二次打磨时少加图形、多精修既有构图，尊重极简原则。
- **MULTI-PAGE OPTION**：多页时风格统一又各有变化、可成系列叙事。
- 与 algorithmic-art 同属「哲学先行 + 媒介实现」家族，视觉媒介不同。

### 6. 设计模式与（反）最佳实践

- **范式：哲学先行 + 媒介实现**：与 algorithmic-art 一致。
- **范式：隐喻嵌入**：Subtle Reference 把主题藏进视觉语言。
- **范式：极高工艺要求**：多次强调 top-of-field、countless hours，驱动更精细输出。
- **反模式**：FINAL STEP 明确反对「加滤镜或新形状」的冲动，改为「让已有内容更像艺术品」。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无独立可执行脚本**：产出为模型生成的 .md（哲学）+ .pdf/.png（画布），实现方式依赖模型使用的绘图/排版工具或代码（未在 SKILL.md 中指定具体库或脚本）。
- **资源引用**：`./canvas-fonts` 目录被提及（「Search the ./canvas-fonts directory」「Use different fonts」）；无函数或 CLI，**仅「目录 + 使用意图」**的自然语言说明。
- **设计模式**：**资源型 + 两阶段协议**；「工具」为字体资源与哲学/画布产出规范，无参数表。
- **最佳实践**：对创作型 skill，若实现侧由模型自选（如 Python 绘图库或设计软件），SKILL.md 侧重输出标准与流程即可，不必绑定单一脚本。
- **反模式**：若在 SKILL.md 中为不存在的「canvas_render.py」写参数，会误导；当前写法正确地将「工具」限定为资源与原则。

---

## Brand Guidelines Skill 设计分析报告

### 1. Skill 名字

- **name**: `brand-guidelines`

应用 Anthropic 品牌颜色与字体的 skill，适用于需要品牌一致性的 artifact。

### 2. Skill 功能概述

- 提供 Anthropic 品牌颜色（主色/辅色）与字体（Poppins/Lora、fallback）；
- 说明如何应用到各类 artifact（尤指 PPT/文档）；Smart Font Application、Text Styling、Shape and Accent Colors；Font Management 与 Color Application 技术细节。

### 3. Skill 元数据中的 description

> Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.

适用范围为「需要 Anthropic 风格」的 artifact；触发语义（brand colors, style guidelines, visual formatting, company design standards）。

### 4. 对 description 的信息结构与 prompt 技巧分析

- 能力（applies brand colors and typography）+ 触发条件（when brand/style/visual formatting/design standards apply）；简短清晰。

### 5. SKILL.md 内容结构与 prompt 亮点

- **Overview + Keywords**：便于路由。
- **Brand Guidelines**：Colors（Main + Accent 列表与 hex）、Typography（Headings/Body + fallback）。
- **Features**：Smart Font Application（24pt+ → Poppins）、Text Styling、Shape and Accent Colors（循环 orange/blue/green）。
- **Technical Details**：Font Management（系统字体、fallback）、Color Application（RGB、python-pptx RGBColor）。
- **极简**：无流程、无脚本，纯「参数仓库」+ 应用逻辑简述。

### 6. 设计模式与（反）最佳实践

- **范式：品牌层 Skill**：与 theme-factory 类似，跨 artifact 的样式层。
- **范式：参数仓库**：主要提供颜色与字体规范，应用方式简短描述。
- **反模式**：若在正文中加入与品牌无关的通用设计建议，会稀释品牌专注度。

### 7. 脚本 / 工具调用文案与设计模式（如有）

- **无脚本或 CLI**：skill 提供的是品牌参数（hex、字体名）与应用规则（标题/正文字号与字体、形状用 accent、颜色用 RGB），**无可执行工具**。
- **「调用」即应用规则**：Read brand guidelines → Apply colors and fonts to deck/artifact；规则以「列表 + 短句」形式给出（如「Headings 24pt+: Poppins」「Non-text shapes use accent colors」），无函数或参数表。
- **设计模式**：**规范清单型**；与 theme-factory 的「主题文件」不同，本 skill 将规范直接写在 SKILL.md 中，便于常驻或快速查阅。
- **最佳实践**：对纯品牌/规范类 skill，保持「参数 + 应用场景」即可，无需虚构脚本或 API。
- **反模式**：若为「apply_brand_theme()」等不存在的函数写文档，会破坏当前「参数仓库」的定位。

---

# 建设 Skill 的设计模式与最佳实践（总结报告）

本报告基于前述 16 个官方 skill 的逐项分析，将其中反复出现的认知进行聚合与抽象，形成一套可复用的「建设 Skill」设计模式与最佳实践，供新 skill 设计与既有 skill 迭代时参考。

---

## 一、元数据与路由设计

### 1.1 description 的信息结构范式

**推荐结构（三至四层）：**

1. **能力声明（What it does）**  
   用 1～2 句话说明：做什么、用什么技术栈或关键特性、产出形态。  
   - 示例：*Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration.*  
   - 作用：缩小搜索空间，让模型在触发后不再在「用哪种库/要不要某特性」上摇摆。

2. **触发条件（When to use）**  
   用「Use this when…」或「Trigger when…」+ **一组典型用户说法或场景**。  
   - 技巧：既写通用说法（如「creating art using code」），也写专业说法（如「flow fields, particle systems」），提高 recall。  
   - 可加「even casually」「regardless of what they plan to do afterward」等，覆盖模糊表达或后续用途变化。

3. **边界与排除（Optional but powerful）**  
   用「Do NOT trigger when…」或「not for…」明确**不**负责的场景，形成封闭边界，减少与其它 skill 冲突。  
   - 示例：*Do NOT trigger when the primary deliverable is a Word document, HTML report...*  
   - 与「primary input/output」「deliverable must be X」等短语配合，在边界场景（如「把表格写成报告」）正确路由。

4. **合规与风格（Constraints & Safety）**  
   将安全或风格约束写成**正向目标**（如「Create original… rather than copying」），而不是单纯「不要侵权」，更易被模型当作默认偏好。

### 1.2 description 的 Prompt 技巧

- **高信息密度**：2～4 句话覆盖能力 + 触发 + 排除 + 合规，便于路由解析与记忆。  
- **典型触发短语枚举**：用一组代表性短语刻画边界，是可复用的 skill 路由技巧。  
- **技术栈与关键特性前置**：把「如何做」预先绑定到该 skill，减少推理分支。  
- **「触发信息只放在 description」**：Body 仅在触发后加载，因此「When to use」必须写在 description 中，body 中的「When to use」对路由无帮助（skill-creator 明确强调）。

### 1.3 命名

- **短、具辨识度**：便于在一组 skill 中检索与触发（如 `xlsx`、`pptx`、`pdf`、`docx`）。  
- **可带领域或平台**：如 `slack-gif-creator`、`algorithmic-art`，名字即传达范围。  
- **与 description 协同**：名字可泛（如 `pdf`），由 description 收紧到「以该物为主要输入/输出」等条件。

---

## 二、SKILL.md 正文结构与组织

### 2.1 渐进披露（Progressive Disclosure）

- **三层加载**：Metadata 常驻 → Body 触发后加载 → References/Scripts 按需加载。  
- **原则**：Context window 是共享资源；只加入模型真正缺少的信息，挑战「这段是否证明了自己的 token 成本」（skill-creator）。  
- **实践**：  
  - SKILL.md 控制在合理篇幅（如 <500 行），过长则拆到 references；  
  - 在 SKILL.md 中明确「何时读哪份 reference」，避免深层嵌套引用；  
  - 多变体/多领域时，按领域或变体拆文件（如 bigquery-skill 下 finance.md / sales.md），使单次只加载相关部分。

### 2.2 常见结构模式

- **Quick Reference 表**：任务 → 指南/命令/文件（pptx、pdf、docx、xlsx），便于快速路由到段落或外部文档。  
- **先标准后方法**：先声明输出质量标准（如「ZERO formula errors」「专业字体」），再给操作步骤（质量门槛优先，xlsx、pptx）。  
- **流程步骤编号化**：将复杂任务拆成 3～6 步（如 Init → Develop → Bundle → Display → Test），每步对应一个动作或脚本，便于模型按序执行。  
- **固定 vs 可变显式化**：在模板型 skill 中明确列出 FIXED（不可改）与 VARIABLE（可定制），减少模型误改不该改的部分（algorithmic-art、canvas 等）。

### 2.3 与 references/assets 的分工

- **SKILL.md**：核心流程、选择逻辑、必须遵守的规则、与触发后的「第一步」指引；仅保留对当前任务关键的内容。  
- **references/**：领域知识、API 细节、长示例、按领域/变体拆分的细节；在 SKILL.md 中通过链接或「See REFERENCE.md」引用。  
- **assets/**：模板、样例、字体等产出用资源；不在 SKILL.md 中展开实现细节，只说明用途与使用方式。  
- **避免重复**：同一信息只存在于 SKILL.md 或 reference 之一，不两处都写（skill-creator）。

---

## 三、Prompt 编写技巧（正文层）

### 3.1 分阶段思维引导

- **先抽象再实现**：例如先写「算法哲学/设计哲学」（.md），再写代码或画布（algorithmic-art、canvas-design）；避免模型直接跳到实现层，提高一致性与深度。  
- **多阶段 pipeline 明示**：如 User request → Philosophy → Implementation → Parameters → UI；在文档中显式写出，让模型按该顺序思考与输出。

### 3.2 示例与约束

- **Few-shot 行为示范**：用完整段落或小节作为「合格输出」的示范（如 PHILOSOPHY EXAMPLES），而不只是零散句子。  
- **示例 + 长度要求**：如「4–6 段 substantial paragraphs」，控制密度与篇幅，避免过短或过长。  
- **命名/风格示例**：列举 5～10 个 movement 名或主题名（风格统一），形成风格空间，引导新生成落在同一气质（algorithmic-art、theme-factory）。

### 3.3 正反对比与反模式列举

- **❌ WRONG / ✅ CORRECT**：用成对代码或行为对比，明确禁止模式与正确模式（xlsx 公式 vs 硬编码、webapp-testing 的 networkidle 前后）。  
- **Avoid / NEVER 清单**：集中列出反模式（如「不要标题下装饰线」「不要 Inter/紫渐变」「不要 Unicode bullet」），配合正向目标收缩输出空间。  
- **「不要什么」与「要什么」同时出现**：反模式防御更稳（如「模板是起点不是菜单」）。

### 3.4 强调与重复

- **关键概念高频重复**：用同义表达多次强调（如 craftsmanship、meticulously crafted、master-level），提高模型对该类要求的权重。  
- **多层级强调**：在 description、正文、模板说明等多处重复安全或质量要求（如原创、零公式错误），降低越界或敷衍概率。

### 3.5 Checklist 与 QA

- **Checklist 化**：将验证步骤写成可打勾清单（Verification Checklist、Common Pitfalls、Formula Testing Strategy），促使模型在结束时「自查」。  
- **QA 即找 bug**：假定首轮输出有问题，要求至少一轮「发现问题 → 修复 → 再验证」循环，而不是一次通过（pptx）。  
- **子代理/新会话测试**：用「读者 Claude」或新会话测试文档可读性，验证对无上下文读者的效果（doc-coauthoring、pptx 视觉 QA）。

### 3.6 人机协作流程

- **显式写清与人交互的顺序**：如「展示 theme-showcase → 询问选择 → 等待确认 → 再应用」（theme-factory），避免模型擅自代用户做选择。  
- **提供可选分支**：如「若用户拒绝流程则 freeform」（doc-coauthoring），保留用户主导权。

---

## 四、可抽象的设计范式

### 4.1 按技能类型

| 范式 | 含义 | 典型 skill |
|------|------|------------|
| **理念先行（Philosophy-First）** | 先产出抽象哲学/宣言（.md），再实现为代码或视觉 | algorithmic-art, canvas-design |
| **固定模板 + 可变内容（Template + Plugin）** | UI/结构/品牌固定，算法/参数/内容可变 | algorithmic-art, web-artifacts-builder |
| **质量门槛优先（Quality-Gate-First）** | 先定义零错误、保留模板等底线，再写步骤 | xlsx, pptx |
| **任务流水线（Pipeline）** | 用编号步骤定义端到端流程，每步对应工具或动作 | web-artifacts-builder, skill-creator, doc-coauthoring |
| **轻量 Router** | SKILL.md 只做「识别场景 → 选哪份 reference」，主体在 reference | internal-comms |
| **文件类型总管** | 某类文件（PDF/PPTX/DOCX/XLSX）的读写、转换、分析全包，用「primary input/output」界定 | pdf, pptx, docx, xlsx |
| **视觉/品牌层** | 只负责样式、主题、品牌，与内容编辑 skill 解耦 | theme-factory, brand-guidelines |
| **元技能（Meta-Skill）** | 指导如何定义或实现其它技能/系统 | skill-creator, mcp-builder |
| **工作流引导** | 教模型如何引导人执行多阶段流程，而非仅自己生成 | doc-coauthoring |
| **平台/场景优化** | 针对单一平台或场景深度优化（如 Slack GIF） | slack-gif-creator |

### 4.2 按资源与工具形态

- **Seeded System**：随机性全部收敛为「有 seed 的系统」+ 可复现 + seed 导航 UI（algorithmic-art）。  
- **概念/隐喻嵌入**：把用户主题作为隐性「概念种子」织入参数或视觉，不直白宣告（algorithmic-art, canvas-design）。  
- **Recon → Act**：先侦察（截图/DOM/选择器），再执行动作；适用于 UI 自动化（webapp-testing）。  
- **黑盒脚本优先**：复杂脚本通过 `--help` + 示例调用使用，避免读源码污染上下文（webapp-testing, skill-creator）。  
- **资源型协议**：无脚本时，「工具」即资源文件（themes/*.md、examples/*.md）；通过「类型→文件映射 + 使用步骤」描述（theme-factory, internal-comms）。  
- **参数仓库**：只提供规范列表（颜色、字体、规则），应用方式用短句描述（brand-guidelines）。

---

## 五、脚本与工具调用文案的设计模式与最佳实践

### 5.1 总体原则

- **面向 LLM 的脚本文档 ≠ 人类 API 文档**：不必详尽枚举每个参数与边缘 case；优先「任务导向 + 示例驱动」，用 1～2 种推荐调用覆盖大部分场景，关键参数用自然语言或示例内注释说明。  
- **参数语义靠任务上下文**：说明「什么时候需要该参数」「对行为的影响」，而非堆砌类型与默认值。  
- **控制 SKILL.md 中的脚本/API 篇幅**：若信息只影响少数调用路径，放到 REFERENCE 或脚本自身 `--help`，避免稀释主流程与设计理念。

### 5.2 按脚本/工具类型的文案模式

| 类型 | 推荐文案形态 | 示例 |
|------|--------------|------|
| **CLI 脚本（单入口）** | 1～2 条完整命令 + 一句「run with --help」；参数通过示例占位符与小标题传达 | webapp-testing with_server.py |
| **多脚本流水线** | 按工作流步骤分节，每脚本「用途 + 一条主命令 + 行为说明」；用 Quick Reference 表做任务→命令映射 | docx unpack/pack/comment；pptx markitdown/soffice/pdftoppm |
| **Python 工具模块** | 按模块分小节：一句用途 + 一个短示例 + 关键参数或枚举值在示例或紧跟的一行中 | slack-gif-creator GIFBuilder/validators/easing/frame_composer |
| **模板/资源** | 「FIXED / VARIABLE」或「输入—输出—作用」；不写函数签名，写「哪些可动/哪些不可动」及原因 | algorithmic-art viewer.html |
| **无脚本（资源/流程型）** | 不虚构脚本；「调用」写成资源列表 + 使用步骤，或通用能力（create_file/str_replace）融入流程描述 | theme-factory, internal-comms, doc-coauthoring |

### 5.3 输出契约与错误处理

- **用输出结构定义契约**：当脚本返回 JSON 等结构化数据时，在 SKILL.md 给出典型输出示例及字段语义（如 recalc.py 的 status/error_summary），便于模型解析与分支，而不必解释内部实现。  
- **关键坑点单独强调**：如 reportlab 上下标用标签不用 Unicode、docx 表格双宽度与 ShadingType.CLEAR，用「CRITICAL」「IMPORTANT」或单独小节标出。

### 5.4 反模式（脚本/工具说明）

- **在 SKILL.md 堆叠大量参数表**：会稀释「任务导向」风格，模型更难抓住主路径；应判断「是否影响大多数调用路径」再放入。  
- **把示例脚本当 pattern 菜单**：需明确「模板是起点不是菜单」「用原则创造新模式」，避免所有产出同质化。  
- **为不存在的脚本或 API 写参数表**：会误导；若 skill 无脚本，就写资源协议或流程，不虚构 CLI/API。  
- **破坏黑盒约定**：若已约定「先 --help、勿读源码」，就不要再在正文逐参数解释，否则易诱使模型去读源码。

---

## 六、反模式与注意事项（整体）

### 6.1 元数据与边界

- **触发条件只写在 body**：body 触发后才加载，对路由无效；when to use 必须在 description。  
- **描述过泛**：如只写「处理文档」，易与 docx/pdf/pptx 等冲突；用「primary input/output」或「deliverable must be X」收紧。  
- **缺少排除**：在有多 skill 重叠的领域（如表格、文档、前端），用「Do NOT trigger when…」可减少误触。

### 6.2 正文与结构

- **SKILL.md 过长且无拆分**：接近或超过 500 行且含大量细节时，考虑拆到 references，主文档保留流程与索引。  
- **重复引用层级过深**：reference 应直接从 SKILL.md 链接，避免 A→B→C 的多层跳转。  
- **与 skill 目标无关的文档**：如 README、CHANGELOG、INSTALLATION_GUIDE 等，skill-creator 明确不放入 skill 包内。

### 6.3 流程与质量

- **跳过关键阶段**：如哲学/设计阶段直接写代码、或跳过 Reader Testing 就收尾，会削弱一致性或可读性。  
- **一次通过即宣告成功**：应对易错输出（如幻灯片、公式）要求至少一轮「检查 → 修复 → 再验证」。  
- **忽略自由度匹配**：任务脆弱、易出错时应低自由度（明确步骤与规则）；开放创意时高自由度；skill-creator 的「narrow bridge vs open field」可作参照。

### 6.4 脚本与工具

- **为不存在的接口写文档**：没有脚本就写资源/流程；有脚本则写「命令 + 行为 + 输出示例」，不编造 API。  
- **示例脚本被当菜单用**：通过「这是结构参考/起点，不是可选样式列表」等文案防御同质化。  
- **过度解释脚本内部**：优先「做什么、输入输出、关键选项」；实现细节留给脚本自身或 reference。

---

## 七、总结：设计 Skill 时的检查清单

- **description**：是否包含「能力 + 触发条件（含典型说法）+ 必要时排除 + 合规/风格」？触发是否只写在 description？  
- **SKILL.md**：是否有清晰流程或 Quick Reference？是否「先标准后方法」、固定 vs 可变是否标明？是否避免与 reference 重复、是否控制篇幅与渐进披露？  
- **Prompt 技巧**：是否用示例与长度要求、WRONG/CORRECT、Avoid 清单、多层级强调、checklist 与 QA 要求？人机协作顺序是否写清？  
- **脚本/工具**：是否采用「任务导向 + 示例 + 输出契约」而非大段 API？是否避免虚构脚本、是否保持黑盒约定？  
- **范式匹配**：当前 skill 属于哪一类（文件总管/流水线/理念先行/路由/风格层/元技能等），是否与上述范式和反模式一致？

将上述认知内化后，新建或迭代 skill 时即可按「元数据 → 结构 → 正文 prompt → 脚本/工具文案 → 反模式自查」顺序落地，并与 16 个官方 skill 的实践保持一致、可维护、可扩展。

