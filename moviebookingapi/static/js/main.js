/*
Title: Movie Ticket Booker
Purpose: A website written to immitate the original Movie Ticket Booker which is written in Visual Basic.
Programmer: Salmaan Nagoormira 
*/

// When the website is loading, a function is called
window.onload = function() {

    // The current date is pulled and is sliced to give the format dd/mm/yyyy
    var date = getCurrentDate()
    // From https://stackoverflow.com/a/65935586/12162910
  
    // Then the date is set into the date picker input
    $("#datePick").val(date)
}

// A variable defined for error messages
var err_messages = {
    "invalid-date": "Date can't be older than today :)",
    "no-name": "No name enterd. Please enter name before saving",
}

var api_url = window.location.hostname

// From https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event

/* 
Here the .change event is listened for when the date is changed. When it does, a function is
invoked.
*/
$("#datePick").change(function() {
    var currDate = getCurrentDate()
    
    // Convert the current date and the inputted date into timestamp format for ease of comparison
    var inpDateTimestamp = new Date($("#datePick").val()).getTime()
    var currDateTimestamp = new Date(currDate).getTime()
    
    /* 
    Here there is a comparison for the input timestamp and the current date timestamp. If the 
    input timestamp is less than the current date timestamp, a error message is invoked.
    */
    if (inpDateTimestamp < currDateTimestamp) {
        $("#alertMessage").text(err_messages['invalid-date'])
        $("#alertMessage").removeClass("d-none")
        // The date is then set back to the current date
        $("#datePick").val(currDate)
        // Then a timeout is set to remove the error message
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)
    }
})

/* 
Here an invocation of the click event listener is initiated. When the calculate button is clicked
a sequence is initiated.
*/
$("#calculateButton").click(() => {
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

})

/* 
Here an invocation of the click event listener is initiated. When the clear button is clicked
a sequence is initiated.
*/
$("#clearButton").click(() => {
    $("#nameInput").val("")
    $("#showSelect").val("default")

    var date = getCurrentDate()
    // From https://stackoverflow.com/a/65935586/12162910
  
    $("#datePick").val(date)

    $("#adultTicketInput").val("")
    $("#childTicketInput").val("")

    $("#superButton").removeClass("active")
    $("#maniteeButton").removeClass("active")
    $("#concessionButton").removeClass("active")
    $("#noneButton").addClass("active")

    $("#invoiceAmount").val("")
})

/* 
Here an invocation of the click event listener is initiated. When the save button is clicked
data is saved into a csv file.
*/

$("#saveButton").click(() => {

    /* 
    Here there is a comparison if the name input is empty or not. If it is, then don't continue
    */
    if ($("#nameInput").val() == "") {
        $("#alertMessage").text(err_messages['no-name'])
        $("#alertMessage").removeClass("d-none")
        // Then a timeout is set to remove the error message
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)

        return
    }

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

    var data = "Name" + "," + $("#nameInput").val() + "," + "Show" + 
    "," + $("#showSelect option:selected").text() + "," + "Date" + 
    "," + $("#datePick").val() + "," + "Adult" + "," + adultTicket + 
    "," + "Child" + "," + childTicket + "," + "Discount" + "," 
    + discount

    var file = new Blob([data], {type: "text/plain"})
    // Here the saveAs function is being used in the external FileSaver.min.js file
    saveAs(file, "MovieBooking.csv")
})

$("#submitButton").click(() => {

    $("#calculateButton").click()
    /* 
    Here there is a comparison if the name input is empty or not. If it is, then don't continue
    */
    if ($("#nameInput").val() == "") {
        $("#alertMessage").text(err_messages['no-name'])
        $("#alertMessage").removeClass("d-none")
        // Then a timeout is set to remove the error message
        setTimeout(() => {
            $("#alertMessage").addClass("d-none")
        }, 3500)

        return
    }

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

    Promise.resolve($.ajax({
        "url": "http://" + api_url +":1234/booking/submit",
        "method": "POST",
        "headers": {
          "content-type": "application/json"
        },
        "data":
        "{\"name\": \"" + name + "\", \"show\": \"" + show + "\",\"date\": \"" + date + "\",\"adult_tickets\": \"" + adultTicket + "\",\"child_tickets\": \"" + childTicket + "\",\"discount\": \"" + discount + "\",\"cost\": \"" + cost + "\"}"
    })).then((data) => {
        if (!data.error) {
            $("#alertMessage").removeClass("alert-warning")
            $("#alertMessage").addClass("alert-success")
            $("#alertMessage").removeClass("d-none")
            $("#alertMessage").text("Booking added successfuly")
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

// Function to get current Australian date and convert it to recognised browser format:
/*
When normally doing new Date().toLocaleString("en-AU").slice(0, 10), the returned result is in the
format dd/mm/yyy. However, in order to set the value of the date picker, the date must returned in
the format yyyy-mm-dd.
*/
function getCurrentDate() {
    /* 
    First date is defined as the current Australian date, which is then sliced to return dd/mm/yyyy.
    It is then split into an array based on the "/"
    */
    var date = new Date().toLocaleString("en-AU").slice(0, 10).split("/")
    // The numeric value of the day is defined
    day = date[0]
    // As well as the year
    year = date[2]
    // Then the day and the month in the array are swapped
    date[0] = year
    date[2] = day
    /* 
    Then the array is put into a loop and joins each string in the array with a "-", which will
    return the format needed, yyyy-mm-dd
    */
    return date.join("-")
}