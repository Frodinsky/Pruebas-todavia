import flet as ft
from eliminar_archivos_duplicados import find_duplicates, delete_file

def main(page: ft.Page):
    # Configuracion ventana
    page.title = "Tareas automatizadas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.colors.BACKGROUND
    page.theme_mode = ft.ThemeMode.DARK
    # Tema personalizado
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE,
            secondary=ft.colors.ORANGE,
            background=ft.colors.GREY_900,
            surface=ft.colors.GREY_800
        )
    )
    #Variables de estado siempre antes del change_view
    state = {
        "current_duplicates": [],
    }

    select_dir_text = ft.Text("No has seleccionado ninguna carpeta",
                              size=14,
                              color=ft.colors.BLUE_200,
                              )
    result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    duplicate_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )

    delete_all_button = ft.ElevatedButton(
        "Eliminar todos los elementos duplicados",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.RED_900,
        icon=ft.icons.DELETE_SWEEP,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )

    #terminan las variables de estado

    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            content_area.content = duplicate_file_view
        elif selected == 1:
            content_area.content = ft.Text("1")
        elif selected == 2:
            content_area.content = ft.Text("2")


        content_area.update()


    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:

            select_dir_text.value = f"Carpeta seleccionada: {e.path}"
            select_dir_text.update()
            scan_directory(e.path)

    def scan_directory(directory):
        duplicate_list.controls.clear()
        state["current_duplicates"] = find_duplicates(directory)

        if not state["current_duplicates"]:
            result_text.value = "No se encontraron archivos duplicados"
            result_text.color = ft.colors.GREEN_400
            delete_all_button.visible = False
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados"
            result_text.color = ft.colors.ORANGE_400
            delete_all_button.visible = True

            for dup_file, original in state["current_duplicates"]:
                dup_row = ft.Row([
                    ft.Text(f"Duplicado: {dup_file} \n Original: {original}",
                            size=15,
                            expand=True,
                            color=ft.colors.BLUE_200
                            ),
                    ft.ElevatedButton(
                        "Eliminar",
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED_900,
                        on_click=lambda e, path=dup_file: delete_duplicate(path)

                    )
                ])
                duplicate_list.controls.append(dup_row)

        # Actualiza pagina
        duplicate_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Archivo Eliminado {filepath}"
            result_text.color = ft.colors.GREEN_400
            delete_all_button.visible = True
            for control in duplicate_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicate_list.controls.remove(control)
            state["current_duplicates"] = [(dub, orig) for dub, orig in state["current_duplicates"] if dub != filepath]
            if not state["current_duplicates"]:
                delete_all_button.visible = False

        else:
            result_text.value = f"Error al eliminar: {filepath}"
            result_text.color = ft.colors.RED_400

        # Actualiza pagina
        duplicate_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_all_duplicates():
        delete_count = 0
        failed_count = 0

        for dup_file, _ in state["current_duplicates"][:]:
            if delete_file(dup_file):
                delete_count += 1
            else:
                failed_count += 1

        duplicate_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Se eliminaron exitosamene {delete_count} los archivos duplicados"
            result_text.color = ft.colors.GREEN_400
        else:
            result_text.value = f"Se eliminaron {delete_count} archivos. Fallaron {failed_count} archivos."
            result_text.color = ft.colors.RED_400

        # Actualiza pagina
        duplicate_list.update()
        result_text.update()
        delete_all_button.update()


    # Configurar el selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)

    # Vista de Archivos duplicados
    duplicate_file_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Eliminar archivos duplicados",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE_200,
                                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    "Seleccionar carpeta",
                    icon=ft.icons.FOLDER_OPEN,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE_900,
                    on_click=lambda _: folder_picker.get_directory_path()
                ),
                delete_all_button,
            ]),
            ft.Container(
                content=select_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            result_text,

            ft.Container(
                content=duplicate_list,
                border=ft.border.all(2, ft.colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.colors.GREY_800,
                expand=True,

            )
        ]),
        padding=30,
        expand=True
    )



    content_area = ft.Container(
        content=duplicate_file_view,
        expand=True,
        padding=30,
    )

    #Menu lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DELETE_FOREVER_OUTLINED,
                selected_icon=ft.icons.DELETE_FOREVER,
                label="Duplicados",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.FOLDER_COPY_OUTLINED,
                selected_icon=ft.icons.FOLDER_COPY,
                label="Organizar", ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD_CIRCLE_OUTLINE,
                selected_icon=ft.icons.ADD_CIRCLE,
                label="Proximamente"
            )
        ],
        on_change=change_view,
        bgcolor=ft.colors.GREY_900,
    )

    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1),
            content_area
        ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)