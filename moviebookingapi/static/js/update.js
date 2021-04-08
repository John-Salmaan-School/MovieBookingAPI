var api_url = window.location.hostname
var canChange = false
$("#nameInput").change(() => {
    Promise.resolve($.ajax({
        "url": "http://" + api_url + ":1234/view/booking/" + $("#nameInput").val(),
        "method": "GET"
    })).then((data) => {
        if (data["data"].length == 0) {
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text("Booking does not exist under that name")
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

            $("#showSelect").val(data["data"][1])
            $("#datePick").val(data["data"][2])
            $("#adultTicketInput").val(data["data"][3])
            $("#childTicketInput").val(data["data"][4])
            $("#invoiceAmount").val(data["data"][6])

            canChange = true
        }
    })
})

$("#updateButton").click(() => {
    calculate()

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
                "content-type": "application/json"
            },
            "data":
            "{\"name\": \"" + name + "\", \"show\": \"" + show + "\",\"date\": \"" + date + "\",\"adult_tickets\": \"" + adultTicket + "\",\"child_tickets\": \"" + childTicket + "\",\"discount\": \"" + discount + "\",\"cost\": \"" + cost + "\"}"
        })).then((data) => {
            $("#alertMessage").removeClass("alert-warning")
            $("#alertMessage").addClass("alert-success")
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text("Booking updated successfully")
            setTimeout(() => {
                $("#alertMessage").removeClass("alert-success")
                $("#alertMessage").addClass("alert-warning")
                $("#alertMessage").addClass("d-none")
            }, 3500)
        })
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