from views import Index, About, Description, My_site, Genpassword, Step_2

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/about/': About(),
    '/read_me/': Description(),
    '/site/': My_site(),
    '/genpass/': Genpassword(),
    '/step_2/': Step_2(),
}
