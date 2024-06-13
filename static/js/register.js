// 绑定按钮操作，整个网页都加载完毕后才会在执行的
function bindEmailcaptchaClick() {
    $("#captcha").click(function (event) {
        //$this 就是点前按钮jequery对象
        var $this = $(this);

        // 阻止默认动作
        event.preventDefault();

        var email = $("input[name='email']").val();

        $.ajax({
            url: "/auth/captcha/email?email=" + email,
            method: "GET",
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    var countdown = 60;
                    //开始倒计时之前，就取消点击事件
                    $this.off("click");
                    var timer = setInterval(function () {
                        $this.text(countdown)
                        countdown -= 1
                        if (countdown <= 0) {
                            //清掉定时器，就不倒计时了
                            clearInterval(timer)
                            $this.text("Resend Captcha");
                            // 重新绑定事件
                            bindEmailcaptchaClick();
                        }
                    }, 1000)
                    alert("邮件发送成功！")
                } else {
                    alert(result['message'])
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    });
}


$(function () {
    bindEmailcaptchaClick();
})
