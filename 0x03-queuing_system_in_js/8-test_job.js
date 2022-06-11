import kue from 'kue';

import createPushNotificationsJobs from '/home/obigvee/Documents/ALX Software Engineering/Back-end/alx-backend/0x03-queuing_system_in_js/8-job.js';

const queue = kue.createQueue();

const list = [
    {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
    }
];
createPushNotificationsJobs(list, queue);
