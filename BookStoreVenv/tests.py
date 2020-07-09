# ця функція добавляю айтемів на першу сторінку для тестів
for s in range(10):
    p = Posts(bookName="test" + str(s),
              BookImgLink="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/3d/3ded0a598c2c2ecd91c5b420761438dfad0c819d_full.jpg",
              cost="200",
              description="""Теперь шаблон немного умнее. Если функция прос
                                qмотра забывает передать значение переменной заполнитель заголовка, вмес
                                то того, чтобы показывать пустой заголовок, шаблон предоставит значение п
                                о умолчанию. Вы можете попробовать, как это услови
                                е работает, удалив аргумент title в вызове render_template() функции view (файл \app\routes.py).""",
              amount="1488",
              author="Artur Conan Varvar",
              lenght=200,
              language="japanese")
    db.session.add(p)
    db.session.commit()



