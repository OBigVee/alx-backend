import { createClient } from 'redis'

const client = createClient()

const CHANNEL = 'holberton school channel'

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.toString()}`)
})

client.on('connect', () => {
  console.log('Redis client connected to the server')
})

// const  subscriber = client.duplicate()

client.subscribe(CHANNEL)
client.on('message', (err, msg) => {
  console.log(msg)
  if (msg === 'KILL_SERVER') {
    client.unsubscribe(CHANNEL)
    client.quit()
  }
})

// client.subscribe(CHANNEL, (message)=>{
//     console.log(message)
//     if (message === 'KILL_SERVER'){
//         client.unsubscribe(CHANNEL)
//         client.quit()
//     }
// })
