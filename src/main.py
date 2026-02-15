import flet as ft
from core.fila import GerenciadorFila

def main(page: ft.Page):
    page.title = "Gestão de Fila - Maxi Popular"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    fila = GerenciadorFila()

    def atualizar_interface():
        lista_view.controls.clear()
        for b in fila.balconistas:
            lista_view.controls.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(foreground_image_url=b["avatar"]),
                    title=ft.Text(b["nome"]),
                    subtitle=ft.Text(f"Atendimentos: {b['atendimentos']}"),
                    trailing=ft.IconButton(ft.icons.DELETE, on_click=lambda _, id=b["id"]: remover_click(id))
                )
            )
        page.update()

    def atender_click(e):
        fila.proximo()
        atualizar_interface()

    def remover_click(id):
        fila.remover(id)
        atualizar_interface()

    # UI Components
    btn_proximo = ft.ElevatedButton(
        "PRÓXIMO ATENDIMENTO", 
        icon=ft.icons.PLAY_ARROW, 
        on_click=atender_click,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN_700)
    )
    
    lista_view = ft.ListView(expand=True, spacing=10)

    # Layout inicial
    page.add(
        ft.Row([ft.Image(src="logo/logo.png", width=100)]), # Usando sua pasta logo/
        ft.Text("Fila de Atendimento", size=24, weight="bold"),
        btn_proximo,
        ft.Divider(),
        lista_view
    )

    atualizar_interface()

if __name__ == "__main__":
    ft.app(target=main)