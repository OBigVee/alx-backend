/**
 * Track progress and errors with Kue: Create the Job processor
 */

import { createQueue, Job } from 'kue'

const queue = createQueue()

const blackListedPhoneArray = [
    4153518780,
    4153518781
]

const sendNotification = (phoneNumber, message, job, done)=>{
    let pending = 2
    let total = 2
    let sendInterval = setInterval(() =>{
        if(total - pending <= total / 2){
            job.progress(total - pending, total)
        }

        if(blackListedPhoneArray.includes(phoneNumber)){
            done(new Error(`Phone number ${phoneNumber} is blacklisted`))
            clearInterval(sendInterval);
            return;
        }

        if(total === pending ){
            console.log(`Sending notification to ${phoneNumber},
            with message: ${message}`)
        }
        --pending || done()
        pending || clearInterval(sendInterval)
    }, 1000)
}

queue.process('push_notification_code_2', 2, (job, done)=>{
    sendNotification(job.phoneNumber, job.data.message, job, done)
})