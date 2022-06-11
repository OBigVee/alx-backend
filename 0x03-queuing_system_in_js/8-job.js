/**
 * Writing the job creation function
 * @param jobs
 * @param queue
 */

import { Queue,Job } from 'kue'

//const queue = createQueue()

const createPushNotificationsJobs = (jobs, queue)=>{
    if(!(jobs instanceof Array)){ throw  new Error('Job is not an array')   }
jobs.forEach(eachJob =>{
   const job = queue.create("push_notification_code_3", eachJob)

    job.on('enqueue', ()=>{
        console.log(`Notification job created: ${job.id}`)
    }).on('complete', ()=>{
        console.log(`Notification job ${job.id} completed`)
    }).on('failed', (errorMessage)=>{
        console.log(`Notification job ${job.id} failed: ${errorMessage}`)
    }).on('progress', (progress, data)=>{
        console.log(`Notification job ${job.id} ${progress}% complete`)
    })
    job.save()
})

}

export default  createPushNotificationsJobs