from talent.models import PersonProfile, PersonSkill, Person, PersonWebsite


def create_person(person: Person, data: dict, **kwargs) -> None:
    person.first_name = data["first_name"] + " " + data["last_name"]
    person.save()
    person_profile = PersonProfile.objects.create(
        person=person,
        overview=data["bio"],
        avatar_id=data['avatar'] if data['avatar'] != -1 else None
    )
    for skill in data["skills"]:
        PersonSkill.objects.create(
            category=skill["category"],
            expertise=skill["expertise"],
            person_profile=person_profile
        )


def update_person(person: Person, data: dict, **kwargs) -> None:
    person.first_name = data["first_name"] + " " + data["last_name"]
    profile = person.profile.last()
    profile.overview = data["bio"]
    if data['avatar'] > 0:
        profile.avatar_id = data['avatar']
    skills = profile.skills
    skills.clear()
    for skill in data["skills"]:
        skills.create(**skill)
    websites = profile.websites
    websites.clear()
    for website in data["websites"]:
        websites.create(**website)
    profile.save()
    person.save()
