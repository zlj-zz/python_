function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    // $.get("/api/logout", function (data) {
    //     if (0 == data.errno) {
    //         location.href = "/";
    //     }
    // })
    $.ajax({
        url: "api/v1.0/session",
        type: "delete",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function (resp) {
            if (resp.errno == "0") {
                location.href = "/index.html";
            }
        }
    });
}

$(document).ready(function () {
    $.get("/api/v1.0/user", function (resp) {
        // 用户未登录
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        }
        // 查询到了用户的信息
        else if ("0" == resp.errno) {
            $("#user-name").html(resp.data.name);
            $("#user-mobile").html(resp.data.mobile);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }

        }
    }, "json");
})