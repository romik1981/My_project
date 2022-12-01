from views import Index, About, Description, My_site, Genpassword

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/about/': About(),
    '/read_me/': Description(),
    '/site/': My_site(),
    '/genpass/': Genpassword(),
}
