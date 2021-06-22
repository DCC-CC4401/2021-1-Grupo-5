
/**
 * This scripts handles the submission of the three forms that are on profile settings:
 * - The "Change Password" Form
 * - The "Change Favorite Games" Form
 * - The "Tags Input", that is actually not a form
 */


/**
 * Gets the change password form data, validates it, and if it is valid submit the form.
 * If the data contains errors, show the errors to the user.
 */
function change_password() {
    let new_pass = document.getElementsByName('new_password1')[0].value;
    let new_pass_confirm = document.getElementsByName('new_password2')[0].value;

    let errorMessage = document.getElementById("errorMessage");
    errorMessage.innerHTML = "";
    errorMessage.style.display = "block";
    errorMessage.style.color = "red";

    switch(checkPassword(new_pass)) {
        case 0:
            errorMessage.innerHTML += "- Su contraseña contiene caracteres inválidos.<br>";
            break;
        case 1:
            errorMessage.innerHTML += "- Su contraseña no contiene letras.<br>";
            break;
        case 2:
            errorMessage.innerHTML += "- Su contraseña no contiene números.<br>";
            break;
        case 3:
            errorMessage.innerHTML += "- Su contraseña debe tener al menos 9 caracteres.<br>";
            break;
        case -1:
            if (new_pass !== new_pass_confirm) {
                console.log("Error, la nueva contraseña no coincide al confirmarla");
                errorMessage.innerHTML = errorMessage.innerHTML + "- Las contraseñas no coinciden.<br>";
                break;
            } else {
                // this form must reload the page, to update the session cookie, using ajax here would complicate things.
                console.log("cambiando contraseña");
                document.getElementById('change_password_form').submit();  // submit and reload.
            }
    }
}


/**
 * Sends the favorite games of the user using AJAX, without reloading the page.
 * @param e Event to prevent the form being inmediatly submitted.
 * @returns {boolean} False to avoid reloading the page.
 */
function update_favorite_games(e) {
    e.preventDefault()
    /*
    When the form changes, is instantly submited without reloading the page.
    The form changes when a checkbox is pressed. It's like the 'like' button on social medias.
    */
    let data = new FormData();
    data.append('lol_game', document.getElementById('lol_checkbox').checked);
    data.append('minecraft_game', document.getElementById('minecraft_checkbox').checked);
    data.append('smash_game', document.getElementById('smash_checkbox').checked);
    data.append('overwatch_game', document.getElementById('overwatch_checkbox').checked);
    data.append('valorant_game', document.getElementById('valorant_checkbox').checked);

    let xhrequest = new XMLHttpRequest();
    xhrequest.open('POST', url_fav_games);
    xhrequest.setRequestHeader('X-CSRFToken', csrfcookie());
    xhrequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhrequest.timeout = 1000;
    xhrequest.onload = function (d) {
        // alert('response:'+d.currentTarget.responseText);

        //console.log(d.currentTarget.responseText);
    }
    xhrequest.onerror = function (d) {
        alert('Oh no!!. Tus preferencias no pudieron ser actualizadas D:');
    }
    xhrequest.send(data);

    return false;
}


/**
 * Sends the user tags using AJAX without reloading the page.
 * @param e Event to prevent the form being inmediatly submitted.
 * @returns {boolean} False to avoid reloading the page.
 */
function update_personal_tags(e) {
    document.getElementById("id_tags").value = document.getElementById('the_tags').getAttribute("data-simple-tags");
    e.preventDefault();
    let data = new FormData();
    data.append('tags_data', document.getElementById('the_tags').getAttribute("data-simple-tags"));
    let xhrequest = new XMLHttpRequest();
    xhrequest.open('POST', url_tags);
    xhrequest.setRequestHeader('X-CSRFToken', csrfcookie());
    xhrequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhrequest.timeout = 1000;
    xhrequest.onload = function (d) {
        // alert('response:'+d.currentTarget.responseText);
        // document.getElementById("error-message-tags").style.display = "block";
        $('#error-message-tags')
            .fadeIn({"duration": 500})
            .delay(2500)
            .fadeOut({"duration": 1000});
    }
    xhrequest.onerror = function (d) {
        alert('Oh no! Algo salió muy mal!');
    }
    $('#error-message-tags')  // stop the animation in case of one was being executed,
        .stop({"clearQueue": true})  // and clear the animation queue,
        .fadeOut({"duration": 0});  // then finally we do an instant fadeOut
    xhrequest.send(data);

    return false;
}


/**
 * The Change Password Button calls the change_password function, to validate and send the form.
 */
let submit_change_psw_button = document.getElementById('change_password_form_btn');
submit_change_psw_button.addEventListener('click', change_password);

/**
 * The Change Favorite Games Form is submitted via AJAX, without reloading, every time the form changes.
 */
let submit_change_fv_games_form = document.getElementById('favorite_games_form');
submit_change_fv_games_form.addEventListener('change', update_favorite_games);

/**
 * The Personal Tags are send via AJAX, without reloading, when the "Actualizar" button is clicked.
 */
let tags_input = document.getElementById("tags-button");
tags_input.addEventListener('click', update_personal_tags);