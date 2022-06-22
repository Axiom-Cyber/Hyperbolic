socket = io()
var open = true
window.onload=()=>{
    $('#command').submit(function(){
        if (open){
            $('#output').html($('#output').html()+this.command.value)
            socket.emit('start_search', 'text', this.command.value)
            open=false
        }
        return false
    })
}

socket.on('send_output', (type, msg, end)=>{
    $('#output').html($('#output').html()+'<br>- '+msg +'<br>')
    if(end){open=true}
})