
function validateForm() {
    let errorMessage = document.getElementById("errorMessage");
    errorMessage.innerHTML = "Errores en formulario:<br>"
    errorMessage.style.display = "block";

    /** @type {string} */ let username = document.getElementById("id_username").value;
    if (username === "") {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Por favor indique un nombre de usuario.<br>";
    }
    if (username.length > 50) {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Nombre de usuario admite máximo 50 caracteres.<br>";
    }
    /** @type {string} */ let first_name = document.getElementById("id_first_name").value;
    if (first_name === "") {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Por favor indique su nombre.<br>";
    }
    if (first_name.length > 50) {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Nombre admite máximo 50 caracteres.<br>";
    }
    /** @type {string} */ let last_name = document.getElementById("id_last_name").value;
    if (last_name === "") {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Por favor indique su apellido.<br>";
    }
    if (last_name.length > 50) {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Apellido admite máximo 50 caracteres.<br>";
    }

    let emailRegex = /\S+@\S+\.\S+/;
    /** @type {string} */ let email = document.getElementById("id_email").value;
    if (email === "") {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Por favor ingrese su email.<br>";
    }
    if (!emailRegex.test(email) && !(email === "")) {
        errorMessage.innerHTML = errorMessage.innerHTML +
            "- Email inválido, debe ser de la forma usuario@servidor.dominio<br>";
    }

    /** @type {string} */ let password1 = document.getElementById("id_password1").value;
    /** @type {string} */ let password2 = document.getElementById("id_password2").value;
    switch(checkPassword(password1)){
        case 0:
            errorMessage.innerHTML = errorMessage.innerHTML + "- Contraseña contiene caracteres inválidos.<br>";
            break;
        case 1:
            errorMessage.innerHTML = errorMessage.innerHTML + "- Contraseña no contiene letras.<br>";
            break;
        case 2:
            errorMessage.innerHTML = errorMessage.innerHTML + "- Contraseña no contiene números.<br>";
            break;
        case 3:
            errorMessage.innerHTML = errorMessage.innerHTML + "- Contraseña debe tener al menos 9 caracteres.<br>";
            break;
        case -1:
            if(!(password1===password2)){
                errorMessage.innerHTML = errorMessage.innerHTML + "- Contraseñas no coinciden.<br>";
                break;
            }
    }

    if (errorMessage.innerHTML === "Errores en formulario:<br>") {
        errorMessage.style.display = "none";
        document.getElementById("true-submit").click();
    }
}
function setForm() {
    document.getElementById('id_username').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
    document.getElementById('id_first_name').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
    document.getElementById('id_last_name').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
    document.getElementById('id_email').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
    document.getElementById('id_password1').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
    document.getElementById('id_password2').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("fake-submit").click();
        }
    });
}

document.onload = setForm();
