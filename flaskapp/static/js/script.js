socket = io()
var open = true
window.onload=()=>{
    $('#command').submit(function(){
        if (open){
            $('#output').html($('#output').html() + this.command.value + '<br>')
            socket.emit('start_search', 'text', this.command.value)
            open=false
        }
        return false
    })
}

socket.on('send_output', (type, msg)=>{
    if(type=='text'){$('#output').html($('#output').html()+'- '+msg +'<br>')}
    else if(type == 'end'){
        open=true
        $('#output').html($('#output').html()+'- '+msg +'<br>')
    }
})