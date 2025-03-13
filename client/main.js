function get_text_witout_timer(text){
    new_text = ""
    timer = false
    for (char of text){
        if (char === "["){
            timer = true
        }
        if (!timer){
            new_text += char
        }
        else if (char === "]"){
            timer = false
        }
    };
    return new_text
}

async function get_text(id_video) {
    fetch(`http://127.0.0.1:5000/text/${id_video}`)
    .then(response => {
        if (!response.ok){
            throw new Error(response.statusText)
        }
        return response.text()
    })
    .then( text => {
        text_witout_timer = get_text_witout_timer(text)
        p = document.querySelector("#text")
        p.textContent = text_witout_timer
    })
    

}



let btn = document.querySelector("#download");
btn.addEventListener("click", () => {
    get_text("1HbF0UpHYzQ&t=2s")
    console.log("finish")
});




async function get_text23(id_video) {
    fetch(`http://127.0.0.1:5000/text/${id_video}`)
    .then(response => {
        console.log(response)
        if (!response.ok) {
            console.error("Erreur de récupération :", response.statusText);
            return;
        }
        console.log("ici")
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        let textContent = '';

        // Fonction pour lire et afficher le texte dès qu'il arrive
        while (!done) {
            reader.read().then(({ done, value }) => {
                console.log(done)
                // Le texte reçu
                const text = decoder.decode(value, { stream: true });
                textContent += text;
                
                let p = document.querySelector("#text");
                p.textContent = textContent;  // Affiche le texte au fur et à mesure
            }).catch(error => {
                console.error("Erreur lors de la récupération du texte :", error);
            });
        }
    })
    .catch(error => {
        console.error("Erreur lors de la récupération du texte :", error);
    });
}
