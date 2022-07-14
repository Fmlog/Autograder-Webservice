from .models import Question, File
import importlib
from inspect import getmembers, isfunction


def autograde(id):
    file = File.objects.filter(id=id).first()
    var = str(file.file)
    file_name = var.split(".")[0]

    question = file.question
    for x in range(len(question.test_case)):

        test_file = importlib.import_module(f'media.{file_name}')
        func = getattr(test_file, question.function)
        test = question.test_case[str(x+1)]
        test_results = question.test_result[str(x+1)]
        result = func(test[0], test[1])
        if result == test_results[0]:
            print(f"pass {x+1}")
        else:
            print(f"failed {x+1}")

    return "stuff"