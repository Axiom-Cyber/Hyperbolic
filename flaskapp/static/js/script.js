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
        }, getText(), getOff(), $('#flagRe').val());
        $('#output').html($('#output').html() + '<p class="working">Working...</p><br>');
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
        if(i.children[2].value in text && i.children[0].checked){
            text[i.children[2].value].push(i.children[3].value)
        } else if (i.children[0].checked) {
            text[i.children[2].value] = [i.children[3].value]
        }
    }
    return text
}

function getOff(){
    var off = []
    for(let i of document.querySelectorAll('#disabled>input')){
        if(!i.checked){off.push(i.name)}
    }
    return off
}

$(document).on('submit','#command',function(e) {
    if (open){
        $('#output').html($('#output').html() + 'text: ' + this.command.value + '<br>')
        socket.emit('search_text', this.command.value, getText(), getOff(), $('#flagRe').val())
        open=false
    }
    return false
})

function addExecutor(){
    document.getElementById('python').innerHTML += `
<div id='solverbox'>
    <input type='checkbox'><button onclick='remove(this)'>Remove</button>
    <input type="text" placeholder="type">
    <textarea></textarea>
</div>`
}
function remove(t){
    while (t.id!='solverbox' && t.parentElement){t=t.parentElement}
    t.remove()
}
const display_regex = /(?:\/([^\/]+))+/gm;
socket.on('send_output', (type, msg)=>{
    if(type=='text') {
        $('#output').html($('#output').html()+'- '+msg +'<br>')
    }
    else if(type == 'image') {
        $("#output").html($("#output").html()+'<img class="uploadedImage" src="' +  msg + '"><br>')
    }
    else if(type == 'end') {
        open=true
        $('#output').html($('#output').html()+'- '+msg +'<br>')
        for (var elem of document.getElementsByClassName("working")){
            elem.remove();
        }
    }
    
    else if (type == 'folder') {
        var data = "<a href='/download/folder/" + msg + "' download>" + display_regex.exec(msg)[1] + "</a>"
        $('#output').html($('#output').html()+'- '+ data +'<br>')
    }
    else if (type=='file') {
        var data = "<a href='/download/file/" + msg + "' download>" + display_regex.exec(msg)[1] + "</a>"
        $('#output').html($('#output').html()+'- '+ data +'<br>')
    }
})
  
socket.on('uploaded', ()=>{
    alert('file successfully added')
})