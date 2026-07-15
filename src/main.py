import flet as ft

KEY_BINDINGS = {
    "move_left":"A",
    "move_right":"D",
    "move_down":"S",
    "move_up":"W"
}

class Player():
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y

    def move_character(self, x,y):
        self.x += x
        self.y += y


def main(page: ft.Page):
    player = Player()
    text = ft.Text("Peenar",animate_position=100,left = 0)
    movement_container = ft.Container(
        ft.Stack(
            [
                text
            ],
        ),
        bgcolor=ft.Colors.RED,
        width = 500,
        height= 500
    )

    def move_player(x,y):
        player.move_character(x,y)
        text.top = player.y * -10
        text.left = player.x * -10
        print(text.top)
        page.update()

  

    def on_keyboard(e: ft.KeyboardEvent):
        print(
            f"Key Pressed: {e.key}\n"
            f"Shift: {e.shift} | Ctrl: {e.ctrl} | Alt: {e.alt} | Meta: {e.meta}"
        )
        key = e.key

        if key == KEY_BINDINGS["move_up"]:
            move_player(0,1)
        elif key == KEY_BINDINGS["move_down"]:
            move_player(0,-1)
        elif key == KEY_BINDINGS["move_left"]:
            move_player(1,0)
        elif key == KEY_BINDINGS["move_right"]:
            move_player(-1,0)
                    
    page.on_keyboard_event = on_keyboard

    page.controls.append(
        movement_container
    )

ft.run(main)