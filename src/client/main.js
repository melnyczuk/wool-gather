const { app, BrowserWindow } = require('electron');
const path = require('path');
const process = require('process');
const childProcess = require('child_process');

const server = childProcess.spawn('pipenv', ['run', 'server']);

function createWindow() {
  const win = new BrowserWindow({
    fullscreen: true,
    title: 'wool-gather',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(app.getAppPath(), './src/client/preload.js'),
    },
  });

  win.loadFile('./src/client/index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

process.on('exit', () => server.kill());
