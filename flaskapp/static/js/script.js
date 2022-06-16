socket = io()

socket.on('send_output', (msg)=>{
    console.log(msg)
})