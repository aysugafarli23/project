// MeidaRecorder API
'use strict';

let log = console.log.bind(console),
    id = val => document.getElementById(val),
    ul = id('ul'),
    start = id('start'),
    stop = id('stop'),
    stream,
    recorder,
    counter = 1,
    chunks,
    media = {
        tag: 'audio',
        type: 'audio/mp3',
        ext: '.mp3',
        gUM: { audio: true }
    };

navigator.mediaDevices.getUserMedia(media.gUM).then(_stream => {
    stream = _stream;
    id('btns').style.display = 'inherit';
    start.removeAttribute('disabled');
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        chunks.push(e.data);
        if (recorder.state == 'inactive') makeLink();
    };
    log('got media successfully');
}).catch(log);

start.onclick = e => {
    start.disabled = true;
    stop.removeAttribute('disabled');
    chunks = [];
    recorder.start();
};

stop.onclick = e => {
    stop.disabled = true;
    recorder.stop();
    start.removeAttribute('disabled');
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makeLink() {
    let blob = new Blob(chunks, { type: media.type }),
        url = URL.createObjectURL(blob),
        li = document.createElement('li'),
        mt = document.createElement(media.tag),
        hf = document.createElement('a');

    mt.controls = true;
    mt.src = url;
    hf.href = url;
    hf.download = `${counter++}${media.ext}`;
    hf.innerHTML = `download ${hf.download}`;
    li.appendChild(mt);
    li.appendChild(hf);
    ul.appendChild(li);

    let formData = new FormData();
    formData.append('media', blob, `recording${media.ext}`);

    fetch('/modules/upload_media/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Media uploaded successfully!');
            } else {
                alert('Upload failed.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Fetching for content body text
const cards = document.querySelector(".cards");

fetch("http://127.0.0.1:8000/modules-api/contents/list/")
  .then((res) => res.json())
  .then((data) => data.map((content) => createCard(content)));

function createCard(content) {
  const cardDiv = `
  <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
    <div class="card" style="width: 100%;">
        <div class="card-body">
            // <h5 class="card-title">${content.title}</h5>
            <p class="card-text">${content.body}</p>
        </div>
    </div>
  </div>`;
  cards.innerHTML += cardDiv;
}