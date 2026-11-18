// 友情链接界面 分页
document.addEventListener("DOMContentLoaded", function () {
  const linksGrid = document.getElementById("links-grid");
  const pagination = document.getElementById("pagination");
  const itemsPerPage = 9;
  const linkCards = Array.from(linksGrid.getElementsByClassName("link-card"));
  const totalPages = Math.ceil(linkCards.length / itemsPerPage);
  let currentPage = 1;

  function showPage(pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    linkCards.forEach((card, index) => {
      if (index >= startIndex && index < endIndex) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });

    currentPage = pageNumber;
    document.querySelectorAll(".pagination button").forEach((btn) => {
      btn.classList.remove("active");
    });
    const activeButton = pagination.querySelector(`button:nth-child(${pageNumber})`);
    if (activeButton) {
      activeButton.classList.add("active");
    }
  }

  function createPagination() {
    pagination.innerHTML = "";
    for (let i = 1; i <= totalPages; i++) {
      const pageButton = document.createElement("button");
      pageButton.textContent = i;
      pageButton.addEventListener("click", () => {
        showPage(i);
      });
      pagination.appendChild(pageButton);
    }
    if (totalPages > 0) {
      showPage(1);
    }
  }

  // 添加键盘事件监听
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" && currentPage > 1) {
      // 左方向键，上一页
      showPage(currentPage - 1);
    } else if (event.key === "ArrowRight" && currentPage < totalPages) {
      // 右方向键，下一页
      showPage(currentPage + 1);
    }
  });

  createPagination();
});
