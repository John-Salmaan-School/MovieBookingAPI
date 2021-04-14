var api_url = window.location.hostname
var canChange = false

var err_messages = {
    "invalid-date": "Date can't be older than today :)",
    "not-logged-in": "You are not logged in. Please log in before updating",
}

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

$("#idInput").change(() => {

    if (!getCookie('auth')) {
        $("#alertMessage").text(err_messages['not-logged-in'])
        $("#alertMessage").removeClass("d-none")
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }

    Promise.resolve($.ajax({
        "url": "http://" + api_url + ":1234/booking/get/" + $("#idInput").val(),
        "headers": {
            "Authentication": getCookie("auth")
        },
        "method": "GET"
    })).then((data) => {
        if (data.error) {
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text(data.error)
            setTimeout(() => {
                $("#alertMessage").addClass("d-none")
            }, 3500)

            $("#showSelect").prop("disabled", true)
            $("#datePick").prop("readonly", true)
            $("#adultTicketInput").prop("readonly", true)
            $("#childTicketInput").prop("readonly", true)
            $("#categoryText").addClass("d-none")
            $("#discountGroups").addClass("d-none")

            canChange = false
        }
        else {
            $("#showSelect").prop("disabled", false)
            $("#datePick").prop("readonly", false)
            $("#adultTicketInput").prop("readonly", false)
            $("#childTicketInput").prop("readonly", false)
            $("#categoryText").removeClass("d-none")
            $("#discountGroups").removeClass("d-none")

            $("#nameInput").val(data.data.name)
            $("#showSelect").val(data.data.show)
            $("#datePick").val(data.data.date)
            $("#adultTicketInput").val(data.data.adult)
            $("#childTicketInput").val(data.data.child)
            $("#invoiceAmount").val(data.data.cost)

            if (data.data.discount == "None") {
                $("#superButton").removeClass("active")
                $("#maniteeButton").removeClass("active")
                $("#concessionButton").removeClass("active")
                $("#noneButton").addClass("active")
            }
            else if (data.data.discount == "Concession Discount") {
                $("#superButton").removeClass("active")
                $("#maniteeButton").removeClass("active")
                $("#concessionButton").addClass("active")
                $("#noneButton").removeClass("active")
            }
            else if (data.data.discount == "Manitee Discount") {
                $("#superButton").removeClass("active")
                $("#maniteeButton").addClass("active")
                $("#concessionButton").removeClass("active")
                $("#noneButton").removeClass("active")
            }
            else if (data.data.discount == "Super Tuesday") {
                $("#superButton").addClass("active")
                $("#maniteeButton").removeClass("active")
                $("#concessionButton").removeClass("active")
                $("#noneButton").removeClass("active")
            }

            canChange = true
        }
    })
})

$("#updateButton").click(() => {
    if (!getCookie('auth')) {
        $("#alertMessage").text(err_messages['not-logged-in'])
        $("#alertMessage").removeClass("d-none")
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
        return
    }

    calculate()

    var id = $("#idInput").val()
    var name = $("#nameInput").val()
    var show = $("#showSelect option:selected").text()
    var date = $("#datePick").val()
    var cost = $("#invoiceAmount").val()
    var discount


    // Sequence to check which radio button is checked and what discount to append.
    if ($("#super").is(":checked")) {
        discount = "Super Tuesday"
    }
    else if ($("#manitee").is(":checked")) {
        discount = "Manitee Discount"
    }
    else if ($("#concession").is(":checked")) {
        discount = "Concession Discount"
    }
    // By default, the default discount will remain 0.0
    else {
        discount = "None"
    }

    var adultTicket = $("#adultTicketInput").val() == "" ? "0" : $("#adultTicketInput").val()
    var childTicket = $("#childTicketInput").val() == "" ? "0" : $("#childTicketInput").val()

    if (canChange) {
        Promise.resolve($.ajax({
            "url": "http://" + api_url + ":1234/booking/update",
            "method": "POST",
            "headers": {
                "content-type": "application/json",
                "Authentication": getCookie("auth")
            },
            "data":
            "{\"id\": \"" + id + "\", \"show\": \"" + show + "\",\"date\": \"" + date + "\",\"adult_tickets\": \"" + adultTicket + "\",\"child_tickets\": \"" + childTicket + "\",\"discount\": \"" + discount + "\",\"cost\": \"" + cost + "\"}"
        })).then((data) => {
            if (!data.error) {
                $("#alertMessage").removeClass("alert-warning")
                $("#alertMessage").addClass("alert-success")
                $("#alertMessage").removeClass("d-none")
                $("#alertMessage").text("Booking updated successfully")
                setTimeout(() => {
                    $("#alertMessage").removeClass("alert-success")
                    $("#alertMessage").addClass("alert-warning")
                    $("#alertMessage").addClass("d-none")
                }, 3500)
            }
            else {
                $("#alertMessage").text(data.error)
                $("#alertMessage").removeClass("d-none")
                setTimeout(() => {
                    $("#alertMessage").addClass("d-none")
                }, 3500)
                return
            }

        })
    }
    else {
        $("#alertMessage").removeClass("d-none")
        $("#alertMessage").text("Invalid Booking ID")
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 2000)
    }
})

function calculate() {
    // Defining constant variables
    var adultPrice = 12
    var childPrice = 8
    var defaultDiscount = 0.0

    /*
    Definition of adult and child ticket count. In these lines, inline boolean functions are used. So
    if the input is empty, the variable will default to having 0 as the value. Else, it will have the
    value of the number inputted
    */
    var adultTicket = ($("#adultTicketInput").val() == "" ? 0 : parseInt($("#adultTicketInput").val()))
    var childTicket = ($("#childTicketInput").val() == "" ? 0 : parseInt($("#childTicketInput").val()))

    // Sequence to check which radio button is checked and what discount to apply.
    if ($("#super").is(":checked")) {
        defaultDiscount = 0.5
    }
    else if ($("#manitee").is(":checked")) {
        defaultDiscount = 0.2
    }
    else if ($("#concession").is(":checked")) {
        defaultDiscount = 0.3
    }
    // By default, the default discount will remain 0.0
    else {
        defaultDiscount = defaultDiscount
    }

    // Here calculations are applied to finally calculate the invoice amount
    var invoiceAmount = parseFloat(((adultTicket * adultPrice) + (childTicket * childPrice)) * (1 - defaultDiscount)).toFixed(2)

    // Then the invoice amount is set into the input, which is read only
    $("#invoiceAmount").val(`$${invoiceAmount}`)
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