/**
 * This script handles the tabs on profile_settings,
 * hiding and showing elements depending on what tab is currently selected
 * @type {HTMLElement}
 */

// get the three tab bodies.
let body_ajustes = document.getElementById('body_ajustes_de_cuenta');
let body_juegos = document.getElementById('body_juegos_favoritos');
let body_tags = document.getElementById('body_tags_favoritos');

// id of the current tab
let selected_id; //"tab_ajustes_de_cuenta";  // it will be initialized later

/**
 * Action of selecting ajustes tab (change password, bad naming decision, sorry)
 * @param e
*/
function tab_ajustes(e) {

    if (selected_id !== 'tab_ajustes_de_cuenta') {
        document.getElementById(selected_id).classList.replace('active_tab', 'inactive_tab');
        selected_id = 'tab_ajustes_de_cuenta';
        document.getElementById(selected_id).classList.replace('inactive_tab', 'active_tab');

        body_ajustes.classList.remove('inactive_content');
        body_juegos.classList.add('inactive_content');
        body_tags.classList.add('inactive_content');
    }
}

/**
 * Action of selecting favorite games tab.
 * @param e
 */
function tab_juegos(e) {
    if (selected_id !== 'tab_juegos_favoritos') {
        document.getElementById(selected_id).classList.replace('active_tab', 'inactive_tab');
        selected_id = 'tab_juegos_favoritos';
        document.getElementById(selected_id).classList.replace('inactive_tab', 'active_tab');

        body_ajustes.classList.add('inactive_content');
        body_juegos.classList.remove('inactive_content');
        body_tags.classList.add('inactive_content');
    }
}
function tab_tags() {
    if (selected_id !== 'tab_tags_favoritos') {
        document.getElementById(selected_id).classList.replace('active_tab', 'inactive_tab');
        selected_id = 'tab_tags_favoritos';
        document.getElementById(selected_id).classList.replace('inactive_tab', 'active_tab');

        body_ajustes.classList.add('inactive_content');
        body_juegos.classList.add('inactive_content');
        body_tags.classList.remove('inactive_content');
    }
}

// add tag button events
document.getElementById('tab_ajustes_de_cuenta').addEventListener('click', tab_ajustes);
document.getElementById('tab_juegos_favoritos').addEventListener('click', tab_juegos);
document.getElementById('tab_tags_favoritos').addEventListener('click', tab_tags);

// get the current tab
selected_id = 'tab_ajustes_de_cuenta';  // set default value, it'll change if there's a tab value on the query params.
const urlParams = new URLSearchParams(window.location.search);
// get tab value, show the right tab and hide the others
switch (urlParams.get('tab')) {
    case 'ajustes':
        selected_id = 'tab_ajustes_de_cuenta';
        body_ajustes.classList.remove('inactive_content'); break;
    case 'juegos':
        selected_id = 'tab_juegos_favoritos';
        body_juegos.classList.remove('inactive_content'); break;
    case 'tags':
        selected_id = 'tab_tags_favoritos'
        body_tags.classList.remove('inactive_content'); break;
    default:  // ajustes again
        selected_id = 'tab_ajustes_de_cuenta';
        body_ajustes.classList.remove('inactive_content');
}
document.getElementById(selected_id).classList.replace('inactive_tab', 'active_tab');