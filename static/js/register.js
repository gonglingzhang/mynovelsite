// 注册界面验证码
$(function () {
  function bindCaptchaBtnClick() {
    $("#captcha-btn").click(function () {
      let $this = $(this);
      let email = $("input[name='email']").val();
      if (email === "") {
        alert("请先输入邮箱地址！");
        return;
      }
      // 取消按钮的点击事件
      $this.off("click");

      // 发送ajax请求
      $.ajax({
        url: "/auth/send_email_captcha?email=" + email,
        method: "GET",
        success: function (result) {
          if (result["code"] == 200) {
            alert("验证码已发送，请注意查收！");
          } else {
            alert("验证码发送失败，请稍后再试！");
          }
        },
        fail: function (error) {
          console.log(error);
        },
      });

      // 倒计时
      let countdown = 60;
      let timer = setInterval(function () {
        if (countdown <= 0) {
          $this.text("获取验证码");
          // 清除定时器
          clearInterval(timer);
          // 重新绑定点击事件
          bindCaptchaBtnClick();
        } else {
          countdown--;
          $this.text("重新发送(" + countdown + ")");
        }
      }, 1000);
    });
  }
  bindCaptchaBtnClick();
});
