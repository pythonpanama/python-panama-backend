TEST_KEYNOTE_1 = {
    "title": "Uso de type hints en Python",
    "description": "Que son los type hints y por qué debemos usarlos",
    "speaker_id": 1,
    "meeting_id": 1,
}

TEST_KEYNOTE_2 = {
    "title": "Creando pruebas con UnitTest",
    "description": "Cómo usar UnitTest para control de calidad de la código",
    "speaker_id": 1,
    "meeting_id": 1,
}

TEST_KEYNOTE_400 = {
    "speaker_id": 1,
    "meeting_id": 1,
}

TEST_MEMBER_1 = {
    "email": "jperez@ppty.com",
    "password": "pass",
    "mobile_phone": "+50769876543",
    "first_name": "Juan",
    "last_name": "Pérez",
    "linkedin_profile": "https://linkedin.com/in/juan_perez",
    "github_profile": "https://github.com/juan_perez",
    "twitter_profile": "https://twitter.com/juan_perez",
    "profile_picture": "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
    "is_active": True,
    "role_id": 1,
}

TEST_MEMBER_2 = {
    "email": "lcohen@ppty.com",
    "password": "pass2",
    "mobile_phone": "+50768765432",
    "first_name": "Luis",
    "last_name": "Cohen",
    "linkedin_profile": "https://linkedin.com/in/luis_cohen",
    "github_profile": "https://github.com/luis_cohen",
    "twitter_profile": "https://twitter.com/luis_cohen",
    "profile_picture": "https://ppty.com/img/D6e6lKNRCbblCoH3n.png",
    "is_active": True,
    "role_id": 1,
}

TEST_MEMBER_400 = {
    "mobile_phone": "+50769876543",
    "linkedin_profile": "https://linkedin.com/in/juan_perez",
    "github_profile": "https://github.com/juan_perez",
    "twitter_profile": "https://twitter.com/juan_perez",
    "profile_picture": "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
    "is_active": True,
}

TEST_MEETING_1 = {
    "datetime": "2021-03-31 20:00:00",
    "type": "online",
    "location": "https://www.meetup.com/Python-Panama/events/276661559",
    "description": "Python Meetup Vol. 25",
    "creator_id": 1,
}

TEST_MEETING_2 = {
    "datetime": "2021-04-15 20:00:00",
    "type": "online",
    "location": "https://www.meetup.com/Python-Panama/events/276661571",
    "description": "Python Meetup Vol. 26",
    "creator_id": 1,
}

TEST_MEETING_400 = {
    "creator_id": 1,
}

TEST_PERMISSION_1 = {"permission_name": "post:keynote"}

TEST_PERMISSION_2 = {"permission_name": "post:meeting"}

TEST_PERMISSION_3 = {"permission_name": "get:member"}

TEST_PERMISSION_4 = {"permission_name": "activate:member"}

TEST_PERMISSION_5 = {"permission_name": "post:permission"}

TEST_PERMISSION_6 = {"permission_name": "post:project"}

TEST_PERMISSION_7 = {"permission_name": "get:role"}

TEST_PERMISSION_8 = {"permission_name": "post:speaker"}

TEST_PERMISSION_9 = {"permission_name": "post:token"}

TEST_PERMISSION_400 = {}

TEST_PROJECT_1 = {
    "start_date": "2021-03-16",
    "end_date": "2021-04-15",
    "title": "REST API para sitio web",
    "description": "Un API en Python/Flask para conectar el frontend a la "
    "base de datos",
    "goals": "Generar páginas de forma dinámica para miembros, reuniones y "
    "proyectos",
    "status": "in progress",
    "admin_id": 1,
}

TEST_PROJECT_2 = {
    "start_date": "2021-04-16",
    "end_date": "2021-05-15",
    "title": "Frontend para Python Panamá",
    "description": "Sitio web de Python Panamá",
    "goals": "Sitio para compartir información relevante",
    "status": "completed",
    "admin_id": 1,
}

TEST_PROJECT_400 = {
    "end_date": "2021-04-15",
    "admin_id": 1,
}

TEST_ROLE_1 = {"role_name": "admin"}

TEST_ROLE_2 = {"role_name": "member"}

TEST_ROLE_3 = {"role_name": "member-admin"}

TEST_ROLE_4 = {"role_name": "meeting-admin"}

TEST_ROLE_5 = {"role_name": "project-admin"}

TEST_ROLE_400 = {}

TEST_SPEAKER_1 = {
    "first_name": "Tomás",
    "last_name": "González",
    "email": "tgonz@python.org",
    "linkedin_profile": "https://linkedin.com/in/tomas_gonzalez",
    "github_profile": "https://github.com/tomas_gonzalez",
    "twitter_profile": "https://twitter.com/tomas_gonzalez",
    "bio": "Experto en Python y el uso de type hints",
    "profile_picture": "https://ppty.com/img/hA4oCfR&o17mqsXm.png",
}

TEST_SPEAKER_2 = {
    "first_name": "Edgar",
    "last_name": "Espino",
    "email": "eespin@python.org",
    "linkedin_profile": "https://linkedin.com/in/edgar_espino",
    "github_profile": "https://github.com/edgar_espino",
    "twitter_profile": "https://twitter.com/edgar_espino",
    "bio": "Experto en Flask",
    "profile_picture": "https://ppty.com/img/hA4oCfR&o17K3fOm.png",
}

TEST_SPEAKER_400 = {
    "linkedin_profile": "https://linkedin.com/in/javier_real",
    "github_profile": "https://github.com/javier_real",
    "twitter_profile": "https://twitter.com/javier_real",
    "profile_picture": "https://ppty.com/img/hA4oCfR&o178P2fOm.png",
}
