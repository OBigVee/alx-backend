
import { createClient,print } from 'redis'
import { promisify } from 'util'

const client = createClient()

client.on('error', (err) => {
    console.log(`Redis client not connected to the server:${err.toString()}`)
})

client.on('connect', async () => {
    console.log('Redis client connected to the server')
    await test_redis_op_async()
})

const setNewSchool = (schoolName, value) => {
    client.set(schoolName, value,print)
}
// promisify object
const get = promisify(client.get).bind(client)

const displaySchoolValue = async (schoolName) => {
   console.log( await get(schoolName))
}

const test_redis_op_async = async()=> {
    await displaySchoolValue('Holberton');
    setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');
}
