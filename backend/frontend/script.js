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

    const resposta = await fetch("/clips");

    clips = await resposta.json();

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

    carregarStreamers();

        await fetch("/update", {

            method: "POST"

        });

        await carregarClips();

}

async function aprovarClip() {

    if (!clipAtual) return;

    await fetch(`/clips/${clipAtual.id}/download`, {
        method: "POST"
    });

    carregarClips();

}

async function rejeitarClip() {

    if (!clipAtual) return;

    await fetch(`/clips/${clipAtual.id}/reject`, {
        method: "POST"
    });

    carregarClips();

}

async function carregarStreamers() {

    const resposta = await fetch("/streamers");

    const streamers = await resposta.json();

    console.log(streamers); 

    const lista = document.getElementById("listaStreamers");

    lista.innerHTML = "";

    streamers.forEach(s => {

        lista.innerHTML += `
            <div class="streamer">

                <span>${s.streamer}</span>

                <button onclick="removerStreamer('${s.streamer}')">
                    ✕
                </button>

            </div>
        `;

    });

}

async function removerStreamer(streamer) {

    await fetch(`/streamers/${streamer}`, {

        method: "DELETE"

    });

    carregarStreamers();

}

carregarClips();

carregarStreamers();