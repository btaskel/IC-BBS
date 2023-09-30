$(function () {
    $('#captcha-btn').on("click", function (event) {
        event.preventDefault();
        // 获取邮箱
        var email = $("input[name='email']").val();
        console.log(email);

        zlajax.get({
            url: "/user/send_email?email=" + email
        }).done(function (result) { // 请求成功则显示发送成功
            alert("验证码发送成功！");
        }).fail(function (error) { // 请求失败
            alert(error.message);
        })
    })
})