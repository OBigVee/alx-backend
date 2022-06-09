import { createClient, print } from 'redis'

const client = createClient()
const HASH_KEY = 'HolbertonSchools'

client.on('error', (err) => {
  console.log(`Redis client not connected to the server:${err.toString()}`)
})

client.on('connect', () => {
  console.log('Redis client connected to the server')
  testRedisAdvancedOp()
})

const setHash = (hashKey, hashField, hashVal) => {
  client.hset(hashKey, hashField, hashVal, print)
}

// main function
const testRedisAdvancedOp = () => {
  const data = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2
  }

  for (const [field, val] of Object.entries(data)) {
    setHash(HASH_KEY, field, val)
  }

  client.hgetall(HASH_KEY, (err, rep) => {
    console.log(rep)
  })
}
