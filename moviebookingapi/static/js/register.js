window.onload = () => {
    var auth_token = getCookie("auth")

    if (auth_token) {
        window.location.replace("/")
    }
}
$("#registerButton").click(function() {
    var name = $("#nameInput").val()
    var email = $("#emailInput").val()
    var confEmail = $("#emailConfirmInput").val()
    var password = $("#passwordInput").val()
    var confPassword = $("#passwordConfirmInput").val()
    var phone = $("#phoneInput").val()
    var api_url = window.location.hostname
    var error_messages = {
        "no-input": "Fields have not been filled out. Fill them out and try again.",
        "invalid-email": "Looks like you entered an invalid email address.",
        "short-password": "The password you entered is too short.",
        "email-no-match": "The emails entered do not match",
        "password-no-match": "The passwords entered do not match",
    }

    if (email == "" && password == "" && confEmail == "" && username == "") {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text(error_messages["no-input"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }
    else if (!validateEmail(email) || !validateEmail(confEmail)) {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text(error_messages["invalid-email"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }
    else if (email != confEmail) {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text(error_messages["email-no-match"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }
    else if (String(password).length < 8 || String(confPassword).length < 8) {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text(error_messages["short-password"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }
    else if (password != confPassword) {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text(error_messages["password-no-match"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }
    else {
        Promise.resolve($.ajax({
            "url": "http://" + api_url + ":1234/auth/register",
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "data": "{\"name\": \"" + name + "\", \"email\": \"" + email + "\", \"password\": \"" + password + "\", \"phone_num\": \"" + phone + "\"}"
        })).then((data) => {
            if (!data.error) {
                $("#alertMessage").removeClass("alert-warning")
                $("#alertMessage").addClass("alert-success")
                $("#alertMessage").removeClass("d-none")
                $("#alertMessage").text("You have registered successfully. Please login")
                setTimeout(() => {
                    $("#alertMessage").removeClass("alert-success")
                    $("#alertMessage").addClass("alert-warning")
                    $("#alertMessage").addClass("d-none")
                }, 2000)

                setTimeout(() => {
                    location.replace("/login")
                }, 3500)
            }
            else {
                $("#alertMessage").removeClass("d-none")
                $("#alertMessage").text(data.error)
                setTimeout(() => {
                    $("#alertMessage").addClass("d-none")
                }, 3500)
            }
        })
    }
})

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}