//Attendre le chargement complet de la page
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });

    
    // Recherche//
    const searchBtn = document.querySelector(".btn-search");

    if (searchBtn) {
        searchBtn.addEventListener("click", () => {

            const keyword = document.querySelector(".hero-search input").value;
            const filiere = document.querySelector(".hero-search select").value;

            if (keyword.trim() === "") {
                alert("Veuillez saisir une compétence ou une matière.");
                return;
            }

            alert(
                `Recherche lancée :\n\nCompétence : ${keyword}\nFilière : ${filiere}`
            );
        });
    }

    
    // Boutons contacter// 
    const contactButtons = document.querySelectorAll(".btn-match");

    contactButtons.forEach(button => {
        button.addEventListener("click", () => {
            alert("Vous devez être connecté pour contacter ce mentor.");
            window.location.href = "mentorlink_connexion.html";
        });
    });

    
    // Animation au scroll// 
    const cards = document.querySelectorAll(
        ".feature, .profile-card, .stat"
    );

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }

        });
    }, {
        threshold: 0.2
    });

    cards.forEach(card => {
        observer.observe(card);
    });


    // Navbar dynamique// 
    window.addEventListener("scroll", () => {

        const nav = document.querySelector("nav");

        if (window.scrollY > 50) {
            nav.style.boxShadow = "0 4px 15px rgba(0,0,0,0.1)";
        } else {
            nav.style.boxShadow = "none";
        }

    });

});