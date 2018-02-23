const express = require('express')
const http = require('http')
const WebSocket = require('ws')
const fetch = require('node-fetch')

const LISTEN_PORT = 3000
const app = express()

const server = http.createServer(app)
const wss = new WebSocket.Server({ server })

const INIT_MESSAGE = `Secussionへようこそ。
まず、セキュリティに関してあなたが興味を持っているテーマを教えてください。`

const THEME_MESSAGE1 = `提示されたテーマに関して次のような意見があります。`
const THEME_MESSAGE2 = `これらについてあなたの考えを聞かせてください。`

const OPINION_MESSAGE1 = `あなたの考えに賛成する次の意見があります。`
const OPINION_MESSAGE2 = `また、あなたの考えに反対する次の意見もあります。`

const NEXT_MESSAGE = `続けて、あなたに別の考えがある場合は聞かせてください。
もし、新しいテーマについて議論するならば/newと入力してください。`

const RENEW_MESSAGE = `では、セキュリティに関してあなたが興味を持っているテーマを教えてください。`

const ERROR_MESSAGE = `不正な入力がされました。もう一度試してください。`

const sleep = msec => new Promise(resolve => setTimeout(resolve, msec))

wss.on('connection', (ws) => {
  ws.on('message', (order) => {
    (async (order) => {
      console.log(order)
      await sleep(1000)
      const command = order.split(' ')[0]
      console.log(order.split(' '))
      const message = order.slice(command.length + 1)
      switch (command) {
        case '/init':
          ws.send(`/theme ${INIT_MESSAGE}`)
          break
        case '/theme':
          let json = {result: false}
          try {
            const response = await fetch(`http://localhost:5000/theme/${message}`)
            json = await response.json()
          } catch (error) {
            console.log(error)
          }
          if (json.result) {
            keywords = json.data.keywords
            op = json.data.op
          } else {
            ws.send(`/error ${ERROR_MESSAGE}`)
            break
          }
          ws.send(`/keywords ${keywords}`)
          ws.send(`/opinion ${THEME_MESSAGE1}\n${op}\n${THEME_MESSAGE2}`)
          break
        case '/opinion':
          keywords = message.split(':')[0]
          opinion = message.slice(keywords.length + 1)
          try {
            const response = await fetch(`http://localhost:5000/opinion/${keywords}/${opinion}`)
            const json = await response.json()
          } catch (error) {
            const json = {result: false}
          }
          if (json.result) {
            posOp = json.data.posOp
            negOp = json.data.negOp
          } else {
            ws.send(`/error ${ERROR_MESSAGE}`)
            break
          }
          posOp = ''
          negOp = ''
          ws.send(`/new ${OPINION_MESSAGE1}\n${posOp}\n${OPINION_MESSAGE2}\n${negOp}\n${NEXT_MESSAGE}`)
          break
        case '/new':
          ws.send(`/theme ${RENEW_MESSAGE}`)
          break
        default:
          ws.send(`/error ${ERROR_MESSAGE}`)
          break
      }
    })(order)
  }).on('close', () => {
    console.log('disconnected...')
  })
})

server.listen(LISTEN_PORT, () => {
  console.log('Listening on %d', server.address().port)
})

process.on('SIGINT', () => {
  process.exit(0)
})

function noop() {}

function heartbeat() {
  this.isAlive = true
}

wss.on('connection', function connection(ws) {
  ws.isAlive = true
  ws.on('pong', heartbeat)
});

const interval = setInterval(function ping() {
  wss.clients.forEach(function each(ws) {
    if (ws.isAlive === false) return ws.terminate()

    ws.isAlive = false
    ws.ping(noop)
  })
}, 30000)
