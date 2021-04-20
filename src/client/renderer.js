const { WebSocket } = window;

const BASE_URL = 'ws://127.0.0.1:4242';
const SUBTITLE_CHANGE_RATE = 10 * 1000;
const SUBTITLES_QUERY = '#subtitles';

const streamContraints = {
  video: {
    width: { max: 3840, ideal: 3840, min: 1920 },
    height: { max: 2160, ideal: 2160, min: 1080 },
    frameRate: { max: 30, ideal: 30, min: 25 },
    zoom: 100,
  },
  audio: false,
};

function sanitizeDataUrl(url) {
  return url.replace('data:', '').replace(/^.+,/, '');
}

function getSendFrame(imageCapture, socket) {
  const reader = new FileReader();

  reader.onload = () => {
    socket.send(sanitizeDataUrl(reader.result));
  };

  return () =>
    imageCapture
      .takePhoto()
      .then((blob) => {
        reader.readAsDataURL(blob);
      })
      .catch(console.error);
}

function setSubtitleContent(subtitle) {
  document.querySelector(SUBTITLES_QUERY).textContent = subtitle;
}

function getMessageHandler(reconnect) {
  const update = (subtitles) => {
    const [sub, ...rest] = subtitles;
    setSubtitleContent(sub);
    setTimeout(
      () => (rest.length > 0 ? update(rest) : reconnect()),
      SUBTITLE_CHANGE_RATE
    );
  };

  return (data) => {
    const { text } = JSON.parse(data);
    update([...text, '']);
  };
}

function connect(imgCap) {
  console.log('connecting...');
  const socket = new WebSocket(BASE_URL);

  const sendFrame = getSendFrame(imgCap, socket);
  const handler = getMessageHandler(() => connect(imgCap));

  socket.onmessage = ({ data }) => handler(data);
  socket.onclose = () => console.log('disconnected');
  socket.onerror = (e) => console.error(e);
  socket.onopen = () => sendFrame();
}

function handleStream(stream) {
  const videoTrack = stream.getVideoTracks()[0];
  connect(new ImageCapture(videoTrack));
  document.getElementById('webcam').srcObject = stream;
}

const lenSocket = new WebSocket(`${BASE_URL}/len`);
lenSocket.onopen = () => lenSocket.send(80);

const pingSocket = new WebSocket(`${BASE_URL}/ping`);
pingSocket.onopen = () => pingSocket.send('ping...');
pingSocket.onclose = () => console.log('');
pingSocket.onmessage = () => {
  navigator.mediaDevices
    .getUserMedia(streamContraints)
    .then(handleStream)
    .catch(console.error);
};
