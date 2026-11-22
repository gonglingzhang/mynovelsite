// 图片验证码刷新（点击图片即可刷新）
$(function () {
  function bindCaptchaClick() {
    $("#captcha-img").click(function () {
      // 加时间戳防止浏览器缓存
      $(this).attr('src', '/auth/image_captcha?t=' + Date.now());
    });
  }
  bindCaptchaClick();
});