window.onload = () => {
    var auth_token = getCookie("auth")

    if (auth_token) {
        window.location.replace("/")
    }
}

$("#loginButton").click(() => {
    var email = $("#emailInput").val()
    var password = $("#passwordInput").val()
    var api_url = window.location.hostname
    var error_messages = {
        "no-input": "No email and/or password entered",
        "invalid-email": "Looks like you entered an invalid email address",
        "short-password": "The password you entered is too short"
    }

    if (email == "" && password == "") {
        $("#alertMessage").removeClass("d-none")
        $("#message").text(error_messages["no-input"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
    }
    else if (!validateEmail(email)) {
        $("#alertMessage").removeClass("d-none")
        $("#message").text(error_messages["invalid-email"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
    }
    else if (String(password).length < 8) {
        $("#alertMessage").removeClass("d-none")
        $("#message").text(error_messages["short-password"])
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
    }
    else {
        Promise.resolve($.ajax({
            "url": "http://" + api_url + ":1234/auth/login",
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "data": "{\"email\": \"" + email + "\", \"password\": \"" + password + "\"}"
        })).then(function(data) {
            if (!data.error) {
                console.log(data)
                $("#alertMessage").removeClass("alert-warning")
                $("#alertMessage").addClass("alert-success")
                $("#alertMessage").removeClass("d-none")
                $("#alertMessage").text(data.data.token)
                setTimeout(() => {
                    $("#alertMessage").removeClass("alert-success")
                    $("#alertMessage").addClass("alert-warning")
                    $("#alertMessage").addClass("d-none")
                }, 1500)
                var expire = new Date(data.data.expire * 1000)
                document.cookie = `auth=${data.data.token};expires=${expire};path=/`
                setTimeout(() => {
                    window.location.replace("/")
                }, 2000)
                
            }
            else {
                $("#alertMessage").removeClass("d-none")
                $("#alertMessage").text(data.data.error)
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