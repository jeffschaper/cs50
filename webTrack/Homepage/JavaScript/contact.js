// Submission count
// set counter to 0
let counter = 0;

function increment(){
    // increment by 1
    counter++;
    // change the result to the counter
    document.getElementById('result').innerHTML = counter;
}

// Clear form entries to an empty string
function clear(){
    document.getElementById('firstName').value = '';
    document.getElementById('lastName').value = '';
    document.getElementById('email').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('DOB').value = '';
    document.getElementById('gender').value = document.getElementById('choose').value;
}

// Alert Congratulations
function congratulations(){
    if (validateForm() === false){
        alert('Please fill out all sections of the form.');
    }
    else{
        alert('Congratuations');
        increment();
        clear();
    }
}

// phone number validation
// this might be able to be done in html
function phoneNumberVal(){
    // regular expression
    // ^ beginning of string
    // \d matches any digit
    // {10} matches 10 times
    // $ end of string
    var phoneNum = /^\d{10}$/;
    if (document.getElementById('phone').value.match(phoneNum)){
        return true;
    }
    else{
        return false;
    }
}

// error for required fields
function validateForm(){
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var DOB = document.getElementById('DOB').value;
    var gender = document.getElementById('gender').value;

    // if any of the conditions are false, return false
    if (firstName === ''){
        return false;
    }
    else if (lastName === ''){
        return false;
    }
    else if (email === ''){
        return false;
    }
    else if (phone === '' || phoneNumberVal() === false){
        return false;
    }
    else if (DOB === ''){
        return false;
    }
    else if (gender === 'Choose'){
        return false;
    }
    else{
        return true;
    }
}