/*
 * TailorDev Biblio
 */
$( document ).ready(function() {

    // Publication list filters form
    $('form#publication-list-filters > *').change(function(){
        $(this).parent('form').submit();
    });
});
