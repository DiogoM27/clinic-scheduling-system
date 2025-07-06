from datetime import datetime

class Consulta:
    def __init__(self, medico, utente, data_hora):
        self.medico = medico
        self.utente = utente
        self.data_hora = data_hora

    def __str__(self):
        return (f"{self.data_hora.strftime('%d/%m/%Y %H:%M')} - "
                f"Médico: {self.medico.nome}, "
                f"Utente: {self.utente.nome}")


class Medico:
    def __init__(self, nome, especialidade, cedula):
        self.nome = nome
        self.especialidade = especialidade
        self.cedula = cedula

    def __str__(self):
        return f"Nome: {self.nome}  Especialidade: {self.especialidade}  Cédula Profissional: {self.cedula}"


class Utente:
    def __init__(self, nome, data_nascimento, cc):
        self.nome = nome
        try:
            self.data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Data de nascimento inválida. Utilize o formato DD/MM/AAAA.")
        self.cc = cc

    def __str__(self):
        return f"Nome: {self.nome}  Data de Nascimento: {self.data_nascimento.strftime('%d/%m/%Y')}  CC: {self.cc}"


class SistemaConsultorio:
    def __init__(self):
        self.medicos = []
        self.utentes = []
        self.consultas = []

    def registar_medico(self):
        nome = input("Nome do médico: ")
        especialidade = input("Especialidade: ")
        cedula = input("Número da cédula profissional: ")

        for medico in self.medicos:
            if medico.cedula == cedula:
                print("Já existe um médico com essa cédula.")
                return

        novo_medico = Medico(nome, especialidade, cedula)
        self.medicos.append(novo_medico)
        print("Médico registado com sucesso.")

    def listar_medicos(self):
        if not self.medicos:
            print("Não existe nenhum médico registado.")
        else:
            print("\n--- Lista de Médicos ---")
            for medico in self.medicos:
                print(medico)

    def registar_utente(self):
        nome = input("Nome do utente: ")
        data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        cc = input("Número do Cartão de Cidadão: ")

        for utente in self.utentes:
            if utente.cc == cc:
                print("Já existe um utente com esse número de CC.")
                return

        try:
            novo_utente = Utente(nome, data_nascimento, cc)
            self.utentes.append(novo_utente)
            print("Utente registado com sucesso.")
        except ValueError as e:
            print(f"Erro: {e}")

    def listar_utentes(self):
        if not self.utentes:
            print("Não existe nenhum utente registado.")
        else:
            print("\n--- Lista de Utentes ---")
            for utente in self.utentes:
                print(utente)

    def marcar_consulta(self):
        if not self.medicos or not self.utentes:
            print("Deve existir pelo menos um médico e um utente registado.")
            return

        cedula = input("Cédula do médico: ")
        medico = next((m for m in self.medicos if m.cedula == cedula), None)
        if not medico:
            print("Médico não encontrado.")
            return

        cc = input("Número de CC do utente: ")
        utente = next((u for u in self.utentes if u.cc == cc), None)
        if not utente:
            print("Utente não encontrado.")
            return

        data_input = input("Data e hora da consulta (DD/MM/AAAA HH:MM): ")
        try:
            data_hora = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Formato de data e hora inválido.")
            return

        for consulta in self.consultas:
            if consulta.medico.cedula == cedula and consulta.data_hora == data_hora:
                print("Este médico já tem uma consulta marcada nesse horário.")
                return

        nova_consulta = Consulta(medico, utente, data_hora)
        self.consultas.append(nova_consulta)
        print("Consulta marcada com sucesso.")

    def listar_consultas(self):
        data_input = input("Introduza a data (DD/MM/AAAA): ")
        try:
            data = datetime.strptime(data_input, "%d/%m/%Y").date()
        except ValueError:
            print("A data introduzida não é válida.")
            return

        consultas_do_dia = [c for c in self.consultas if c.data_hora.date() == data]

        if not consultas_do_dia:
            print("Não existem consultas marcadas para essa data.")
            return

        print(f"\n--- Consultas marcadas para {data.strftime('%d/%m/%Y')} ---")
        for consulta in sorted(consultas_do_dia, key=lambda c: c.data_hora):
            print(consulta)

    def exportar_consultas_para_ficheiro(self):
        data_input = input("Introduza a data para exportar as consultas (DD/MM/AAAA): ")
        try:
            data = datetime.strptime(data_input, "%d/%m/%Y").date()
        except ValueError:
            print("A data introduzida não é válida.")
            return

        consultas_do_dia = [c for c in self.consultas if c.data_hora.date() == data]

        if not consultas_do_dia:
            print("Não existem consultas marcadas para essa data.")
            return

        nome_ficheiro = f"consultas_{data.strftime('%Y-%m-%d')}.txt"
        try:
            with open(nome_ficheiro, "w", encoding="utf-8") as f:
                f.write(f"Consultas para o dia {data.strftime('%d/%m/%Y')}:\n")
                f.write("-" * 40 + "\n")
                for consulta in sorted(consultas_do_dia, key=lambda c: c.data_hora):
                    f.write(str(consulta) + "\n")
            print(f"Consultas exportadas com sucesso para o ficheiro '{nome_ficheiro}'.")
        except Exception as e:
            print(f"Erro ao escrever o ficheiro: {e}")


def menu():
    sistema = SistemaConsultorio()  

    
    medico1 = Medico("Dra. Inês Costa", "Cardiologia", "M1234")
    medico2 = Medico("Dr. Pedro Almeida", "Dermatologia", "M5678")
    sistema.medicos.append(medico1)
    sistema.medicos.append(medico2)

    
    utente1 = Utente("Ana Silva", "12/05/1987", "123456789")
    utente2 = Utente("Rui Fonseca", "24/09/1992", "987654321")
    sistema.utentes.append(utente1)
    sistema.utentes.append(utente2)

    
    consulta1 = Consulta(medico1, utente1, datetime.strptime("30/05/2025 10:30", "%d/%m/%Y %H:%M"))
    consulta2 = Consulta(medico2, utente2, datetime.strptime("30/05/2025 14:00", "%d/%m/%Y %H:%M"))
    sistema.consultas.append(consulta1)
    sistema.consultas.append(consulta2)

    while True:
        print("\n--- Menu Principal ---")
        print("1. Registar Médico")
        print("2. Listar Médicos")
        print("3. Registar Utente")
        print("4. Listar Utentes")
        print("5. Marcar Consulta")
        print("6. Listar Consultas")
        print("7. Exportar Consultas para Ficheiro")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.registar_medico()
        elif opcao == "2":
            sistema.listar_medicos()
        elif opcao == "3":
            sistema.registar_utente()
        elif opcao == "4":
            sistema.listar_utentes()
        elif opcao == "5":
            sistema.marcar_consulta()
        elif opcao == "6":
            sistema.listar_consultas()
        elif opcao == "7":
            sistema.exportar_consultas_para_ficheiro()
        elif opcao == "0":
            print("A encerrar o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()