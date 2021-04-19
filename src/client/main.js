const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 1080,
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
