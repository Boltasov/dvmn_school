from datacenter.models import Schoolkid, Lesson, Chastisement, Commendation, Mark


def get_schoolkid(full_name: str):
    kid = Schoolkid.objects.get(full_name__contains=full_name)
    print(f'Ученик: {kid}')
    return kid


def fix_marks(schoolkid: Schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    print('Оценки обновлены')


def remove_chastisements(schoolkid: Schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print('Замечания удалены')


def create_commendation(schoolkid: Schoolkid, subject_name: str):
    lesson = Lesson.objects.filter(subject__title__contains=subject_name, year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter).order_by('-date').first()
    Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    print('Похвала добавлена')