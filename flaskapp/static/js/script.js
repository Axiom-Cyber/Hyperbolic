socket = io()
var open = true
window.onload=()=>{
    $('#command').submit(function(){
        
    })
}

$(document).on('submit','#upload',function(e)
{
    e.preventDefault();
    var file = document.getElementById("file").files[0];
    var fileReader = new FileReader();
    fileReader.readAsArrayBuffer(file)
    fileReader.onload = () => {
        var arrayBuffer = fileReader.result; 
        $('#output').html($('#output').html() + 'file: ' + file.name + '<br>')
        socket.emit("search_file", { 
            name: file.name, 
            type: file.type, 
            size: file.size, 
            binary: arrayBuffer 
        });
    }
});
$(document).on('submit','#command',function(e) {
    if (open){
        $('#output').html($('#output').html() + 'text: ' + this.command.value + '<br>')
        socket.emit('search_text', this.command.value)
        open=false
    }
    return false
})


socket.on('send_output', (type, msg)=>{
    if(type=='text'){$('#output').html($('#output').html()+'- '+msg +'<br>')}
    else if(type == 'end'){
        open=true
        $('#output').html($('#output').html()+'- '+msg +'<br>')
    }
})