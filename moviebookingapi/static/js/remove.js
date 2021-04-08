var api_url = window.location.hostname
var err_messages = {
    "no-name": "Name cannot be empty"
}
$("#removeButton").click(() => {
    if ($("#nameInput").val() == "") {
        $("#alertMessage").text(err_messages['no-name'])
        $("#alertMessage").removeClass("d-none")
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)

        return
    }

    var name = $("#nameInput").val()
    Promise.resolve($.ajax({
        "url": "http://" + api_url + ":1234/booking/remove",
        "dataType": 'json',
        "method": "POST",
        "headers": {
            "content-type": "application/json"
        },
        "data": "{\"name\": \"" + name + "\"}"
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