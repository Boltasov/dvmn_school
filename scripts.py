from datacenter.models import Schoolkid, Lesson, Chastisement, Commendation, Mark


def get_schoolkid(full_name: str):
    kids = Schoolkid.objects.filter(full_name__contains=full_name)
    if kids.count() <= 0:
        print('Не найдено учеников по запросу. Проверьте правильность указанных фамилии и имени\n'
              'Пример: Носов Иван')
        return
    if kids.count() > 1:
        print('Найдено больше одного ученика по запросу. Добавьте и фамилию, и имя, и отчество\n'
              'Пример: Носов Иван Алексеевич')
        return
    kid = kids.first()
    print(f'Выбранный ученик: {kid}')
    return kid


def fix_marks(schoolkid: Schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    print('Оценки обновлены')


def remove_chastisements(schoolkid: Schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print('Замечания удалены')


def create_commendation(schoolkid: Schoolkid, subject_name: str, text: str):
    lesson = Lesson.objects.filter(subject__title__contains=subject_name,
                                   year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter).order_by('-date').first()
    if not lesson:
        print('Уроки по этому предмету не найдены. Введите название предмета так, как оно указано на сайте.')
    else:
        Commendation.objects.create(text=text,
                                    created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
        print('Похвала добавлена')
