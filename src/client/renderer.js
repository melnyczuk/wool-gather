const { WebSocket } = window;

const BASE_URL = '127.0.0.1:4242';
const SUBTITLE_CHANGE_RATE = 2 * 1000;
const SUBTITLES_QUERY = '#subtitles';

const settings = { line_len: 80 };

const streamContraints = {
  video: {
    width: { max: 3840, ideal: 3840, min: 1280 },
    height: { max: 2160, ideal: 2160, min: 720 },
    frameRate: { max: 30, ideal: 30, min: 25 },
    zoom: 100,
  },
  audio: false,
};

function getSendFrame(imageCapture, socket) {
  const reader = new FileReader();

  reader.onload = () => {
    const sanitisedDataUrl = reader.result
      .replace('data:', '')
      .replace(/^.+,/, '');
    socket.send(sanitisedDataUrl);
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
  const socket = new WebSocket(`ws://${BASE_URL}`);
  const sendFrame = getSendFrame(imgCap, socket);
  const handler = getMessageHandler(() => connect(imgCap));
  socket.onmessage = ({ data }) => handler(data);
  socket.onerror = (e) => console.error(e);
  socket.onopen = () => sendFrame();
}

function handleStream(stream) {
  const videoTrack = stream.getVideoTracks()[0];
  connect(new ImageCapture(videoTrack));
  document.getElementById('webcam').srcObject = stream;
}

function main() {
  const settingSocket = new WebSocket(`ws://${BASE_URL}/settings`);
  settingSocket.onopen = () => settingSocket.send(JSON.stringify(settings));
  settingSocket.onmessage = () => {
    navigator.mediaDevices
      .getUserMedia(streamContraints)
      .then(handleStream)
      .catch(console.error);
  };
}

function ping() {
  return fetch(`http://${BASE_URL}`)
    .then(() => main())
    .catch(() => ping());
}

ping();
