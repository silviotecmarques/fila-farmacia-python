import flet as ft
from src.core.fila import GerenciadorFila

def main(page: ft.Page):
    page.title = "Fila Maxi Popular"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 650
    page.window_icon = "icon/icon.ico"
    
    fila = GerenciadorFila()

    def atualizar_lista():
        lista_view.controls.clear()
        for idx, b in enumerate(fila.balconistas):
            lista_view.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Image(src=b["avatar"], width=40, height=40),
                        title=ft.Text(b["nome"], weight="bold" if idx == 0 else "normal"),
                        subtitle=ft.Text(f"Atendimentos: {b['atendimentos']}"),
                        trailing=ft.IconButton(ft.icons.DELETE_OUTLINE, on_click=lambda _, id=b["id"]: remover_click(id))
                    ),
                    bgcolor=ft.colors.GREEN_50 if idx == 0 else None,
                    border_radius=8,
                )
            )
        page.update()

    def atender_click(e):
        fila.proximo()
        atualizar_lista()

    def pular_click(e):
        fila.pular()
        atualizar_lista()

    def remover_click(id):
        fila.remover(id)
        atualizar_lista()

    lista_view = ft.ListView(expand=True, spacing=10)

    page.add(
        ft.Column([
            ft.Row([ft.Image(src="icon/icon.ico", width=60)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("FILA DE ATENDIMENTO", size=18, weight="bold"),
            ft.Row([
                ft.ElevatedButton("ATENDER", icon=ft.icons.CHECK, on_click=atender_click, bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE, expand=True),
                ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click=pular_click, tooltip="Pular"),
            ]),
            ft.Divider(),
            lista_view
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    atualizar_lista()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")