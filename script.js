const bouton = document.getElementById("searchBtn");

bouton.addEventListener("click", function () {

    const recherche =
        document.querySelector("input").value;

    if (recherche === "") {
        alert("Veuillez saisir une matière.");
    } else {
        alert("Recherche : " + recherche);
    }

});