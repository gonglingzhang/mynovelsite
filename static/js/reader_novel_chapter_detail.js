document.addEventListener("DOMContentLoaded", function () {
  // 常量定义
  const RIGHT_CONTAINER_VISIBILITY_KEY = "rightContainerVisibility";
  const THEME_KEY = "theme";
  const NIGHT_THEME = "night-theme";
  const DEFAULT_THEME = "default-theme";
  let isLoading = false; // 添加加载状态锁

  const FONT_COLOR_CONFIG = {
    "whiter-font-color": "#ffffff",
    "gray-font-color": "#888888",
    "green-font-color": "#4CAF50",
    "blue-font-color": "#2196F3",
    "orange-font-color": "#FF9800",
    "default-font-color": "#333333",
    "chapter-text-info-color": "rgba(108, 117, 125, 1)",
  };

  /*阅读小助手右侧设置显示开关 并且存储样式，样式不会因改变章节而变化*/
  // 删除原有的 toggleBtn 获取和事件绑定代码
  // 替换为事件委托实现
  document.addEventListener("click", function (e) {
    if (e.target.closest(".toggleRightBtn")) {
      e.preventDefault();
      const toggleBtn = e.target.closest(".toggleRightBtn");
      const toggleIcon = toggleBtn.querySelector(".toggleIcon");
      const toggleText = toggleBtn.querySelector(".toggleText");
      const currentVisibility = window.getComputedStyle(rightContainer).visibility;
      const newVisibility = currentVisibility === "hidden" ? "visible" : "hidden";

      // 更新当前按钮UI
      if (newVisibility === "hidden") {
        toggleIcon.innerHTML = `<path d="M11 4a4 4 0 0 1 0 8H8a5 5 0 0 0 2-4 5 5 0 0 0-2-4zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8M0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5" />`;
        toggleText.innerHTML = `&nbsp;显示右侧按钮`;
      } else {
        toggleIcon.innerHTML = `<path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8" />`;
        toggleText.innerHTML = `&nbsp;隐藏右侧按钮`;
      }

      // 更新所有同类按钮状态
      document.querySelectorAll(".toggleRightBtn").forEach((btn) => {
        const icon = btn.querySelector(".toggleIcon");
        const text = btn.querySelector(".toggleText");
        icon.innerHTML = toggleIcon.innerHTML;
        text.innerHTML = toggleText.innerHTML;
      });

      localStorage.setItem(RIGHT_CONTAINER_VISIBILITY_KEY, newVisibility);
      rightContainer.style.visibility = newVisibility;
    }
  });

  /*主题切换相关js*/
  // 获取所有主题按钮
  const themeButtons = document.querySelectorAll(".btn-setting-modal-theme .btn-theme");
  // 所有可用主题类名
  const themeClasses = ["default-theme", "green-theme", "cyan-theme", "ecru-theme", "orange-theme", "night-theme"];
  const body = document.body;

  // 获取日夜主题切换按钮
  const dayButton = document.getElementById("dayThemeToggle");
  const nightButton = document.getElementById("nightThemeToggle");

  // 统一主题切换处理函数
  function switchTheme(theme) {
    // 移除所有按钮的active类
    document.querySelectorAll(".btn-setting-modal-theme .btn-theme").forEach((button) => {
      button.classList.remove("active");
    });

    // 为当前选中的主题按钮添加active类
    const activeButton = document.getElementById(theme);
    if (activeButton) {
      activeButton.classList.add("active");
    }
    // 移除所有主题类
    themeClasses.forEach((t) => body.classList.remove(t));
    // 添加目标主题类
    body.classList.add(theme);
    // 保存主题偏好
    localStorage.setItem(THEME_KEY, theme);
    // 更新按钮显示状态
    if (theme === NIGHT_THEME) {
      dayButton.style.display = "inline-block";
      nightButton.style.display = "none";
    } else {
      dayButton.style.display = "none";
      nightButton.style.display = "inline-block";
    }
  }

  // 主题面板按钮点击事件
  themeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      switchTheme(this.id);
    });
  });

  // 日夜快捷切换按钮事件
  nightButton.addEventListener("click", function () {
    switchTheme(NIGHT_THEME);
  });

  dayButton.addEventListener("click", function () {
    switchTheme(DEFAULT_THEME);
  });

  // 页面加载时应用保存的主题
  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme && themeClasses.includes(savedTheme)) {
    switchTheme(savedTheme);
  } else {
    // 默认应用日间主题
    switchTheme(DEFAULT_THEME);
  }
  /*下滑超过一页，显示返回顶部按钮*/
  const scrollDiv = document.querySelector(".scroll-to-show");
  window.addEventListener("scroll", function () {
    const windowHeight = window.innerHeight;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    if (scrollTop >= windowHeight) {
      scrollDiv.style.display = "block";
    } else {
      scrollDiv.style.display = "none";
    }
  });

  /*返回顶部*/
  const backToTopBtn = document.getElementById("backToTop");
  backToTopBtn.addEventListener("click", function (e) {
    e.preventDefault(); // 阻止默认跳转行为
    window.scrollTo({
      top: 0,
      behavior: "smooth", // 平滑滚动
    });
  });

  /*上下章翻页相关js*/
  // 键盘左右键控制上下一章
  const previousChapterUrl = window.previousChapterUrl;
  const nextChapterUrl = window.nextChapterUrl;
  // 监听键盘事件
  document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft" && previousChapterUrl !== "null") {
      window.location.href = previousChapterUrl;
    } else if (event.key === "ArrowRight" && nextChapterUrl !== "null") {
      window.location.href = nextChapterUrl;
    }
  });

  /*目录模态框中的按钮被按下有背景色*/
  const buttons = document.querySelectorAll(".btn-modal-showNovelContentModal");
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      // 移除所有按钮的 active 类
      buttons.forEach((btn) => btn.classList.remove("active"));
      // 为当前点击的按钮添加 active 类
      this.classList.add("active");
    });
  });

  /* 监听模态框显示事件，点击目录的时候直接定位到对应章节 */
  const showNovelContentModal = document.getElementById("showNovelContentModal");
  if (showNovelContentModal) {
    showNovelContentModal.addEventListener("shown.bs.modal", function () {
      const currentChapter = document.getElementById("current-chapter");
      if (currentChapter) {
        currentChapter.style.color = "red";
        // 滚动到当前章节位置
        currentChapter.scrollIntoView({
          behavior: "smooth",
          // 让滚动操作以平滑动画的方式进行
          block: "start",
          // "start"：目标元素顶部与滚动容器顶部对齐。
          // "end"：目标元素底部与滚动容器底部对齐。
          // "center"：目标元素在滚动容器块级方向上居中显示。
          // "nearest"：选择最近的对齐方式，尽量减少滚动距离。
        });
      }
    });
  }

  /* 检查是否有滚动条，小说内容页面是否显示滚动条 */
  // 通过检查文档的 scrollHeight 和 clientHeight 来判断是否有滚动
  function checkScrollbar() {
    const html = document.documentElement;
    if (html.scrollHeight > html.clientHeight) {
      // 内容超出视口高度，有滚动条
      html.classList.add("has-scrollbar");
    } else {
      // 内容未超出视口高度，无滚动条
      html.classList.remove("has-scrollbar");
    }
  }
  window.addEventListener("load", checkScrollbar);
  window.addEventListener("resize", checkScrollbar);

  /* 目录模态框 - 卷和章节联动倒序切换（修复双击问题 + 自动定位当前章节） */
  const reverseBtn = document.querySelector(".btn-modal-reverse");
  let isReversed = false; // 标记当前是否为倒序状态
  let originalVolumeGroups = []; // 存储初始卷组顺序

  if (reverseBtn) {
    // 页面加载时保存原始卷组（仅执行一次）
    const modalBody = document.querySelector(".dir-modal-body");
    const volumeElements = Array.from(modalBody.children);
    // 分组：[[header1, list1], [header2, list2], ...]
    for (let i = 0; i < volumeElements.length; i += 2) {
      originalVolumeGroups.push(volumeElements.slice(i, i + 2));
    }
    reverseBtn.addEventListener("click", function () {
      isReversed = !isReversed;
      const btnContent = this.querySelector("span.d-flex");
      if (isReversed) {
        // 倒序状态：显示「正序」文本和向上排序 SVG
        btnContent.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-up" viewBox="0 0 16 16"><path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/></svg><span>正序</span>`;
      } else {
        // 正序状态：显示「倒序」文本和向下排序 SVG（修复语法错误：移除多余分号）
        btnContent.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-down" viewBox="0 0 16 16"><path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/></svg><span>倒序</span>`;
      } // 1. 反转卷顺序
      modalBody.innerHTML = "";
      const orderedVolumeGroups = isReversed ? [...originalVolumeGroups].reverse() : originalVolumeGroups;
      orderedVolumeGroups.forEach((group) => {
        group.forEach((el) => modalBody.appendChild(el.cloneNode(true)));
      });
      // 2. 反转章节顺序
      const chapterLists = document.querySelectorAll(".dir-chapter-list");
      const bookmarkChapterLists = document.querySelectorAll(".bookmark-chapter-list");
      // 反转目录
      chapterLists.forEach((list) => {
        const row = list.querySelector(".row");
        const chapters = Array.from(row.children);
        row.innerHTML = "";
        if (isReversed) {
          const orderedChapters = chapters.reverse();
          orderedChapters.forEach((chapter) => row.appendChild(chapter));
        } else {
          const orderedChapters = chapters;
          orderedChapters.forEach((chapter) => row.appendChild(chapter));
        }
      });
      // 反转书签
      bookmarkChapterLists.forEach((list) => {
        const row = list.querySelector(".row");
        const chapters = Array.from(row.children);
        row.innerHTML = "";
        const orderedChapters = chapters.reverse();
        orderedChapters.forEach((chapter) => row.appendChild(chapter));
      });

      // 3. 自动定位到当前章节（新增逻辑）
      const currentChapter = document.getElementById("current-chapter");
      if (currentChapter) {
        currentChapter.scrollIntoView({
          behavior: "smooth", // 平滑滚动
          block: "start", // 顶部对齐
        });
      }
      // 新增：重新绑定卷标题点击事件
      bindVolumeHeaderEvents();
    });
  }

  /*展开或者收起该卷下的小说章节*/
  // 将事件绑定逻辑封装为函数
  function bindVolumeHeaderEvents() {
    const volumeHeaders = document.querySelectorAll(".volume-header");
    // 先移除可能存在的重复事件监听（避免重复绑定）
    volumeHeaders.forEach((header) => {
      // 移除旧的事件监听器
      const oldListener = header.__clickListener;
      if (oldListener) {
        header.removeEventListener("click", oldListener);
      }
      // 创建新的事件监听器并绑定
      const newListener = function () {
        const chapterList = this.nextElementSibling;
        const svg = this.querySelector("svg");
        const path = svg.querySelector("path"); // 缓存path元素引用
        // 使用requestAnimationFrame优化渲染性能
        requestAnimationFrame(() => {
          // 切换折叠状态
          const isCollapsed = this.classList.toggle("collapsed");
          chapterList.classList.toggle("collapsed", isCollapsed);
          // 切换SVG图标（使用CSS类代替直接修改属性）
          if (isCollapsed) {
            svg.classList.remove("bi-caret-up-fill");
            svg.classList.add("bi-caret-down-fill");
            path.setAttribute("d", "M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z");
          } else {
            svg.classList.remove("bi-caret-down-fill");
            svg.classList.add("bi-caret-up-fill");
            path.setAttribute("d", "m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z");
          }
        });
      };
      // 存储监听器引用以便后续移除
      header.__clickListener = newListener;
      header.addEventListener("click", newListener);
    });
  }
  // 初始页面加载时绑定事件
  bindVolumeHeaderEvents();

  /* 模态框自适应定位与宽度控制 */
  // 获取阅读容器（复用变量，避免重复查询DOM）
  const readContainer = document.querySelector(".read-container");

  /* 1. 目录模态框宽度自适应与水平对齐 */
  function alignContentModal() {
    const contentModalDialog = document.querySelector("#showNovelContentModal .dir-modal-dialog");

    if (readContainer && contentModalDialog) {
      // 获取阅读容器位置信息
      const containerRect = readContainer.getBoundingClientRect();
      // 计算模态框宽度（阅读容器的100%）
      const modalWidth = containerRect.width * 1;

      // 设置宽度和水平居中
      contentModalDialog.style.maxWidth = `${modalWidth}px`;
      // 水平居中公式：阅读容器左边界 + (阅读容器宽度 - 模态框宽度)/2
      contentModalDialog.style.left = `${containerRect.left + (containerRect.width - modalWidth) / 2}px`;
      // 移除默认margin以避免冲突
      contentModalDialog.style.margin = "0";
    }
  }

  /* 2. 设置模态框右侧对齐 */
  function alignSettingsModal() {
    const settingsModalDialog = document.querySelector("#settingsModal .modal-dialog");
    const toolsModalDialog = document.querySelector("#toolsModal .modal-dialog");

    if (readContainer && settingsModalDialog) {
      // 计算设置模态框右侧与视口右侧的距离（对齐阅读容器右边缘）
      const viewportWidth = document.documentElement.clientWidth;
      const readContainerRect = readContainer.getBoundingClientRect();
      const readContainerRight = viewportWidth - readContainerRect.right;
      settingsModalDialog.style.right = `${readContainerRight}px`;
    }
    if (readContainer && toolsModalDialog) {
      // 计算设置模态框右侧与视口右侧的距离（对齐阅读容器右边缘）
      const viewportWidth = document.documentElement.clientWidth;
      const readContainerRect = readContainer.getBoundingClientRect();
      const readContainerRight = viewportWidth - readContainerRect.right;
      toolsModalDialog.style.right = `${readContainerRight}px`;
    }
  }

  /* 初始化与事件监听（统一管理两个模态框的自适应触发） */
  // 页面加载时初始化
  alignContentModal();
  alignSettingsModal();

  // 窗口大小变化时触发
  window.addEventListener("resize", () => {
    alignContentModal();
    alignSettingsModal();
  });
  // 阅读容器宽度变化时触发（用户调整页面宽度设置）
  if (readContainer) {
    const resizeObserver = new ResizeObserver(() => {
      alignContentModal();
      alignSettingsModal();
    });
    resizeObserver.observe(readContainer); // 观察阅读容器尺寸变化
  }
  // 模态框显示时强制对齐（确保打开时状态正确）
  const contentModal = document.getElementById("showNovelContentModal");
  if (contentModal) {
    contentModal.addEventListener("shown.bs.modal", alignContentModal);
  }
  const settingsModal = document.getElementById("settingsModal");
  if (settingsModal) {
    settingsModal.addEventListener("shown.bs.modal", alignSettingsModal);
  }

  /* 字体大小控制逻辑 */
  const fontSizeControl = {
    minSize: 12, // 最小字体大小（px）
    maxSize: 48, // 最大字体大小（px）
    step: 2, // 调整步长（px）
    currentSize: 30, // 默认字体大小（px）
  };
  const decreaseBtn = document.getElementById("decreaseFontSize");
  const increaseBtn = document.getElementById("increaseFontSize");
  const sizeDisplay = document.getElementById("currentFontSize");
  const chapterContent = document.querySelector(".chapter-content"); // 复用章节内容容器
  function updateFontSize() {
    sizeDisplay.textContent = `${fontSizeControl.currentSize}px`;
    // 修改为使用CSS变量控制字体大小
    document.documentElement.style.setProperty("--content-font-size-style", `${fontSizeControl.currentSize}px`);
    localStorage.setItem("fontSize", fontSizeControl.currentSize);
  }
  const savedSize = localStorage.getItem("fontSize");
  if (savedSize) {
    fontSizeControl.currentSize = Math.min(Math.max(parseInt(savedSize), fontSizeControl.minSize), fontSizeControl.maxSize);
  }
  updateFontSize();
  decreaseBtn.addEventListener("click", () => {
    if (fontSizeControl.currentSize > fontSizeControl.minSize) {
      fontSizeControl.currentSize -= fontSizeControl.step;
      updateFontSize();
    }
  });
  increaseBtn.addEventListener("click", () => {
    if (fontSizeControl.currentSize < fontSizeControl.maxSize) {
      fontSizeControl.currentSize += fontSizeControl.step;
      updateFontSize();
    }
  });

  /* 字体颜色控制逻辑 */

  // 初始化字体颜色
  function initFontColor() {
    const readContainer = document.querySelector(".read-container");
    const savedColor = localStorage.getItem("reader_font_color");
    const savedInfoColor = localStorage.getItem("chapterTextInfoColor");
    const colorButtons = document.querySelectorAll(".btn-font-color");

    // 从本地存储恢复颜色设置
    if (savedColor) {
      readContainer.style.setProperty("--read-container-text-color", savedColor);
    }
    if (savedInfoColor) {
      readContainer.style.setProperty("--chapter-text-info-color", savedInfoColor);
    }

    // 绑定按钮点击事件
    colorButtons.forEach((button) => {
      // 设置默认选中状态
      if (savedColor === FONT_COLOR_CONFIG[button.id] || (!savedColor && button.id === "default-font-color")) {
        button.classList.add("active");
      }

      // 点击切换颜色
      button.addEventListener("click", () => {
        // 移除所有按钮选中状态
        colorButtons.forEach((btn) => btn.classList.remove("active"));
        // 设置当前按钮选中状态
        button.classList.add("active");
        // 获取并应用颜色值
        const color = FONT_COLOR_CONFIG[button.id];
        readContainer.style.setProperty("--read-container-text-color", color);
        readContainer.style.setProperty("--chapter-text-info-color", color);
        // 保存到本地存储
        localStorage.setItem("reader_font_color", color);
        localStorage.setItem("chapterTextInfoColor", color);
      });
    });
  }
  initFontColor();

  /* 行间距控制逻辑 */
  const rootElement = document.documentElement;
  const lineHeightConfig = {
    default: "100%",
    storageKey: "lineHeight",
    valueMap: { "80%": 0.8, "100%": 1.0, "125%": 1.25, "150%": 1.5, "200%": 2.0, "300%": 3.0 },
  };
  const lineHeightButtons = document.querySelectorAll(".btn-setting-modal-line-height .btn");
  function applyLineHeight(buttonText) {
    const lineHeight = lineHeightConfig.valueMap[buttonText];
    if (lineHeight) {
      // 修改为使用CSS变量控制行间距
      rootElement.style.setProperty("--content-line-height-style", lineHeight);
      localStorage.setItem(lineHeightConfig.storageKey, buttonText);
      lineHeightButtons.forEach((btn) => btn.classList.toggle("active", btn.textContent.trim() === buttonText));
    }
  }
  function initLineHeight() {
    const savedLineHeight = localStorage.getItem(lineHeightConfig.storageKey) || lineHeightConfig.default;
    applyLineHeight(savedLineHeight);
  }
  lineHeightButtons.forEach((button) => button.addEventListener("click", () => applyLineHeight(button.textContent.trim())));
  initLineHeight();

  /* 页面宽度控制逻辑 */
  const contentWidthConfig = {
    storageKey: "contentWidth",
    defaultWidth: "800",
    cssVariable: "--read-container-width",
  };
  const contentWidthButtons = document.querySelectorAll(".btn-setting-modal-content-width .font-selector");

  function applyContentWidth(width) {
    rootElement.style.setProperty(contentWidthConfig.cssVariable, `${width}px`);
    localStorage.setItem(contentWidthConfig.storageKey, width);
    contentWidthButtons.forEach((btn) => btn.classList.toggle("active", btn.textContent.trim() === width));
  }
  function initContentWidth() {
    const savedWidth = localStorage.getItem(contentWidthConfig.storageKey) || contentWidthConfig.defaultWidth;
    applyContentWidth(savedWidth);
  }
  contentWidthButtons.forEach((button) => button.addEventListener("click", () => applyContentWidth(button.textContent.trim())));
  initContentWidth();

  /* 正文字体控制逻辑 */
  const fontConfig = {
    storageKey: "contentFont", // 本地存储键名
    defaultFont: "KaiTi", // 默认字体（与CSS初始值保持一致）
    cssVariable: "--content-font-family-style", // 关联的CSS变量
  };
  const fontButtons = document.querySelectorAll(".btn-setting-modal-font .font-selector");
  // 应用选中的字体设置
  function applyFont(fontFamily) {
    // 更新CSS变量（修复变量名错误）
    rootElement.style.setProperty(fontConfig.cssVariable, `"${fontFamily}", serif`);
    localStorage.setItem(fontConfig.storageKey, fontFamily);
    fontButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.font === fontFamily);
    });
  }
  // 初始化字体设置（页面加载时执行）
  function initFont() {
    // 从localStorage读取保存的字体，无则使用默认值
    const savedFont = localStorage.getItem(fontConfig.storageKey) || fontConfig.defaultFont;
    applyFont(savedFont);
  }
  // 绑定按钮点击事件
  fontButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const selectedFont = button.dataset.font; // 获取data-font属性值（如"SimSun"）
      applyFont(selectedFont);
    });
  });
  // 页面加载时初始化字体设置
  initFont();

  /* 恢复默认样式功能 */
  const restoreDefaultsBtn = document.querySelector("#resetSettings");
  if (restoreDefaultsBtn) {
    restoreDefaultsBtn.addEventListener("click", () => {
      // 清除所有样式相关的localStorage项
      localStorage.removeItem(THEME_KEY);
      localStorage.removeItem("fontSize");
      localStorage.removeItem(lineHeightConfig.storageKey);
      localStorage.removeItem(contentWidthConfig.storageKey);
      localStorage.removeItem(fontConfig.storageKey);
      // 添加字体颜色存储清除
      localStorage.removeItem("reader_font_color");
      localStorage.removeItem("chapterTextInfoColor");
      // 修复：使用已定义的switchTheme函数替代未定义的updateThemeUI
      switchTheme(DEFAULT_THEME);
      // 重置字体大小到默认值
      fontSizeControl.currentSize = 30;
      updateFontSize();
      // 重置行间距到默认值
      initLineHeight();
      // 重置页面宽度到默认值
      initContentWidth();
      // 重置字体到默认值
      initFont();
      // 添加字体颜色重置逻辑
      const readContainer = document.querySelector(".read-container");
      const defaultColor = FONT_COLOR_CONFIG["default-font-color"];
      const chapter_text_info_color = FONT_COLOR_CONFIG["chapter-text-info-color"];
      // 直接操作.read-container元素
      if (readContainer) {
        readContainer.style.setProperty("--read-container-text-color", defaultColor);
        readContainer.style.setProperty("--chapter-text-info-color", chapter_text_info_color);
      }
      // 更新按钮选中状态
      const colorButtons = document.querySelectorAll(".btn-font-color");
      colorButtons.forEach((btn) => btn.classList.remove("active"));
      document.getElementById("default-font-color").classList.add("active");
      // 关闭设置模态框
      // const settingsModal = bootstrap.Modal.getInstance(document.getElementById("settingsModal"));
      // settingsModal.hide();
    });
  }

  /*添加翻页模式控制脚本 */
  // 获取按钮元素
  const chapterBtn = document.getElementById("chapter-pageMode");
  const scrollBtn = document.getElementById("scroll-pageMode");
  const contentContainer = document.querySelector(".read-container");
  const changeChapterDiv = document.getElementById("changeChapterContainer");
  // 获取链接元素
  const chapterLinkElement = document.querySelector(".breadcrumb-item.active a");
  // 安全获取 href 属性值（避免 null 错误）
  const chapterHref = chapterLinkElement ? chapterLinkElement.href : null; // 初始化默认模式
  let currentMode = "chapter";
  // 滚动翻页模式激活函数
  function activateScrollMode() {
    currentMode = "scroll";
    changeChapterDiv.style.setProperty("display", "none", "important");
    chapterBtn.classList.remove("active");
    scrollBtn.classList.add("active");
    window.addEventListener("scroll", handleScroll);
    // 新增：主动触发一次滚动检查，处理内容不足一页的情况
    handleScroll();
    window.addEventListener("scroll", handleScroll); // 确认事件绑定
  }
  // 滚动事件处理函数
  function handleScroll() {
    const scrollPosition = window.scrollY;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    // 当滚动到底部80%时加载下一章
    if (scrollPosition + windowHeight >= documentHeight * 0.8) {
      if (currentMode === "scroll") {
        loadNextChapter(); // 实现加载下一章的函数
      }
    }
    updateVisibleChapterLink();
  }
  // 1. 添加可见性检查的独立函数
  let currentChapterLink = null;
  function updateVisibleChapterLink() {
    requestAnimationFrame(() => {
      const activeLinks = document.querySelectorAll(".breadcrumb-item.active a");

      for (const link of activeLinks) {
        const rect = link.getBoundingClientRect();
        if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
          currentChapterLink = link;
          break;
        }
      }
      if (currentChapterLink) {
        console.log("当前章节链接:", currentChapterLink.href);
      } else {
        console.log("未找到可见的章节链接");
      }
    });
  }

  function activateChapterMode() {
    stopAutoScroll();
    // 根据currentChapterLink是否存在决定访问哪个链接
    if (currentChapterLink === null) {
      // currentChapterLink为null时访问chapterHref
      window.location.href = chapterHref;
    } else {
      // currentChapterLink存在时访问其href属性
      window.location.href = currentChapterLink.href;
    }
  }

  // 添加翻页逻辑实现
  function loadNextChapter() {
    const nextUrl = window.nextChapterUrl;
    if (!nextUrl || isLoading) return; // 没有下一章或正在加载则退出
    // 章节模式下直接跳转（新增逻辑）
    if (currentMode === "chapter") {
      window.location.href = nextUrl;
      return;
    }
    if (currentMode === "scroll") {
      isLoading = true; // 设置加载状态
      fetch(nextUrl)
        .then((response) => response.text())
        .then((html) => {
          const tempDiv = document.createElement("div");
          tempDiv.innerHTML = html;
          // 获取新章节信息和内容
          const readContainer = tempDiv.querySelector(".read-container");
          // 移除.change-chapter元素
          const changeChapterDiv = readContainer.querySelector(".change-chapter");
          if (changeChapterDiv) {
            changeChapterDiv.remove();
          }
          // 构建新章节HTML（包含信息和内容）
          let newChapterHTML = "";
          newChapterHTML += '<hr class="chapter-separator">'; // 添加章节分隔线
          // 关键修复：为动态章节添加URL属性
          // newChapterHTML += `<div class="chapter-container" data-chapter-url="${nextUrl}">`;
          newChapterHTML += readContainer.innerHTML;
          // newChapterHTML += "</div>";
          // 追加新章节内容
          if (newChapterHTML) {
            contentContainer.innerHTML += newChapterHTML;
            updateVisibleChapterLink(); // 新增：内容更新后检查可见性
          }
          // 更新下一章URL（从新页面HTML中提取）
          const scripts = tempDiv.querySelectorAll("script");
          let found = false;
          scripts.forEach((script) => {
            if (script.textContent.includes("window.nextChapterUrl")) {
              // console.log("找到更新nextChapterUrl的脚本:", script.textContent);
              eval(script.textContent);
              found = true;
            }
          });
          if (!found) {
            const nextChapterMeta = tempDiv.querySelector('meta[name="next-chapter-url"]');
            if (nextChapterMeta) {
              window.nextChapterUrl = nextChapterMeta.content;
            } else {
              // 添加错误处理
              console.error("未找到下一章URL");
              window.nextChapterUrl = null;
            }
          }
        })
        .catch((error) => {
          console.error("加载下一章失败:", error);
        })
        .finally(() => {
          isLoading = false; // 无论成功失败都重置加载状态
        });
    }
    setTimeout(handleScroll, 0); // 延迟触发，确保 DOM 更新完成
  }
  // 绑定按钮点击事件
  chapterBtn.addEventListener("click", function () {
    currentMode = "chapter";
    activateChapterMode(); // 只在切换模式时执行一次
  });
  scrollBtn.addEventListener("click", activateScrollMode);

  /* 朗读功能实现 */
  /* 朗读功能实现 */
  const ReadAloud = {
    speech: null,
    utterance: null,
    isSpeaking: false,
    voices: [],
    currentVoice: null,
    activeButton: null, // 跟踪当前激活的按钮
    readingQueue: [],
    currentParagraphIndex: 0,
    contentObserver: null,
    lastReadPosition: 0,

    init() {
      // 检查浏览器支持
      if (!("speechSynthesis" in window)) {
        console.error("浏览器不支持文本朗读功能");
        return;
      }
      this.speech = window.speechSynthesis;
      this.utterance = new SpeechSynthesisUtterance();
      this.getVoices();
      window.speechSynthesis.onvoiceschanged = () => this.getVoices();
      this.bindEvents();
      this.initContentObserver();
    },

    getVoices() {
      this.voices = this.speech.getVoices();
    },

    bindEvents() {
      // 男声阅读按钮 - 使用箭头函数绑定this
      const maleBtn = document.getElementById("chapter-readMode-male");
      const femaleBtn = document.getElementById("scroll-readMode-female");

      maleBtn.addEventListener("click", () => this.toggleReading("male", maleBtn));
      femaleBtn.addEventListener("click", () => this.toggleReading("female", femaleBtn));
    },

    selectVoice(gender) {
      const femaleVoices = ["Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)", "Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)", "Microsoft Yaoyao - Chinese (Simplified, PRC)", "Microsoft Huihui - Chinese (Simplified, PRC)"];
      const maleVoices = ["Microsoft Yunxi Online (Natural) - Chinese (Mainland)", "Microsoft Yunjian Online (Natural) - Chinese (Mainland)", "Microsoft Yunyang Online (Natural) - Chinese (Mainland)"];
      const isMale = gender === "male";
      const defaultVoiceName = isMale ? "Microsoft Yunyang Online (Natural) - Chinese (Mainland)" : "Microsoft Yaoyao - Chinese (Simplified, PRC)";
      const voicePattern = isMale ? /male|男|男声|男士|先生|boy|man|kangkang|zhijun|wang/i : /female|女|女声|女士|girl|woman/i;
      const chinesePattern = /chinese|zh|中文|普通话|mandarin/i;
      const dialectPattern = /东北|四川|粤语|方言|regional|dialect/i;
      const isChineseVoice = (voice) => chinesePattern.test(voice.name) && !dialectPattern.test(voice.name) && (voice.lang === "zh-CN" || voice.lang === "zh" || voice.lang === "zh-Hans" || voice.lang === "zh-Hans-CN");
      console.log(
        "可用语音列表:",
        this.voices.filter((v) => v.lang?.startsWith("zh")).map((v) => ({ id: v.voiceURI, name: v.name, lang: v.lang, gender: v.gender }))
      );
      if (isMale) {
        const specifiedVoice = this.voices.find((voice) => voice.name === defaultVoiceName);
        if (specifiedVoice) {
          console.log("选中指定男声:", specifiedVoice.name);
          return specifiedVoice;
        }
        const preciseVoice = this.voices.find((voice) => isChineseVoice(voice) && voicePattern.test(voice.name) && (voice.gender === "male" || voice.gender === "VoiceGenderMale"));
        if (preciseVoice) {
          console.log("选中精确中文普通话男声:", preciseVoice.name);
          return preciseVoice;
        }
        const namedVoice = this.voices.find((voice) => isChineseVoice(voice) && voicePattern.test(voice.name));
        if (namedVoice) {
          console.log("选中中文男声:", namedVoice.name);
          return namedVoice;
        }
      } else {
        const femaleVoiceMatch = this.voices.find((voice) => femaleVoices.includes(voice.name));
        if (femaleVoiceMatch) {
          console.log("选中指定女声:", femaleVoiceMatch.name);
          return femaleVoiceMatch;
        }
        const preciseVoice = this.voices.find((voice) => isChineseVoice(voice) && voicePattern.test(voice.name) && (voice.gender === "female" || voice.gender === "VoiceGenderFemale"));
        if (preciseVoice) {
          console.log("选中精确中文普通话女声:", preciseVoice.name);
          return preciseVoice;
        }
        const namedVoice = this.voices.find((voice) => isChineseVoice(voice) && voicePattern.test(voice.name));
        if (namedVoice) {
          console.log("选中中文女声:", namedVoice.name);
          return namedVoice;
        }
      }

      const defaultChineseVoice = this.voices.find((voice) => voice.lang === "zh-CN" && !dialectPattern.test(voice.name));
      if (defaultChineseVoice) {
        console.log("使用默认中文语音:", defaultChineseVoice.name);
        return defaultChineseVoice;
      }
      const genderText = isMale ? "男声" : "女声";
      console.error(`未找到中文普通话${genderText}语音，请确保浏览器已安装相关语音包。`);
      alert(`未找到中文普通话${genderText}语音，请尝试更换浏览器或安装${genderText}语音包。`);
      return null;
    },

    toggleReading(gender, button) {
      if (this.isSpeaking && this.activeButton === button) {
        this.stopReading();
      } else if (this.isSpeaking && this.activeButton !== button) {
        this.stopReading();
        setTimeout(() => this.startReading(gender, button), 300);
      } else {
        this.startReading(gender, button);
      }
    },

    startReading(gender, button) {
      const chapterContent = document.querySelector(".read-container") || document.body;
      const text = chapterContent.innerText.trim();
      if (!text) {
        alert("没有找到可朗读的内容");
        return;
      }
      this.currentVoice = this.selectVoice(gender);
      if (!this.currentVoice) return;
      this.readingQueue = [];
      this.currentParagraphIndex = 0;
      this.lastReadPosition = 0;
      this.processNewContent(chapterContent);
      this.isSpeaking = true;
      this.activeButton = button;
      this.updateButton(button, true);
      if (this.readingQueue.length > 0) {
        this.processReadingQueue();
      }
    },

    processReadingQueue() {
      if (this.readingQueue.length === 0) {
        this.cleanup();
        return;
      }

      const currentText = this.readingQueue.shift();
      this.currentParagraphIndex++;
      this.utterance.text = currentText;
      this.utterance.voice = this.currentVoice;
      this.utterance.lang = "zh-CN";
      this.utterance.rate = 1;
      this.utterance.pitch = 1;
      this.utterance.volume = 1;

      this.utterance.onend = () => {
        if (this.readingQueue.length > 0) {
          this.processReadingQueue();
        } else {
          this.cleanup();
        }
      };

      this.utterance.onerror = (event) => {
        if (event.error !== "interrupted") {
          console.error("朗读出错:", event.error);
        }
        this.cleanup();
      };
      this.speech.speak(this.utterance);
      console.log(`正在朗读第${this.currentParagraphIndex}段:`, currentText.substring(0, 30) + "...");
    },

    stopReading() {
      if (this.speech) {
        this.speech.cancel();
      }
      this.cleanup();
    },

    cleanup() {
      if (this.activeButton) {
        this.updateButton(this.activeButton, false);
        this.activeButton = null;
      }
      this.isSpeaking = false;
      this.currentVoice = null;
      this.readingQueue = [];
      this.currentParagraphIndex = 0;
      this.lastReadPosition = 0;
    },

    updateButton(button, isActive) {
      if (isActive) {
        button.textContent = "停止朗读";
        button.classList.add("active");
      } else {
        const isMaleButton = button.id === "chapter-readMode-male";
        button.textContent = isMaleButton ? "男声阅读" : "女声阅读";
        button.classList.remove("active");
      }
    },

    initContentObserver() {
      const chapterContent = document.querySelector(".read-container") || document.body;
      if (!chapterContent) return;
      const config = {
        childList: true,
        subtree: true,
        characterData: true,
      };
      this.contentObserver = new MutationObserver((mutations) => {
        if (!this.isSpeaking) return;
        this.processNewContent(chapterContent);
      });
      this.contentObserver.observe(chapterContent, config);
    },

    processNewContent(container) {
      const fullText = container.innerText.trim();
      const newText = fullText.substring(this.lastReadPosition);
      if (newText.length > 0) {
        const paragraphs = newText.split(/[\n\r]+/).filter((p) => p.trim().length > 0);
        if (paragraphs.length > 0) {
          this.readingQueue.push(...paragraphs);
          this.lastReadPosition = fullText.length;
          console.log(`检测到${paragraphs.length}段新内容，已添加到朗读队列`);
        }
      }
    },
  };
  ReadAloud.init();
});
/* 自动下拉功能实现 - 简化版 */
const AutoScroll = {
  isActive: false,
  speed: 70, // 默认中速(值越小速度越快)
  intervalId: null,
  presets: {
    100: ["慢速", "slow"],
    70: ["中速", "medium"],
    30: ["快速", "fast"],
  },
};

function startAutoScroll() {
  if (AutoScroll.isActive) return;
  AutoScroll.isActive = true;
  updateAutoScrollButtonText();
  const scrollStep = Math.max(1, Math.floor(500 / AutoScroll.speed));
  AutoScroll.intervalId = setInterval(() => {
    window.scrollBy(0, scrollStep);
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
      stopAutoScroll();
      updateAutoScrollButtonText();
      if (ReadAloud.isSpeaking) {
        setTimeout(() => {
          const container = document.querySelector(".read-container") || document.body;
          ReadAloud.processNewContent(container);
        }, 1000);
      }
    }
  }, 50);
}

function stopAutoScroll() {
  if (!AutoScroll.isActive) return;
  AutoScroll.isActive = false;
  clearInterval(AutoScroll.intervalId);
  AutoScroll.intervalId = null;
  updateAutoScrollButtonText();
}

function updateAutoScrollButtonText() {
  const button = document.querySelector('[data-action="toggle"]');
  if (button) {
    button.textContent = AutoScroll.isActive ? "停止滚动" : "自动滚动";
    button.classList.toggle("active", AutoScroll.isActive);
    updateActiveButton(AutoScroll.isActive);
  }
}

function setAutoScrollSpeed(speed) {
  if (typeof speed !== "number" || speed < 1 || speed > 2000) {
    console.error("无效的滚动速度值:", speed);
    return;
  }
  AutoScroll.speed = speed;
  syncSpeedInput();
  updateSpeedDisplay();
  updateActiveButton();
  if (AutoScroll.isActive) {
    stopAutoScroll();
    startAutoScroll();
  }
}

function syncSpeedInput() {
  const input = document.getElementById("custom-scroll-speed");
  if (input) input.value = AutoScroll.speed;
}

function updateSpeedDisplay() {
  const display = document.getElementById("current-speed-display");
  if (!display) return;
  const preset = Object.entries(AutoScroll.presets).find(([value]) => Number(value) === AutoScroll.speed);
  display.textContent = preset ? preset[1][0] : "自定义";
}

function updateActiveButton() {
  document.querySelectorAll(".speed-btn").forEach((btn) => btn.classList.remove("active"));
  const preset = Object.entries(AutoScroll.presets).find(([value]) => Number(value) === AutoScroll.speed);
  if (preset) {
    const btn = document.querySelector(`.speed-btn[data-speed="${preset[1][1]}"]`);
    if (btn) btn.classList.add("active");
  } else {
    const customBtn = document.querySelector('.speed-btn[data-speed="diy"]');
    if (customBtn) customBtn.classList.add("active");
  }
}

document.addEventListener("click", (e) => {
  if (e.target.matches('[data-action="toggle"]')) {
    const button = e.target.closest(".auto-scroll-btn");
    AutoScroll.isActive ? stopAutoScroll() : startAutoScroll();
    button.classList.toggle("active", AutoScroll.isActive);
  }
  if (e.target.matches(".speed-btn")) {
    const speed = Number(e.target.dataset.speed);
    if (!isNaN(speed)) {
      setAutoScrollSpeed(speed);
    }
  }
});

document.getElementById("custom-scroll-speed")?.addEventListener("change", (e) => {
  const speed = parseInt(e.target.value, 10);
  if (!isNaN(speed)) {
    setAutoScrollSpeed(speed);
  }
});

$(document).ready(function () {
  $(".tab-btn").click(function () {
    // 移除所有按钮的active类
    $(".tab-btn").removeClass("active");
    // 给当前点击的按钮添加active类
    $(this).addClass("active");

    // 隐藏所有内容区域
    $(".dir-modal-body").hide();
    // 显示目标内容区域
    const target = $(this).data("target");
    $("#" + target).show();
  });
});
