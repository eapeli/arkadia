const { contextBridge, ipcRenderer, webUtils } = require('electron')

contextBridge.exposeInMainWorld('damonDesktop', {
  getConnection: profile => ipcRenderer.invoke('damon:connection', profile),
  revalidateConnection: () => ipcRenderer.invoke('damon:connection:revalidate'),
  touchBackend: profile => ipcRenderer.invoke('damon:backend:touch', profile),
  getGatewayWsUrl: profile => ipcRenderer.invoke('damon:gateway:ws-url', profile),
  openSessionWindow: (sessionId, opts) => ipcRenderer.invoke('damon:window:openSession', sessionId, opts),
  getBootProgress: () => ipcRenderer.invoke('damon:boot-progress:get'),
  getConnectionConfig: profile => ipcRenderer.invoke('damon:connection-config:get', profile),
  saveConnectionConfig: payload => ipcRenderer.invoke('damon:connection-config:save', payload),
  applyConnectionConfig: payload => ipcRenderer.invoke('damon:connection-config:apply', payload),
  testConnectionConfig: payload => ipcRenderer.invoke('damon:connection-config:test', payload),
  probeConnectionConfig: remoteUrl => ipcRenderer.invoke('damon:connection-config:probe', remoteUrl),
  oauthLoginConnectionConfig: remoteUrl => ipcRenderer.invoke('damon:connection-config:oauth-login', remoteUrl),
  oauthLogoutConnectionConfig: remoteUrl => ipcRenderer.invoke('damon:connection-config:oauth-logout', remoteUrl),
  profile: {
    get: () => ipcRenderer.invoke('damon:profile:get'),
    set: name => ipcRenderer.invoke('damon:profile:set', name)
  },
  api: request => ipcRenderer.invoke('damon:api', request),
  notify: payload => ipcRenderer.invoke('damon:notify', payload),
  requestMicrophoneAccess: () => ipcRenderer.invoke('damon:requestMicrophoneAccess'),
  readFileDataUrl: filePath => ipcRenderer.invoke('damon:readFileDataUrl', filePath),
  readFileText: filePath => ipcRenderer.invoke('damon:readFileText', filePath),
  selectPaths: options => ipcRenderer.invoke('damon:selectPaths', options),
  writeClipboard: text => ipcRenderer.invoke('damon:writeClipboard', text),
  saveImageFromUrl: url => ipcRenderer.invoke('damon:saveImageFromUrl', url),
  saveImageBuffer: (data, ext) => ipcRenderer.invoke('damon:saveImageBuffer', { data, ext }),
  saveClipboardImage: () => ipcRenderer.invoke('damon:saveClipboardImage'),
  getPathForFile: file => {
    try {
      return webUtils.getPathForFile(file) || ''
    } catch {
      return ''
    }
  },
  normalizePreviewTarget: (target, baseDir) => ipcRenderer.invoke('damon:normalizePreviewTarget', target, baseDir),
  watchPreviewFile: url => ipcRenderer.invoke('damon:watchPreviewFile', url),
  stopPreviewFileWatch: id => ipcRenderer.invoke('damon:stopPreviewFileWatch', id),
  setTitleBarTheme: payload => ipcRenderer.send('damon:titlebar-theme', payload),
  setNativeTheme: mode => ipcRenderer.send('damon:native-theme', mode),
  setTranslucency: payload => ipcRenderer.send('damon:translucency', payload),
  setPreviewShortcutActive: active => ipcRenderer.send('damon:previewShortcutActive', Boolean(active)),
  openExternal: url => ipcRenderer.invoke('damon:openExternal', url),
  fetchLinkTitle: url => ipcRenderer.invoke('damon:fetchLinkTitle', url),
  sanitizeWorkspaceCwd: cwd => ipcRenderer.invoke('damon:workspace:sanitize', cwd),
  settings: {
    getDefaultProjectDir: () => ipcRenderer.invoke('damon:setting:defaultProjectDir:get'),
    setDefaultProjectDir: dir => ipcRenderer.invoke('damon:setting:defaultProjectDir:set', dir),
    pickDefaultProjectDir: () => ipcRenderer.invoke('damon:setting:defaultProjectDir:pick')
  },
  revealLogs: () => ipcRenderer.invoke('damon:logs:reveal'),
  getRecentLogs: () => ipcRenderer.invoke('damon:logs:recent'),
  readDir: dirPath => ipcRenderer.invoke('damon:fs:readDir', dirPath),
  gitRoot: startPath => ipcRenderer.invoke('damon:fs:gitRoot', startPath),
  worktrees: cwds => ipcRenderer.invoke('damon:fs:worktrees', cwds),
  terminal: {
    dispose: id => ipcRenderer.invoke('damon:terminal:dispose', id),
    resize: (id, size) => ipcRenderer.invoke('damon:terminal:resize', id, size),
    start: options => ipcRenderer.invoke('damon:terminal:start', options),
    write: (id, data) => ipcRenderer.invoke('damon:terminal:write', id, data),
    onData: (id, callback) => {
      const channel = `damon:terminal:${id}:data`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    },
    onExit: (id, callback) => {
      const channel = `damon:terminal:${id}:exit`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    }
  },
  onClosePreviewRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('damon:close-preview-requested', listener)
    return () => ipcRenderer.removeListener('damon:close-preview-requested', listener)
  },
  onOpenUpdatesRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('damon:open-updates', listener)
    return () => ipcRenderer.removeListener('damon:open-updates', listener)
  },
  onDeepLink: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:deep-link', listener)
    return () => ipcRenderer.removeListener('damon:deep-link', listener)
  },
  signalDeepLinkReady: () => ipcRenderer.invoke('damon:deep-link-ready'),
  onWindowStateChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:window-state-changed', listener)
    return () => ipcRenderer.removeListener('damon:window-state-changed', listener)
  },
  onFocusSession: callback => {
    const listener = (_event, sessionId) => callback(sessionId)
    ipcRenderer.on('damon:focus-session', listener)
    return () => ipcRenderer.removeListener('damon:focus-session', listener)
  },
  onNotificationAction: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:notification-action', listener)
    return () => ipcRenderer.removeListener('damon:notification-action', listener)
  },
  onPreviewFileChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:preview-file-changed', listener)
    return () => ipcRenderer.removeListener('damon:preview-file-changed', listener)
  },
  onBackendExit: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:backend-exit', listener)
    return () => ipcRenderer.removeListener('damon:backend-exit', listener)
  },
  onPowerResume: callback => {
    const listener = () => callback()
    ipcRenderer.on('damon:power-resume', listener)
    return () => ipcRenderer.removeListener('damon:power-resume', listener)
  },
  onBootProgress: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:boot-progress', listener)
    return () => ipcRenderer.removeListener('damon:boot-progress', listener)
  },
  // First-launch bootstrap progress -- emitted by the install.ps1 stage
  // runner in main.cjs (apps/desktop/electron/bootstrap-runner.cjs).
  // Renderer's install overlay subscribes to live events and queries the
  // current snapshot via getBootstrapState() to recover after a devtools
  // reload mid-bootstrap.
  getBootstrapState: () => ipcRenderer.invoke('damon:bootstrap:get'),
  resetBootstrap: () => ipcRenderer.invoke('damon:bootstrap:reset'),
  repairBootstrap: () => ipcRenderer.invoke('damon:bootstrap:repair'),
  cancelBootstrap: () => ipcRenderer.invoke('damon:bootstrap:cancel'),
  onBootstrapEvent: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('damon:bootstrap:event', listener)
    return () => ipcRenderer.removeListener('damon:bootstrap:event', listener)
  },
  getVersion: () => ipcRenderer.invoke('damon:version'),
  uninstall: {
    summary: () => ipcRenderer.invoke('damon:uninstall:summary'),
    run: mode => ipcRenderer.invoke('damon:uninstall:run', { mode })
  },
  updates: {
    check: () => ipcRenderer.invoke('damon:updates:check'),
    apply: opts => ipcRenderer.invoke('damon:updates:apply', opts),
    getBranch: () => ipcRenderer.invoke('damon:updates:branch:get'),
    setBranch: name => ipcRenderer.invoke('damon:updates:branch:set', name),
    onProgress: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('damon:updates:progress', listener)
      return () => ipcRenderer.removeListener('damon:updates:progress', listener)
    }
  },
  themes: {
    fetchMarketplace: id => ipcRenderer.invoke('damon:vscode-theme:fetch', id),
    searchMarketplace: query => ipcRenderer.invoke('damon:vscode-theme:search', query)
  }
})
