const sio = io('http://localhost:8000', {
    transports: ["websocket"],
    path: '/ws/socket.io'
});


sio.on('connect', () => {
  console.log('connected');
  sio.emit('sum', {numbers: [1, 2]}, (result) => {
    console.log(result);
  });
});

sio.on('connect_error', (e) => {
    console.log(e);
})

sio.on('disconnect', () => {
  console.log('disconnected');
});


sio.on('mult', (data, cb) => {
    const result = data.numbers[0] * data.numbers[1];
    cb(result);
});

sio.on('client_count', (count) => {
    console.log(' there are ' + count + ' connected clients.');
});

sio.on('room_count', (count) => {
    console.log(' there are ' + count + ' client in my room ')
});

sio.on('user_joined', (username) => {
    console.log('There are ' + username + ' has joined');
});

sio.on('user_left', (username) => {
    console.log('There are ' + username + ' has left');
})