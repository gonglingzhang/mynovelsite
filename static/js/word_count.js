// 创建小说新章节的时候判断输入的章节是否为阿拉伯数字，和判断标题字数
document.addEventListener("DOMContentLoaded", function () {
  const intInput = document.getElementById("IntInput");
  const chapterDiv = document.getElementById("chapterDiv");

  function updateTextColor() {
    if (intInput.value === "") {
      chapterDiv.style.color = "gray";
      intInput.style.borderBottomColor = "gray";
    } else {
      chapterDiv.style.color = "black";
      intInput.style.borderBottomColor = "black";
    }
  }
  // 初始化时设置颜色
  updateTextColor();
  // 监听输入事件
  intInput.addEventListener("input", updateTextColor);
  // 监听聚焦事件
  intInput.addEventListener("focus", updateTextColor);
  // 监听失焦事件
  intInput.addEventListener("blur", updateTextColor);
  // const intInput = document.getElementById('IntInput');
  const numberPrompt = document.getElementById("numberPrompt");

  intInput.addEventListener("input", function () {
    const value = this.value;
    const regex = /^\d*$/; // 正则表达式，检查是否为纯数字
    if (!regex.test(value)) {
      numberPrompt.style.display = "block";
    } else {
      numberPrompt.style.display = "none";
    }
  });

  const inputElement = document.getElementById("floatingInput");
  const wordCountElement = document.getElementById("wordCount");
  const maxLength = parseInt(inputElement.getAttribute("maxlength"));

  function updateWordCount() {
    const currentLength = inputElement.value.length;
    wordCountElement.textContent = `${currentLength}/${maxLength}`;
  }

  // 聚焦时显示字数统计 div
  inputElement.addEventListener("focus", () => {
    wordCountElement.style.display = "block";
  });

  // 失去聚焦时隐藏字数统计 div
  inputElement.addEventListener("blur", () => {
    wordCountElement.style.display = "none";
  });

  // 监听输入事件，输入内容变化时更新字数统计
  inputElement.addEventListener("input", updateWordCount);
  // 页面加载时初始化字数统计
  updateWordCount();
});
