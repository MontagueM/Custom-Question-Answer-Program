import image_presenter

questions_desired = {"multiple": False, "medium": False, "long": False, "maths": False}
subject_list = {"m": "maths", "f": "furthermaths", "e": "economics", "p": "physics"}
question_list = {"mu": "multiple", "me": "medium", "lo": "long", "ma": "maths"}
# subject_text = input("Subject maths (m), further maths (f), ecomomics (e), physics (p), debug (d)? ").lower()
subject_text = input("Press enter to start all of FM1 hard content")
if subject_text == "":
    subject = "maths"
    questions_desired["maths"] = True
    image_presenter.main(subject, questions_desired, True)
    quit()
subject = subject_list.get(subject_text)

if subject is None:
    print("Subject not found.\nQuitting.")
    quit()

if subject != "maths" and subject != "furthermaths":
    question_text = input("Question types multiple choice (mu), medium (me), long (lo)? ").lower()
else:
    question_text = "ma"
question_text = question_text.split(", ")

for i in question_text:
    questions_desired[question_list.get(i)] = True

a = 0
for i in questions_desired:
    if i is False:
        a += 1
if a == 4:
    print("Question type not found. Quitting")

image_presenter.main(subject, questions_desired, False)
