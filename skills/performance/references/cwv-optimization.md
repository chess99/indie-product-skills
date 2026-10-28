# 按瓶颈优化

## 加载与 LCP

先把 LCP 拆成服务响应、资源加载延迟、下载和渲染延迟。图片大才调整尺寸/压缩；发现晚才处理 HTML 可发现性、优先级或 preload；被 JS 隐藏则修渲染路径。不要给所有图片 preload。

```html
<!-- 已确认的首屏关键图片；尺寸与真实素材比例一致 -->
<img src="/hero.webp" width="1200" height="675"
     fetchpriority="high" alt="产品操作预览">
<!-- 非首屏图片才考虑延迟加载 -->
<img src="/detail.webp" width="800" height="600"
     loading="lazy" decoding="async" alt="详细结果">
```

已有 `srcset`/`sizes` 时保持资源选择一致，避免 preload 下载另一个尺寸。优先复用框架图片和字体组件。字体检查字重、字符子集、fallback 度量及 `font-display`，不要一律注入异步 CSS hack。

## CLS

查看位移轨迹后处理实际来源：媒体宽高/比例、广告与异步组件预留空间、字体匹配、交互后内容的位置。预留尺寸应覆盖真实设备布局；不能用隐藏内容换分数。

## INP 与长任务

分开看输入排队、事件处理和下一帧绘制。拆分过长任务，减少同步布局与 DOM 工作；适合的计算移至 worker。先反馈交互状态，再处理非关键工作。TBT 改善后仍要复测真实交互。

第三方脚本应按用途、同意状态和时机加载。延迟 analytics 到首次交互会漏记未交互访客，不能默认这么做。确需多种触发器加载同一资源时使用共享的一次性状态；每种事件各自 `{once: true}` 仍可能导致重复加载。

## 缓存与服务器

区分静态版本资源、HTML、用户数据和 API。只有内容寻址资源适合 `public, max-age=31536000, immutable`。HTML 要考虑发布刷新；私有响应不能误设共享缓存。先查现有缓存/慢查询/重定向证据，再决定是否更换部署平台。

## 权威参考

- [Web Vitals](https://web.dev/articles/vitals)：指标和 p75 口径。
- [INP](https://web.dev/articles/inp)：真实交互与响应分解。
- [优化 LCP](https://web.dev/articles/optimize-lcp)：子阶段诊断。
- [PSI API](https://developers.google.com/speed/docs/insights/v5/get-started)：字段、错误与 CrUX 数据变化。

使用平台接口或阈值前核对当前文档；同一个名词在实验室与真实用户数据中可能有不同范围。
