import { createQueue } from 'kue'

const queue = createQueue()
const objJob = {
    phoneNumber: '07012345678',
    message: "Hello world, it's Redis creating a job for you ah ah!",
}
const job = queue.create('push_notification_code',
objJob
).save((err)=>{
    if(!err) console.log(`Notification job created: ${job.id}`)
})

job.on('complete', ()=>{
    console.log('Notification job completed')
}).on('failed', (errorMessage)=>{
    console.log('Notification job failed')
})