import random
import string
from locust import HttpUser, TaskSet, task, between, events


def random_str(n=8):
    return "".join(random.choices(string.ascii_lowercase, k=n))


# ─────────────────────────────────────────────
# Task Sets
# ─────────────────────────────────────────────

class AuthTasks(TaskSet):
    """Testa register e login isoladamente."""

    @task(1)
    def register(self):
        username = random_str()
        self.client.post("/auth/register", json={
            "username": username,
            "email": f"{username}@test.com",
            "password": "senha123456"
        }, name="/auth/register")

    @task(3)
    def login(self):
        self.client.post("/auth/login", json={
            "username": self.user.username,
            "password": "senha123456"
        }, name="/auth/login")


class AlunoTasks(TaskSet):
    aluno_ids = []

    @task(3)
    def listar_alunos(self):
        self.client.get("/alunos", headers=self.user.auth_header, name="GET /alunos")

    @task(2)
    def criar_aluno(self):
        nome = random_str()
        r = self.client.post("/alunos", json={
            "nome": nome,
            "email": f"{nome}@escola.com",
            "idade": random.randint(16, 60)
        }, headers=self.user.auth_header, name="POST /alunos")
        if r.status_code == 201:
            AlunoTasks.aluno_ids.append(r.json().get("id"))

    @task(2)
    def buscar_aluno(self):
        if not AlunoTasks.aluno_ids:
            return
        id_ = random.choice(AlunoTasks.aluno_ids)
        self.client.get(f"/alunos/{id_}", headers=self.user.auth_header, name="GET /alunos/{id}")

    @task(1)
    def atualizar_aluno(self):
        if not AlunoTasks.aluno_ids:
            return
        id_ = random.choice(AlunoTasks.aluno_ids)
        nome = random_str()
        self.client.put(f"/alunos/{id_}", json={
            "nome": nome,
            "email": f"{nome}@escola.com",
            "idade": random.randint(16, 60)
        }, headers=self.user.auth_header, name="PUT /alunos/{id}")

    @task(1)
    def deletar_aluno(self):
        if not AlunoTasks.aluno_ids:
            return
        id_ = AlunoTasks.aluno_ids.pop()
        self.client.delete(f"/alunos/{id_}", headers=self.user.auth_header, name="DELETE /alunos/{id}")


class CursoTasks(TaskSet):
    curso_ids = []

    @task(3)
    def listar_cursos(self):
        self.client.get("/cursos", headers=self.user.auth_header, name="GET /cursos")

    @task(2)
    def criar_curso(self):
        r = self.client.post("/cursos", json={
            "nome": f"Curso {random_str()}",
            "descricao": "Descrição gerada pelo teste de carga",
            "cargaHoraria": random.randint(20, 400)
        }, headers=self.user.auth_header, name="POST /cursos")
        if r.status_code == 201:
            CursoTasks.curso_ids.append(r.json().get("id"))

    @task(2)
    def buscar_curso(self):
        if not CursoTasks.curso_ids:
            return
        id_ = random.choice(CursoTasks.curso_ids)
        self.client.get(f"/cursos/{id_}", headers=self.user.auth_header, name="GET /cursos/{id}")

    @task(1)
    def atualizar_curso(self):
        if not CursoTasks.curso_ids:
            return
        id_ = random.choice(CursoTasks.curso_ids)
        self.client.put(f"/cursos/{id_}", json={
            "nome": f"Curso {random_str()} Atualizado",
            "descricao": "Atualizado pelo Locust",
            "cargaHoraria": random.randint(20, 400)
        }, headers=self.user.auth_header, name="PUT /cursos/{id}")

    @task(1)
    def deletar_curso(self):
        if not CursoTasks.curso_ids:
            return
        id_ = CursoTasks.curso_ids.pop()
        self.client.delete(f"/cursos/{id_}", headers=self.user.auth_header, name="DELETE /cursos/{id}")


class ProfessorTasks(TaskSet):
    professor_ids = []

    @task(3)
    def listar_professores(self):
        self.client.get("/professores", headers=self.user.auth_header, name="GET /professores")

    @task(2)
    def criar_professor(self):
        r = self.client.post("/professores", json={
            "nome": f"Prof. {random_str()}",
            "especialidade": random.choice(["Matemática", "História", "Física", "TI", "Português"])
        }, headers=self.user.auth_header, name="POST /professores")
        if r.status_code == 201:
            ProfessorTasks.professor_ids.append(r.json().get("id"))

    @task(1)
    def buscar_professor(self):
        if not ProfessorTasks.professor_ids:
            return
        id_ = random.choice(ProfessorTasks.professor_ids)
        self.client.get(f"/professores/{id_}", headers=self.user.auth_header, name="GET /professores/{id}")

    @task(1)
    def atualizar_professor(self):
        if not ProfessorTasks.professor_ids:
            return
        id_ = random.choice(ProfessorTasks.professor_ids)
        self.client.put(f"/professores/{id_}", json={
            "nome": f"Prof. {random_str()} Atualizado",
            "especialidade": "Atualizado"
        }, headers=self.user.auth_header, name="PUT /professores/{id}")

    @task(1)
    def deletar_professor(self):
        if not ProfessorTasks.professor_ids:
            return
        id_ = ProfessorTasks.professor_ids.pop()
        self.client.delete(f"/professores/{id_}", headers=self.user.auth_header, name="DELETE /professores/{id}")


# ─────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────

class EscolaUser(HttpUser):
    """
    Usuário realista: faz login no on_start e usa o token
    em todos os requests subsequentes.
    """
    wait_time = between(0.5, 2)
    host = "http://localhost:8080"

    username = None
    auth_header = {}

    tasks = {
        AlunoTasks: 4,
        CursoTasks: 3,
        ProfessorTasks: 3,
    }

    def on_start(self):
        """Registra e autentica antes de começar os testes."""
        self.username = random_str()
        password = "senha123456"

        # Tenta registrar
        r = self.client.post("/auth/register", json={
            "username": self.username,
            "email": f"{self.username}@locust.com",
            "password": password
        }, name="/auth/register [setup]")

        if r.status_code == 201:
            token = r.json().get("token")
        else:
            # Se falhou (ex: username duplicado), faz login direto
            r = self.client.post("/auth/login", json={
                "username": self.username,
                "password": password
            }, name="/auth/login [setup]")
            token = r.json().get("token") if r.status_code == 200 else None

        if token:
            self.auth_header = {"Authorization": f"Bearer {token}"}
        else:
            # Para o usuário se não conseguiu autenticar
            self.environment.runner.quit()


class AuthOnlyUser(HttpUser):
    """
    Usuário focado só em auth — simula pico de logins.
    """
    wait_time = between(0.2, 1)
    host = "http://localhost:8080"
    weight = 1  # proporção menor que EscolaUser

    username = "admin"  # usuário fixo já cadastrado

    tasks = {AuthTasks: 1}

    def on_start(self):
        # Garante que o usuário admin existe
        self.client.post("/auth/register", json={
            "username": self.username,
            "email": "admin@locust.com",
            "password": "senha123456"
        }, name="/auth/register [setup]")