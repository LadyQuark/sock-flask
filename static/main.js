document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io('/log');

    // When connected
    socket.on('connect', () => {
        console.log("Connected!")
        
        // Each button should emit a "user event" when clicked
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                let info = {
                    'event': 'button click',
                    'data': {
                        'name': button.dataset.name,
                    },
                }
                socket.emit('user event', info);
            };
        });
    });

    // When receiving
    socket.on('confirmation', data => {
        //TODO
        console.log("Got it!")
        console.log(data)
    });
});