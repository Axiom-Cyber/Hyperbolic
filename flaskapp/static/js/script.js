$(".pageish-btn").click(function() {
    var a = $(this).data('page-link')
    var links = [];
    $('.pageish').each(function () {
        links.push(this.id);
    });
    console.log(links);
    for (var i = 0; i < links.length; i++) {
        console.log(links[i])
        if (links[i] == a) {
            $('#'+links[i]).show();
        } else {
            $('#'+links[i]).hide();
        }
    }
});