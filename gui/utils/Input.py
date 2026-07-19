import pygame


class MouseListener:
    def mouse_button_down(self, event):
        pass

    def mouse_button_up(self, event):
        pass

    def mouse_motion(self, event):
        pass

    def mouse_wheel(self, event):
        pass


class KeyboardListener:
    def key_down(self, event):
        pass

    def keyUp(self, event):
        pass


class Input:
    def __init__(self):
        self.key_listeners = []
        self.mouse_listeners = []

    def add_mouse_listener(self, listener):
        self.mouse_listeners.append(listener)

    def add_keyboard_listener(self, listener):
        self.key_listeners.append(listener)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 2 or event.button == 3):
            for listener in self.mouse_listeners:
                consumed = listener.mouse_button_down(event)
                if consumed:
                    return True

        if event.type == pygame.MOUSEBUTTONUP:
            for listener in self.mouse_listeners:
                consumed = listener.mouse_button_up(event)
                if consumed:
                    return True

        if event.type == pygame.MOUSEMOTION:
            for listener in self.mouse_listeners:
                consumed = listener.mouse_motion(event)
                if consumed:
                    return True

        # Mouse wheel event is when the event type is MOUSEBUTTONDOWN and the button is 4 or 5
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
            for listener in self.mouse_listeners:
                consumed = listener.mouse_wheel(event)
                if consumed:
                    return True

        if event.type == pygame.KEYDOWN:
            for listener in self.key_listeners:
                consumed = listener.key_down(event)
                if consumed:
                    return True

        if event.type == pygame.KEYUP:
            for listener in self.key_listeners:
                consumed = listener.keyUp(event)
                if consumed:
                    return True
