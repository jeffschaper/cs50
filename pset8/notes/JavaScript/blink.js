function blink(){
    let body = document.querySelector('body');
    // visibiltiy must be an internal javascript function?
    if (body.style.visibility === 'hidden'){
        body.style.visibility = 'visible';
    }
    else{
        body.style.visibility = 'hidden';
    }
}

// Blink every 500ms
window.setInterval(blink, 500);