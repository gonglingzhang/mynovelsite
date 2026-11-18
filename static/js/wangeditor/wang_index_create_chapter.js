document.addEventListener("DOMContentLoaded", () => {
  const csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
  const { createEditor, createToolbar } = window.wangEditor;
  const editorConfig = {
    placeholder: "",
    onChange(editor) {
      const html = editor.getHtml();
      // console.log("editor content", html);
      // 也可以同步到 <textarea>
    },
    MENU_CONF: {
      // 修改 uploadImage 菜单配置
      uploadImage: {
        server: "/content/media/chapter_upload_image/",
        fieldName: "upload_image_name",
        allowedFileTypes: ["image/*"],
        // 或者使用 headers 配置携带 CSRF 令牌
        headers: {
          "X-CSRFToken": csrfmiddlewaretoken,
        },
      },
      uploadVideo: {
        server: "/content/media/chapter_upload_video/",
        fieldName: "upload_video_name",
        allowedFileTypes: ["video/*"],
        headers: {
          "X-CSRFToken": csrfmiddlewaretoken,
        },
        maxFileSize: 4000 * 1024 * 1024,
      },
      defaultFontSize: "36px",
      fontSize: {
        fontSizeList: ["12px", "14px", "16px", "18px", "20px", "22px", "24px", "28px", "32px", "36px", "40px", { name: "50px", value: "50px" }],
      },
    },
  };

  const editor = createEditor({
    selector: "#editor-container",
    html: "<p><br></p>",
    config: editorConfig,
    mode: "default", // or 'simple'
  });

  const toolbarConfig = {
    MENU_CONF: editorConfig.MENU_CONF,
  };

  console.log(editor.getAllMenuKeys());
  console.log(editor.getMenuConfig("uploadImage"));

  const toolbar = createToolbar({
    editor,
    selector: "#toolbar-container",
    config: toolbarConfig,
    mode: "default", // or 'simple'
  });

  // 打印 toolbarConfig 的值
  console.log("toolbarConfig 的值为:", toolbarConfig);
  console.log(toolbar.getConfig().toolbarKeys);

  //根据标签的id属性获取元素使用 #id
  $("#submit-btn").click(function (event) {
    //阻止按钮默认行为
    event.preventDefault();
    //根据标签的name属性获取元素使用 标签[name='name']
    let chapter_name = "第" + String($("input[name='chapter_name']").val()) + "章";
    let chapter_intro = $("input[name='chapter_intro']").val();
    let novel_volume = $("select[name='volume_id']").val();
    let chapter_content = editor.getHtml(); //获取编辑器内容
    $.ajax(novelChapterCreateUrl, {
      method: "POST",
      data: {
        chapter_name,
        chapter_intro,
        novel_volume,
        chapter_content,
      },
      headers: {
        "X-CSRFToken": csrfmiddlewaretoken,
      },
      success: function (result) {
        if (result["code"] == 200) {
          alert("保存成功！");
          // 发布成功，跳转到文章详情页
          window.location = "/content/my_novel_detail/" + String(result["novel_id"]);
        } else {
          // 发布失败，提示错误信息
          if (Array.isArray(result["message"])) {
            alert(result["message"].join("\n")); // 如果是数组，将元素用换行符连接
          } else {
            alert(result["message"]);
          }
        }
      },
      error: function (xhr, status, error) {
        console.error("AJAX 请求出错:", status, error);
        alert("请求失败，请稍后重试！");
      },
    });
  });
});
