socket = io()
var open = true
window.onload=()=>{
    $('#command').submit(function(){
        if (open){
            $('#output').html($('#output').html()+this.command.value)
            socket.emit('start_search', 'text', this.command.value)
        }  
        return false
    })
}

socket.on('send_output', (msg)=>{
    $('#output').html($('#output').html()+'<br>- '+msg +'<br>')
})