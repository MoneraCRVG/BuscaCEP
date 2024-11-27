import flet as ft
import requests
def main(page: ft.Page):
    page.title = "Busca CEP"

    cep_field = ft.TextField(label="CEP", on_change=lambda e: submit_cep(e))
    cep_submit_button = ft.ElevatedButton(text="Buscar", on_click=lambda e: fetch(e))
    cep = ft.Text()
    endereco = ft.Text()
    bairro = ft.Text()
    cidade = ft.Text()
    ddd = ft.Text()
    def format_cep(cep):
        cep = ''.join(filter(str.isdigit, cep))
        if len(cep) <= 5:
            return cep[:5]
        elif len(cep) <= 8:
            return cep[:5] + '-' + cep[5:8]
        else:
            return cep[:5] + '-' + cep[5:8]

    def submit_cep(e):
        cep_field.error_text = ""

        cep = e.control.value

        cep = format_cep(cep)

        e.control.value = cep

        page.update()

    def fetch(e):
        cep = cep_field.value.replace('-', '')

        if len(cep) == 8:
            r = requests.get(f"https://cep.awesomeapi.com.br/json/{cep_field.value.replace('-', '')}")

            if r.status_code == 200:
                r = r.json()
                endereco.value = r["address"]
                bairro.value = r["district"]
                cidade.value = f'''{r["city"]} - {r["state"]}'''
                ddd.value = f'''DDD {r["ddd"]}'''
                page.update()
            elif r.status_code == 404:
                cep_field.error_text = "CEP não encontrado"
                page.update()

        else:
            cep_field.error_text = "Formato inválido"


    page.add(cep_field, cep_submit_button, cep, endereco, bairro, cidade, ddd)

ft.app(main)
