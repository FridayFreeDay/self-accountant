// Скрипт для прокрутки страницы к якорю #table_id при загрузке страницы
$(document).ready(function(){
    $('html, body').animate({ scrollTop: $("#table_id").offset().top }, 300);
     });
