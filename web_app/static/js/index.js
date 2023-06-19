document.addEventListener('DOMContentLoaded', function(){
    text_box.addEventListener('input', function(){
        var temp_list = new Array();
        for(i=0; i < list.length;i++)
            temp_list[i] = list[i]
        var text = this.value.toLowerCase();
        var text_list = text.split(' ');
        display.innerHTML = '';
        text_list.forEach(text => {
            if (text != ''){
                for(i=0; i < temp_list.length; i++){
                    var movie = temp_list[i].toLowerCase();
                    if(!(movie.includes(text))){
                        var index = temp_list.indexOf(temp_list[i]);
                        if(index > -1){
                            temp_list.splice(index, 1);
                            i = -1;
                        }
                    }
                }
            }
        })
        if(text_list[0] != ''){
            var count = 0;
            for(i=0; i < temp_list.length;i++){
                const p = document.createElement('p');
                p.setAttribute('class', 'recs');
                p.innerHTML = temp_list[i];
                display.append(p);
                count++;
                if(count == 5)
                    break;
            }
        }
    add_events();
    })

    function add_events(){
        const p_tags = document.querySelectorAll('p.recs');
        p_tags.forEach(e => {
            e.addEventListener('click', function(){
                text_box.value = e.innerHTML;
            })
        })
    }

    text_box.addEventListener('keydown', (e) => {
        if(e.keyCode == 13)
            e.preventDefault();
    })
})