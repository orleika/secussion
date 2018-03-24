;(function () {
  const ws = new WebSocket('wss://sechack.orleika.io/ws')
  const logsForm = document.getElementById('logs')
  const orderForm = document.getElementById('order')

  orderForm.value = ''
  orderForm.placeholder = '興味を持っているテーマを書き込む'

  ws.addEventListener('open', () => {
    loading(true)
    ws.send('/init')
  })

  let state = ''
  let keywords = ''
  ws.addEventListener('message', event => {
    loading(false)
    const command = event.data.split(' ')[0]
    const reply = event.data.slice(command.length + 1)
    if (command === '/keywords') {
      keywords = reply
    } else if (command === '/error') {
      appendLogs(reply)
    } else {
      appendLogs(reply)
      setPlaceholder(command)
      state = command
      logsForm.scrollTop = logsForm.scrollHeight
    }
  })

  function setPlaceholder(state) {
    switch(state) {
      case '/theme':
        orderForm.placeholder = '興味を持っているテーマを書き込む'
        break
      case '/opinion':
        orderForm.placeholder = 'あなたの考えを書き込む'
        break
      case '/new':
        orderForm.placeholder = '新たなテーマについて入力する場合は/newと入力'
        break
      default:
        orderForm.placeholder = ''
        break
    }
  }

  document.addEventListener('keypress', event => {
    const order = orderForm.value
    if (event.keyCode === 13 && order) {
      appendLogs(order, true)
      send(order)
      orderForm.value = ''
      logsForm.scrollTop = logsForm.scrollHeight
    }
  });

  function send(order) {
    if (order === '/new') {
      ws.send(order)
    } else {
      if (state === '/new') {
        state = '/opinion'
      }
      if (state === '/opinion') {
        order = `${keywords}:${order}`
      }
      ws.send(state + ' ' + order)
    }
    loading(true)
  }

  const loadingDom = document.createElement('div')
  loadingDom.classList.add('message-loading')
  let loadingStatus = false
  function loading(enable) {
    let op = loadingStatus ^ enable
    if (op && enable) {
      logsForm.appendChild(loadingDom)
    } else if (op && !enable) {
      logsForm.removeChild(loadingDom)
    }
    loadingStatus = enable
  }

  function appendLogs(message, order) {
    if (!message) {
      return
    }
    const messages = message.split('\n').filter(t => t)
    messages.forEach(m => {
      const e = document.createElement('div')
      e.classList.add('message')
      const type = m.split(' ')[0]
      if (type === '#main') {
        m = m.slice(type.length + 1)
        e.classList.add('message-main')
      }
      const t = document.createTextNode(m)
      if (order) {
        e.classList.add('message-order')
      }
      e.appendChild(t)
      logsForm.appendChild(e)
    })
  }
}())
