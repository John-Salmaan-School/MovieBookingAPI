var api_url = window.location.hostname

window.onload = () => {
    Promise.resolve($.ajax({
    "url": "http://" + api_url + ":1234/profile/info",
    "headers": {
        "Authentication": getCookie("auth"),
    },
    "method": "GET"
    })).then((data) => {
        if (!data.error) {
            $("#formButtons").addClass("d-none")
            $("#userButtons").removeClass("d-none")
            $("#userInfo").text(data.data.name)
        }
        else {
            $("#formButtons").removeClass("d-none")
            $("#userButtons").addClass("d-none")
        }
    })
}

$("#logoutButton").click(() => {
    document.cookie = "auth=; expires=Thu, 01 Jan 1970 00:00:00 GMT"

    if (!getCookie("auth")) {
        $("#alertMessage").removeClass("alert-warning")
        $("#alertMessage").addClass("alert-success")
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text("You have logged out successfully")
        setTimeout(() => {
            $("#alertMessage").removeClass("alert-success")
            $("#alertMessage").addClass("alert-warning")
            $("#alertMessage").addClass("d-none")
            window.location.replace("/")
        }, 3500)
    }
})

var err_messages = {
    "no-name": "Name cannot be empty"
}
$("#removeButton").click(() => {

    var id = $("#idInput").val()
    Promise.resolve($.ajax({
        "url": "http://" + api_url + ":1234/booking/remove",
        "dataType": 'json',
        "method": "POST",
        "headers": {
            "content-type": "application/json",
            "Authentication": getCookie("auth")
        },
        "data": "{\"id\": \"" + id + "\"}"
    })).then((data) => {
        if (!data.error) {
            $("#alertMessage").removeClass("alert-warning")
            $("#alertMessage").addClass("alert-success")
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text("Booking removed successfuly")
            setTimeout(() => {
                $("#alertMessage").removeClass("alert-success")
                $("#alertMessage").addClass("alert-warning")
                $("#alertMessage").addClass("d-none")
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
})

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