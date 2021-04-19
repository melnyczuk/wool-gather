const { WebSocket } = window;

const BASE_URL = 'ws://127.0.0.1:4242';
const SUBTITLE_CHANGE_RATE = 10 * 1000;
const SUBTITLES_QUERY = '#subtitles';

function sanitizeDataUrl(url) {
  return url.replace('data:', '').replace(/^.+,/, '');
}

function getSendFrame(imgCap, socket) {
  const reader = new FileReader();

  reader.onload = () => {
    console.log('sending image...');
    socket.send(sanitizeDataUrl(reader.result));
  };

  return () => {
    imgCap.takePhoto().then((blob) => {
      reader.readAsDataURL(blob);
    });
  };
}

function getMessageHandler(reconnect) {
  const update = (subtitles) => {
    const [sub, ...rest] = subtitles;
    document.querySelector(SUBTITLES_QUERY).textContent = sub;
    console.log('rest length', rest.length);
    setTimeout(
      () => (rest.length === 0 ? reconnect() : update(rest)),
      SUBTITLE_CHANGE_RATE
    );
  };

  return (data) => {
    const { text } = JSON.parse(data);
    console.log('Adding subtitles: ', text.length);
    update(text);
  };
}

function connect(imgCap) {
  console.log('connecting...');
  const socket = new WebSocket(BASE_URL);

  const sendFrame = getSendFrame(imgCap, socket);
  const handler = getMessageHandler(() => connect(imgCap));

  socket.onmessage = ({ data }) => handler(data);
  socket.onclose = () => console.log('disconnected');
  socket.onopen = () => sendFrame();
}

const pingSocket = new WebSocket(`${BASE_URL}/ping`);
pingSocket.onopen = () => pingSocket.send('ping...');
pingSocket.onclose = () => console.log('Ping socket closed');
pingSocket.onmessage = () => {
  navigator.getUserMedia(
    { video: true, audio: false },
    (stream) => {
      const [videoTrack] = stream.getVideoTracks();
      const imgCap = new ImageCapture(videoTrack);

      connect(imgCap);

      document.getElementById('webcam').srcObject = stream;
    },
    console.error
  );
};
