// mian 星星特效
document.addEventListener("DOMContentLoaded", function () {
  function createStarsInContainer(container, starsId) {
    // 判断是否有container 即 "footer" 或 "header"
    if (!container) return;
    let starsDiv = container.querySelector("#" + starsId);
    // 判断container中是否有指定id的div，没有就加一个
    if (!starsDiv) {
      starsDiv = document.createElement("div");
      starsDiv.id = starsId;
      container.appendChild(starsDiv);
    } else {
      container.appendChild(starsDiv);
    }
    // 仅在container没有定位时设置为相对定位，避免覆盖如fixed-bottom的fixed定位
    if (getComputedStyle(container).position === "static") {
      container.style.position = "relative";
    }
    starsDiv.style.position = "absolute";
    starsDiv.style.top = "0";
    starsDiv.style.left = "0";
    starsDiv.style.width = "100%";
    starsDiv.style.height = "100%";
    starsDiv.style.pointerEvents = "none";
    // 星星的数量
    const starCount = 43;
    // 将 starsDiv 这个元素的 HTML 内容清空
    starsDiv.innerHTML = "";
    // 生成星星
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement("div");
      star.className = "star";
      star.style.top = Math.random() * 95 + "%";
      star.style.left = Math.random() * 95 + "%";
      star.style.animationDelay = Math.random() * 5 + "s";
      starsDiv.appendChild(star);
    }
    // 改变星星闪烁的位置
    function randomizeStarPosition(star) {
      star.style.top = Math.random() * 95 + "%";
      star.style.left = Math.random() * 95 + "%";
    }
    starsDiv.querySelectorAll(".star").forEach((star) => {
      star.addEventListener("animationiteration", function () {
        randomizeStarPosition(star);
      });
    });
  }
  createStarsInContainer(document.querySelector("main"), "main-stars");
});
