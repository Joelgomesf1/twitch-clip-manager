let clips = [];

let clipAtual = null;

function atualizarCards() {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, indice) => {

        if (indice === clipAtual) {

            card.classList.add("ativo");

        } else {

            card.classList.remove("ativo");

        }

    });

}

function carregarPlayer(clip) {

    clipAtual = clip;

    document.getElementById("tituloClip").textContent = clip.title;

    document.getElementById("streamerClip").textContent =
        "Streamer: " + clip.streamer;

    document.getElementById("linkClip").href = clip.url;

    document.getElementById("linkClip").textContent =
    "Assistir na Twitch";

    atualizarCards();

}





async function carregarClips() {

    const resposta = await fetch("/approved");

    clips = await resposta.json();
    
    if (clips.length > 0) {

    clipAtual = 0;

    carregarPlayer(clips[0]);

}

    if (clips.length === 0) {

    document.getElementById("tituloClip").textContent =
        "Nenhum clip pendente";

    document.getElementById("streamerClip").textContent = "";

    document.getElementById("linkClip").style.display = "none";

    document.getElementById("clips").innerHTML = "";

    return;

}

document.getElementById("linkClip").style.display = "inline";

    if (clips.length > 0) {

    clipAtual = 0;

    carregarPlayer(clips[clipAtual]);

    }
    const container = document.getElementById("clips");

    container.innerHTML = "";

    clips.forEach(clip => {

        const card = document.createElement("div");

    card.className = "card";

    card.onclick = () => {

    clipAtual = clips.indexOf(clip);

    carregarPlayer(clip);

};

    card.innerHTML = `
        <h2>${clip.title}</h2>

        <p>Streamer: ${clip.streamer}</p>

        <p>Plataforma: ${clip.platform}</p>

        <a href="${clip.url}" target="_blank">
            Assistir na Twitch
        </a>
    `;

    container.appendChild(card);

    });

}

carregarClips();

async function excluirClip() {

    if (clips.length === 0) {
        return;
    }

    const confirmar = confirm("Deseja realmente excluir este clip?");

    if (!confirmar) {
        return;
    }

    const id = clips[clipAtual].id;

    const resposta = await fetch(`/clips/${id}`, {
        method: "DELETE"
    });

    if (!resposta.ok) {

        alert("Erro ao excluir o clip.");

        return;

    }

    carregarClips();

}

document
    .getElementById("btnProximo")
    .addEventListener("click", proximoClip);

document
    .getElementById("btnExcluir")
    .addEventListener("click", excluirClip);

function proximoClip() {

    if (clips.length === 0)
        return;

    clipAtual++;

    if (clipAtual >= clips.length)
        clipAtual = 0;

    carregarPlayer(clips[clipAtual]);

}

async function adicionarStreamer() {

    const streamer = document
        .getElementById("novoStreamer")
        .value;

    if (!streamer) return;

    await fetch("/streamers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            streamer
        })
    });

    alert("Streamer adicionado!");

}

async function baixarClip() {

    if (!clipAtual) return;

    window.open(clipAtual.url, "_blank");

}

async function rejeitarClip() {

    if (!clipAtual) return;

    await fetch(`/clips/${clipAtual.id}/reject`, {
        method: "POST"
    });

    carregarClips();

}