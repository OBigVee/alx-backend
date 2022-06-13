import { createClient } from 'redis'
import { createQueue } from 'kue'
import { promisify } from 'util'
import express from 'express'

const app = express()
const PORT = 1245

const client = createClient()
const queue = createQueue()
let reservationEnabled = true

client.on('error', (errMessage) => {
  console.log(`Redis client not connected to the server:${errMessage.toString()}`)
})

client.on('connect', () => {
  console.log('Redis client connected to the server')
})

const reserveSeat = (number) => {
  // return promisify(client.set).bind(client)('available_seats', number);
  return client.set('available_seats', number)
}
const get = promisify(client.get).bind(client)
const getCurrentAvailableSeats = async () => {
  return await get('available_seats')
}

app.get('/available_seats', (req, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats })
    })
})

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' })
  } else {
    const job = queue.create('reserve_seat', reserveSeat())
      .save((err) => {
        if (!err) {
          return res.json({ status: 'Reservation in process' })
        } else {
          return res.json({ status: 'Reservation failed' })
        }
      })
    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`)
    }).on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err}`)
    })
  }
})

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' })
  queue.process('reserve_seat', (job, done) => {
    getCurrentAvailableSeats().then((result) => Number.parseInt(result || 0))
      .then((availableSeats) => {
        // const availableSeatsAfterSub =
        reserveSeat(availableSeats - 1)
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled
        if (availableSeats >= 0) {
          return done()
        } else {
          return res.json({ Error: 'Not enough seats available' })
        }

        // reservationEnabled = availableSeats <= 1 ? false : reservationEnabled
        // if(availableSeats >= 0){
        //     return done()
        // }else{
        //     return res.json({Error: "Not enough seats available" })
        // }
      })
    done()
  })
})
const resetAvailableSeats = async (initialSeatsCount) => {
  return promisify(client.set)
    .bind(client)('available_seats', Number.parseInt(initialSeatsCount))
}
app.listen(PORT, () => {
  resetAvailableSeats(50)
    .then(() => {
      reservationEnabled = true
      console.log(`API available on localhost port ${PORT}`)
    })
})

module.exports = app
