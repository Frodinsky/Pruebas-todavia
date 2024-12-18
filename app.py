import flet as ft
import os
from eliminar_archivos_duplicados import find_duplicates, delete_file
from agrupar_archivos import organize_folder
from  remover_fondo import process_images



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
        "current_view": "duplicates"
    }
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

    #Inicio de las variables de eliminar archivos duplicados
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
    #Termina las variables de eliminar archivos duplicados

    organize_dir_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.colors.BLUE_200,
    )

    organize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)



    removebg_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    image_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )
    remove_all_button = ft.ElevatedButton(
        "Eliminar Fondo de todas las imagenes",
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
            state["current_view"] = "duplicates"
            content_area.content = duplicate_file_view
        elif selected == 1:
            state["current_view"] = "organize"
            content_area.content = organize_files_views
        elif selected == 2:
            state["current_view"] = "removebg"
            content_area.content = backgroundremove_file_view
        elif selected == 3:
            state["current_view"] = "pronto"
            content_area.content = ft.Text("5")
        content_area.update()


    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            if state["current_view"] == "duplicates":
                select_dir_text.value = f"Carpeta seleccionada: {e.path}"
                select_dir_text.update()
                scan_directory(e.path)
            elif state["current_view"] == "organize":
                organize_dir_text.value = f"Carpeta seleccionada: {e.path}"
                organize_dir_text.update()
                organize_directory(e.path)
            elif state["current_view"] == "removebg":
                removebg_result_text.value = f"Carpeta seleccionada: {e.path}"
                removebg_result_text.update()
                remove_directory(e.path)

#Se implementa funcion para ver todas las imagenes en la vista
    def remove_directory(directory):
        try:
            # Limpiar la lista de imágenes previas
            image_list.controls.clear()

            # Buscar imágenes en el directorio
            image_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    img_path = os.path.join(root, file)

                    # Verificar si la ruta corresponde a un archivo y si es una imagen
                    if os.path.isfile(img_path) and any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                        image_files.append(img_path)

            # Si no se encuentran imágenes
            if not image_files:
                removebg_result_text.value = "No se encontraron imágenes en el directorio."
                removebg_result_text.color = ft.colors.RED_400
                removebg_result_text.update()
                return

            # Si se encuentran imágenes, mostrar la lista en la interfaz
            removebg_result_text.value = f"Se encontraron {len(image_files)} imágenes."
            removebg_result_text.color = ft.colors.ORANGE_400
            removebg_result_text.update()

            for img_path in image_files:
                # Mostrar depuración de las rutas de imagen que estamos procesando
                print(f"Procesando archivo: {img_path}")

                # Crear una fila para cada imagen con su nombre y un botón para eliminar el fondo
                img_row = ft.Row([
                    ft.Text(f"Imagen: {img_path}",
                            size=15,
                            expand=True,
                            color=ft.colors.BLUE_200
                            ),
                    ft.ElevatedButton(
                        "Eliminar Fondo",
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED_900,
                        on_click=lambda es, path=img_path: process_and_remove_bg(path)  # Eliminar fondo
                    )
                ])
                image_list.controls.append(img_row)

            # Actualizar la interfaz con la lista de imágenes
            image_list.update()

        except Exception as e:
            removebg_result_text.value = f"Error al procesar las imágenes: {str(e)}"
            removebg_result_text.color = ft.colors.RED_400
            removebg_result_text.update()


    def process_and_remove_bg(img_path):
        try:
            # Asegurarse de que la ruta corresponde a un archivo, no un directorio
            if not os.path.isfile(img_path):
                raise ValueError(f"La ruta no es un archivo válido: {img_path}")

            # Aquí aplicas la lógica para eliminar el fondo de la imagen
            process_images(img_path)  # Esta es la función que procesará la imagen

            # Mostrar mensaje de éxito
            removebg_result_text.value = f"Fondo eliminado exitosamente de {img_path}"
            removebg_result_text.color = ft.colors.GREEN_400
            removebg_result_text.update()

        except Exception as e:
            # Si ocurre un error con alguna imagen, mostrar mensaje de error
            removebg_result_text.value = f"Error al eliminar el fondo de {img_path}: {str(e)}"
            removebg_result_text.color = ft.colors.RED_400
            removebg_result_text.update()

    #demas funciones estan bien
    def organize_directory(directory):
        try:
            organize_folder(directory)
            organize_result_text.value = "Archivos organizados exitosamente"
            organize_result_text.color = ft.colors.GREEN_400

        except Exception as e:
            organize_result_text.value = f"Error al organizar los archivos {str(e)}"
            organize_result_text.color = ft.colors.RED_400

        organize_result_text.update()

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

    # Vista de organizar archivos
    organize_files_views = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Organizar archivos en carpetas",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE_200,
                                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                "Seleccionar carpeta",
                icon=ft.icons.FOLDER_OPEN,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=organize_result_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            organize_dir_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Los archivos seran organizados en las siguientes carpetas",
                        size=20,
                        color=ft.colors.BLUE_200,

                    ),
                    ft.Text("Imágenes: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp", size=18),
                    ft.Text("Videos: .mp4, .avi, .mov, .mkv, .wmv, .flv", size=18),
                    ft.Text("Documentos: .pdf, .docx, .pptx, .txt, .rtf", size=18),
                    ft.Text("Datasets: .csv, .json, .xlsx, .tsv, .xml, .hdf5, .sav", size=18),
                    ft.Text("Comprimidos: .zip, .rar, .tar, .gz, .7z, .bz2", size=18),
                    ft.Text("Audio: .mp3, .wav, .aac, .flac, .ogg, .m4a", size=18),
                    ft.Text("Imágenes Vectoriales: .svg, .ai, .eps, .cdr", size=18),
                ]),
                border=ft.border.all(2, ft.colors.BLUE_400),
                border_radius=11,
                padding=22,
                margin=ft.margin.only(top=10),
                bgcolor=ft.colors.GREY_800,

            )
        ]),
        padding=30,
        expand=True
    )


    # Vista de Quitar fondo imagenes
    backgroundremove_file_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Remover fondo a imagenes",
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
                #delete_all_button,
            ]),
            ft.Container(
                content=removebg_result_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            removebg_result_text,

            ft.Container(
                content=image_list,
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
                icon=ft.icons.IMAGE_OUTLINED,
                selected_icon=ft.icons.IMAGE_ROUNDED,
                label="Remover Fondo"
            ),
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