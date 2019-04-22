$(function (){
    $('button').on('click', addNew)

    async function addNew (){
        let flavor = $('#flavor').val();
        let size = $('#size').val();
        let rating = $('#rating').val();
        let image =$('#image').val();

        let response = await $.ajax({
            method: "POST",
            url: `/cupcakes`,
            contentType: "application/json",
            data: JSON.stringify({
                "flavor": flavor,
                "size": size,
                "rating": Number(rating),
                "image": image
            }),
        });

        if (response){
            $('ul').append(`<div>
                <img class="img-fluid img-thumbnail cupcake" src="${image}">
                <li>flavor: ${flavor} Size: ${size} Rated: ${rating}</li>
            </div>`)
        }
        $('form').trigger("reset")
    }

})