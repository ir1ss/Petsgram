// 邮箱验证
function doSendMail(obj) {
    let email = $.trim($("#inputEmail").val());
    // 校验地址的正则表达式，.+代表任意字符
    if(!email.match(/.+@.+\..+/)) {
        bootbox.alert({title : "错误提示", message : "邮箱地址格式不正确."});
        $("#inputEmail").focus();
        return false;
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
            bootbox.alert({title : "错误提示", message : "邮箱地址格式不正确."});
            $("#inputEmail").focus();
            return false;
        }
        if (data == 'send-pass') {
            bootbox.alert({title : "信息提示", message : "邮箱验证码已发送成功，请查收."});
            //发送成功后邮箱输入文本被禁止
            $('#inputEmail').attr('disabled', true);
            //发送成功后发送按钮被禁止
            $(obj).attr('disabled', true);
            return true;
        }else {
            bootbox.alert({title:"错误提示", message:"邮箱验证码未发送成功."});
            return false;
        }
    })
}

// 注册
function deReg() {
    let username = $.trim($("#inputUsername").val());
    let password = $.trim($("#inputPassword").val());
    let petname = $.trim($("#inputPetName").val());
    let petbreed = $.trim($("#inputPetBreed").val());
    let city = $.trim($("#inputCity").val());
    let province = $.trim($("#inputState").val());
    let email = $.trim($("#inputEmail").val());
    let ecode = $.trim($("#ecode").val());
    if (!email.match(/.+@.+\..+/) || password.length < 5) {
        bootbox.alert({title:"错误提示", message:"注册邮箱地址不正确或者密码少于五位."});
        return false;
    }else {
        param = "username=" + username;
        param += "&password=" + password;
        param += "&ecode=" + ecode;
        param += "&petname=" + petname;
        param += "&petbreed=" + petbreed;
        param += "&city=" + city;
        param += "&province=" + province;
        param += "&email=" + email;
        $.post('/user', param, function (data) {
            if(data == "ecode-error"){
                bootbox.alert({title:"错误提示", message:"验证码无效."});
                location.reload();
                $("#inputEmailCode").val('');
                $("#inputEmailCode").focus('');
            }else if(data == "up-invalid") {
                bootbox.alert({title:"错误提示", message:"邮箱地址格式错误或密码小于五位."});
            }else if(data == "username-used") {
                bootbox.alert({title:"错误提示", message:"该用户名已被注册."});
            }else if(data == "email-used") {
                bootbox.alert({title:"错误提示", message:"邮箱已被注册."});
            }else if(data == "reg-pass") {
                bootbox.alert({title:"信息提示", message:"注册成功!(新用户+50积分)."});
                setTimeout("location.href = '/';", 1000);
            }
        })
    }
}

function doLog() {
    let username = $.trim($("#inputUsername").val());
    let password = $.trim($("#inputPassword").val());
    let vcode = $.trim($("#logincode").val());
    console.log(username);
    param = "username=" + username;
    param += "&password=" + password;
    param += "&vcode=" + vcode;
    $.post('/userLogin', param, function (data) {
        if(data == "vcode-error"){
            bootbox.alert({title:"错误提示", message:"验证码错误."});
            setTimeout("location.reload();", 1000);
            $("#logincode").val('');
            $("#logincode").focus('');
        }else if(data == "wrong-password"){
            bootbox.alert({title:"错误提示", message:"密码错误."});
        }else if(data == "login-success"){
            bootbox.alert({title:"信息提示", message:"登录成功!"});
            setTimeout("location.href = '/';", 1000);
        }else if(data == "no-such-user"){
            bootbox.alert({title:"错误提示", message:"用户名不存在."})
        }else if(data == "login-success-and-add-credit"){
            bootbox.alert({title:"信息提示", message:"每日登录+5积分."});
            setTimeout("location.href = '/';", 1000);
        }
    })
}

