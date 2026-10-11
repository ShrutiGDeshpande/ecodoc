function openModal(sectionType) {
    var modalId = "myModal" + sectionType.charAt(0).toUpperCase() + sectionType.slice(1);
    document.getElementById(modalId).style.display = "block";
}

function closeModal(sectionType) {
    var modalId = "myModal" + sectionType.charAt(0).toUpperCase() + sectionType.slice(1);
    document.getElementById(modalId).style.display = "none";
}

window.onclick = function(event) {
    var modals = document.getElementsByClassName("modal");
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}