var err_messages = {
    "no-name": "No show name inputted",
    "no-adult": "No adult cost inputted",
    "no-child": "No child cost inputted",
}

var api_url = window.location.hostname
var canChange = false

$(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop()
    $(".custom-file-label").html(fileName)
});

$("#submitButton").click(() => {
    if ($("#show_name").val() == "") {
        console.log("test")
        $("#showMessage").removeClass("d-none")
        $("#showMessage").text(err_messages["no-name"])
        setTimeout(() => {
            $("#showMessage").addClass("d-none")
            $("#showMessage").text("")
        }, 3500)
    }
    else if ($("#cost_adult").val() == "") {
        $("#showMessage").removeClass("d-none")
        $("#showMessage").text(err_messages["no-adult"])
        setTimeout(() => {
            $("#showMessage").addClass("d-none")
            $("#showMessage").text("")
        }, 3500)
    }
    else if ($("#cost_child").val() == "") {
        $("#showMessage").removeClass("d-none")
        $("#showMessage").text(err_messages["no-child"])
        setTimeout(() => {
            $("#showMessage").addClass("d-none")
            $("#showMessage").text("")
        }, 3500)
    }
    else if ($("#cost_child").val() == "") {
        $("#showMessage").removeClass("d-none")
        $("#showMessage").text(err_messages["no-child"])
        setTimeout(() => {
            $("#showMessage").addClass("d-none")
            $("#showMessage").text("")
        }, 3500)
    }
    // Sourced from https://stackoverflow.com/a/31321760/12162910
    else if ($('#customFile').get(0).files.length === 0) {
        $("#showMessage").removeClass("d-none")
        $("#showMessage").text(err_messages["no-file"])
        setTimeout(() => {
            $("#showMessage").addClass("d-none")
            $("#showMessage").text("")
        }, 3500)
    }
    else {
        $("#form").submit()
    }
})

$("#update_show_name").change(() => {
    Promise.resolve($.ajax({
        "url": "http://" + api_url + ":1234/show/get/" + $("#update_show_name").val(),
        "headers": {
            "Authentication": getCookie("auth")
        },
        "method": "GET"
    })).then((data) => {
        if (data.error) {
            $("#update_cost_adult").prop('readonly', true)
            $("#update_cost_child").prop('readonly', true)
            $("#update_customFile").addClass("d-none")

            $("#update_showMessage").removeClass("d-none")
            $("#update_showMessage").text(data.error)
            setTimeout(() => {
                $("#update_showMessage").addClass("d-none")
                $("#update_showMessage").text("")
            }, 3500)
        }
        else {
            $("#update_cost_adult").prop('readonly', false)
            $("#update_cost_child").prop('readonly', false)
            $("#update_customFile").removeClass("d-none")

            $("#update_cost_adult").val(data.data.cost_adult)
            $("#update_cost_child").val(data.data.cost_child)
            $(".custom-file-label").html(data.data.image)
        }
    })
})

$("#updateButton").click(() => {
    if ($("#update_show_name").val() == "") {
        $("#update_showMessage").removeClass("d-none")
        $("#update_showMessage").text(err_messages["no-name"])
        setTimeout(() => {
            $("#update_showMessage").addClass("d-none")
            $("#update_showMessage").text("")
        }, 3500)
    }
    else if ($("#update_cost_adult").val() == "") {
        $("#update_showMessage").removeClass("d-none")
        $("#update_showMessage").text(err_messages["no-adult"])
        setTimeout(() => {
            $("#update_showMessage").addClass("d-none")
            $("#update_showMessage").text("")
        }, 3500)
    }
    else if ($("#update_cost_child").val() == "") {
        $("#update_showMessage").removeClass("d-none")
        $("#update_showMessage").text(err_messages["no-child"])
        setTimeout(() => {
            $("#update_showMessage").addClass("d-none")
            $("#update_showMessage").text("")
        }, 3500)
    }
    else if ($("#update_cost_child").val() == "") {
        $("#update_showMessage").removeClass("d-none")
        $("#update_showMessage").text(err_messages["no-child"])
        setTimeout(() => {
            $("#update_showMessage").addClass("d-none")
            $("#update_showMessage").text("")
        }, 3500)
    }
    else {
        $("#update_form").submit()
    }
})

function remove(name) {
    Promise.resolve($.ajax({
        "url": "http://" + api_url + `:1234/show/remove/${name}`,
        "headers": {
            "Authentication": getCookie("auth")
        },
        "method": "POST"
    })).then((data) => {
        if (data.error) {
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text(data.error)
            setTimeout(() => {
                $("#alertMessage").addClass("d-none")
                $("#alertMessage").text("")
            }, 3500)
        }
        else {
            $("#alertMessage").removeClass("alert-warning")
            $("#alertMessage").addClass("alert-success")
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text("Show removed successfully")
            setTimeout(() => {
                $("#alertMessage").removeClass("alert-success")
                $("#alertMessage").addClass("alert-warning")
                $("#alertMessage").addClass("d-none")
                window.location.reload()
            }, 3500)
        }
    })
}