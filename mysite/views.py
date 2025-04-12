from django.core.cache import cache
from . import words_work
from django.shortcuts import render

def index(request):
    word_count = words_work.get_word_count()
    context = {"word_count": word_count}
    return render(request, "index.html", context)


def word_list(request):
    words = words_work.get_word_for_table()
    return render(request, "word_list.html", context={"words": words})

def add_word(request):
    return render(request, "word_add.html")


def send_word(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_email = request.POST.get("email")
        user_phone = request.POST.get("phone", "-")
        new_word = request.POST.get("new_word", "")
        new_pinyin = request.POST.get ("new_pinyin", "")
        new_translation = request.POST.get("new_translation", "")
        context = {"user": user_name}
        if len(new_translation) == 0:
            context["success"] = False
            context["comment"] = "Поле \"Перевод\" должно быть не пустым"
        elif len(new_word) == 0:
            context["success"] = False
            context["comment"] = "Поле \"Слово (иероглифами)\" должно быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваше слово принято и добавлено в словарь."
            user_id = words_work.add_user(user_name, user_email, user_phone)
            words_work.write_word(new_word, new_translation, user_id, new_pinyin)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "word_request.html", context)
    else:
        add_word(request)

def words_trainer(request):
    train_words = words_work.train_word()
    return render(request, "word_trainer.html", context={"train_words": train_words})

trainings_all = 0
trainings_success = 0
trainings_fails = 0
def check_word(request):
    if request.method == "POST":
        cache.clear()
        user_index= request.POST.get("user_index")
        true_index = request.POST.get("true_index")
        train_character= request.POST.get("train_character")
        train_translation = request.POST.get("train_translation")
        context = {"true_index)": true_index, "train_character": train_character,"train_translation": train_translation}
        if user_index not in ["1",'2','3']:
            context["success"] = False
            context["comment"] = "Введено неверное значение. Ваш ответ должен быть числом (1, 2 или 3)."
            words_work.add_training(0)
        elif user_index != true_index:
            context["success"] = False
            context["comment"] = "Ваш ответ неверен. Повторите слова еще раз!"
            context["answer_character"] = train_character
            context["answer_translation"] = train_translation
            words_work.add_training(0)
        else:
            context["success"] = True
            context["comment"] = "Все верно! Продолжайте в том же духе!"
            words_work.add_training(1)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "train_request.html", context)
    else:
        add_word(request)

def show_stats(request):
    stats = words_work.get_words_stats()
    return render(request, "stats.html", stats)
