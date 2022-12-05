from views import Index, About, Description, My_site, Genpassword, Step_2, StudyPrograms, CoursesList,\
                CreateCourse, CreateCategory, CategoryList

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/about/': About(),
    '/read_me/': Description(),
    '/site/': My_site(),
    '/genpass/': Genpassword(),
    '/step_2/': Step_2(),
    '/study_programs/': StudyPrograms(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList()
}
