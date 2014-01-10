/*
    TailorDev Biblio, 2013

    author: Julien Maupetit
 */
$( document ).ready(function() {

    // Publication list filters form
    $('form#publication-list-filters > *').change(function(){
        $(this).parent('form').submit();
    });
});
