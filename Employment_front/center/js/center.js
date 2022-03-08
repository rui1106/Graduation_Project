// 基本信息修改
$(".change_info").submit(function (e) {
    // 阻止默认提交操作
    e.preventDefault();
    // 清空错误信息内容
    $("#change_info_err").hide();
    // 取到用户输入的内容
    var user_name = $("input[name=username]").val();  // 用户名
    var signature = $("input[name=signature]").val();  // 个性签名
    var email = $("input[name=email]").val();  // 邮箱
    var sex = $("input[name='sex']:checked").val();
    // 判断值
    if (user_name) {
        if (user_name.length == 11) {
            if (!isNaN(user_name)) {
                $("#change_info_err").html("用户名不能为11位的纯数字！");
                $("#change_info_err").show();
                return;
            }
        }
    }
    $("#change_info_err").hide();

    // 发起注册请求
    var params = {
        "user_name": user_name,
        "signature": signature,
        "email": email,
        "sex": sex,
    };
    $.ajax({
        url: "/center/change_info",
        type: "post",
        // data: params,
        data: JSON.stringify(params),
        contentType: "application/json",
        success: function (resp) {
            if (resp.errno == "0") {
                // 刷新当前界面
                location.reload()
            } else {
                $("#change_info_err").html(resp.errmsg);
                $("#change_info_err").show();
            }
        }
    })
})

// 修改密码
$(".change_psw").submit(function (e) {
    // 阻止默认提交操作
    e.preventDefault();
    // 清空错误信息内容
    $("#change_psw_err").hide();
    // 取到用户输入的内容
    var old_psw = $(".old_psw").val();  // 原密码
    var new_psw = $(".new_psw").val();  // 新密码
    var re_new_psw = $(".re_new_psw").val();  // 确认密码

    // 判断值
    if (old_psw.length < 6) {
        $("#change_psw_err").html("原密码错误！");
        $("#change_psw_err").show();
        return;
    }
    $("#change_psw_err").hide();
    if (new_psw.length < 6) {
        $("#change_psw_err").html("新密码不能少于6位！");
        $("#change_psw_err").show();
        return;
    }
    $("#change_psw_err").hide();
    if (new_psw != re_new_psw) {
        $("#change_psw_err").html("两次密码不一致！");
        $("#change_psw_err").show();
        return;
    }
    $("#change_psw_err").hide();
    // 发起注册请求
    var params = {
        "old_psw": old_psw,
        "new_psw": new_psw,
    };
    $.ajax({
        url: "/center/change_psw",
        type: "post",
        // data: params,
        data: JSON.stringify(params),
        contentType: "application/json",
        success: function (resp) {
            if (resp.errno == "0") {
                // 刷新当前界面
                location.reload()
            } else {
                $("#change_psw_err").html(resp.errmsg);
                $("#change_psw_err").show();
            }
        }
    })
})

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//修改头像
$(function () {
    $(".change_img").submit(function (e) {
        // 阻止默认提交
        e.preventDefault()
        $("#change_img_err").hide();
        //TODO 上传头像
        $(this).ajaxSubmit({
            url: '/center/change_img',
            type: 'post',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0') {
                    // 上传头像成功
                    // 获取上传头像的完整的url地址
                    // var avatar_url = resp.avatar_url;
                    // // 设置页面上用户头像img的src属性
                    // $('.now_user_pic').attr('src', avatar_url);
                    // $('.user_login>img', parent.document).attr('src', avatar_url);
                    parent.location.reload();
                } else {
                    // 上传头像失败
                    $("#change_img_err").html(resp.errmsg);
                    $("#change_img_err").show();
                }
            }
        })
    })
})


