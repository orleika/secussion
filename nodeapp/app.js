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

const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

wss.on('connection', (ws) => {
  ws.on('message', (order) => {
    (async (order) => {
      console.log(order)
      await sleep(1000)
      const command = order.split(' ')[0]
      console.log(order.split(' '))
      const message = order.slice(command.length + 1)
      let json = {result: false}
      switch (command) {
        case '/init':
          ws.send(`/theme ${INIT_MESSAGE}`)
          break
        case '/theme':
          try {
            const option = {method: 'post', headers, body: JSON.stringify({message})}
            const response = await fetch('http://api:5000/theme', option)
            json = await response.json()
          } catch (error) {
            console.log(error)
          }
          if (!json.result) {
            ws.send(`/error ${ERROR_MESSAGE}`)
          } else {
            const keywords = json.data.keywords
            const op = json.data.opinions.join('\n')
            ws.send(`/keywords ${keywords}`)
            ws.send(`/opinion ${THEME_MESSAGE1}\n${op}\n${THEME_MESSAGE2}`)
          }
          break
        case '/opinion':
          try {
            const keywords = message.split(':')[0]
            const opinion = message.slice(keywords.length + 1)
            const option = {method: 'post', headers, body: JSON.stringify({keywords, opinion})}
            const response = await fetch('http://api:5000/opinion', option)
            json = await response.json()
          } catch (error) {
            console.log(error)
          }
          if (!json.result) {
            ws.send(`/error ${ERROR_MESSAGE}`)
          } else {
            const posOp = json.data.posOpinions.join('\n')
            const negOp = json.data.negOpinions.join('\n')
            ws.send(`/new ${OPINION_MESSAGE1}\n${posOp}\n${OPINION_MESSAGE2}\n${negOp}\n${NEXT_MESSAGE}`)
          }
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
