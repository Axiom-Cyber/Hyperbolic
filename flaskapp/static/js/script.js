socket = io()
var open = true

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
        }, getText());
    }
});

$(document).on('submit','#adminupload',function(e) {
    open=false
    var file = document.getElementById("file").files[0];
    var fileReader = new FileReader();
    fileReader.readAsArrayBuffer(file)
    fileReader.onload = () => {
        var arrayBuffer = fileReader.result; 
        socket.emit("upload_file", { 
            name: file.name, 
            type: file.type, 
            size: file.size, 
            binary: arrayBuffer
        }, $('#desc').val());
    }
    return false
});

function getText(){
    var text = {}
    for(let i of document.querySelectorAll('#python>div')){
        if(i.children[0].value in text){
            text[i.children[0].value].push(i.children[1].value)
        } else {
            text[i.children[0].value] = [i.children[1].value]
        }
    }
    return text
}

$(document).on('submit','#command',function(e) {
    if (open){
        $('#output').html($('#output').html() + 'text: ' + this.command.value + '<br>')
        socket.emit('search_text', this.command.value, getText())
        open=false
    }
    return false
})

function addExecutor(){
    document.getElementById('python').innerHTML += '<div><input type="text" placeholder="type"><textarea></textarea></div>'
}

socket.on('send_output', (type, msg)=>{
    if(type=='text'){$('#output').html($('#output').html()+'- '+msg +'<br>')}
    else if(type == 'end'){
        open=true
        $('#output').html($('#output').html()+'- '+msg +'<br>')
    }
})