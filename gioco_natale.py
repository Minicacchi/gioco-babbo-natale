import arcade
import random
import time
import math


"""
Compiti per casa: La scorpacciata di Babbo Natale
Dato questo giochino come partenza, aggiungere le seguenti modifiche:
1 - Scaricare, disegnare o generare con AI un'immagine di sfondo
     e mostrarla poi come background
2 - Premendo il tasto "M", il suono verrà mutato. Premendolo di nuovo
     il suono deve tornare. Avete due possibilità: o evitate proprio
     di far partire il suono, o vi guardate come funziona play_sound
     e vedete se c'è qualcosa che vi può essere utile
3 - Contate quanti biscotti vengono raccolti, salvatelo in una variabile
4 - Mostrate con draw_text il punteggio (numero di biscotti raccolti)
5 - Fate in modo che il nuovo biscotto venga sempre creato almeno a 100 pixel
    di distanza rispetto al giocatore

6 - Ogni volta che babbo natale mangia 5 biscotti, dalla prossima volta
    in  poi verranno creati 2 biscotti per volta. Dopo averne mangiati
    altri 5, vengono creati 3 biscotti per volta, poi 4, e via dicendo

7 - (Opzionale) Ogni volta che genero un biscotto, al 3% di possibilità potrebbe essere un
         "golden cookie". Il golden cookie rimane solo 3 secondi sullo schermo
        ma vale 100 punti. 

        - Crea una nuova immagine per il golden cookie
        - Gestisci la creazione, il timer, ecc
        - Gestisci il punteggio

Fate questo esercizio in una repository su git e mandate il link al vostro account sul form
"""

class BabboNatale(arcade.Window):

    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.babbo = None
        self.lista_babbo = arcade.SpriteList()
        self.lista_cookie = arcade.SpriteList()

        self.background = None
        self.suono_munch = arcade.load_sound("./assets/munch.mp3")

        # Movimento
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.velocita = 4

        # Gioco
        self.soundOnOff = True
        self.biscotti_raccolti = 0
        self.cookie_spawn_count = 1
        self.punteggio = 0

        self.setup()

    def setup(self):
        self.background = arcade.load_texture("./assets/sfondo gioco.png")

        self.babbo = arcade.Sprite("./assets/babbo.png", scale=1.0)
        self.babbo.center_x = 300
        self.babbo.center_y = 100
        self.lista_babbo.append(self.babbo)

        self.lista_cookie.clear()

        for _ in range(self.cookie_spawn_count):
            self.crea_cookie()

    def crea_cookie(self):
        valid_position = False

        while not valid_position:
            is_golden = random.random() < 0.03

            if is_golden:
                cookie = arcade.Sprite("./assets/golden_cookie.png", scale=0.2)
                cookie.valore = 100
                cookie.spawn_time = time.time()
            else:
                cookie = arcade.Sprite("./assets/cookie.png", scale=0.2)
                cookie.valore = 1
                cookie.spawn_time = None

            cookie.center_x = random.randint(50, 550)
            cookie.center_y = random.randint(50, 550)
            
            # Calcola la distanza tra Babbo Natale e il biscotto
            distanza = math.sqrt(
                (cookie.center_x - self.babbo.center_x)**2 + 
                (cookie.center_y - self.babbo.center_y)**2
            )
            
            # Crea il biscotto solo se la distanza è >= 100 pixel
            if distanza >= 100:
                valid_position = True
                self.lista_cookie.append(cookie)
                
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, 600, 600)
        )

        self.lista_cookie.draw()
        self.lista_babbo.draw()

        arcade.draw_text(
            f"Biscotti: {self.biscotti_raccolti}",
            10, self.height - 30,
            arcade.color.WHITE, 20
        )

        arcade.draw_text(
            f"Punti: {self.punteggio}",
            400, self.height - 30,
            arcade.color.RED, 20
        )

    def on_update(self, delta_time):
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        self.babbo.center_x += change_x
        self.babbo.center_y += change_y

        self.babbo.center_x = max(0, min(self.width, self.babbo.center_x))
        self.babbo.center_y = max(0, min(self.height, self.babbo.center_y))

        # Collisioni
        collisioni = arcade.check_for_collision_with_list(
            self.babbo, self.lista_cookie
        )

        if collisioni:
            if self.soundOnOff:
                arcade.play_sound(self.suono_munch)

            for cookie in collisioni:
                cookie.remove_from_sprite_lists()
                self.biscotti_raccolti += 1
                self.punteggio += cookie.valore
                if self.punteggio > 0 and self.punteggio % 5 == 0:
                    self.cookie_spawn_count += 1
                else:
                    self.cookie_spawn_count=1
            for _ in range(self.cookie_spawn_count):
                self.crea_cookie()

        # Timer golden cookie (3 secondi)
        for cookie in self.lista_cookie:
            if cookie.spawn_time and time.time() - cookie.spawn_time > 3:
                cookie.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.up_pressed = True
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.down_pressed = True
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = True
        elif key == arcade.key.M:
            self.soundOnOff = not self.soundOnOff

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.up_pressed = False
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.down_pressed = False
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = False


def main():
    gioco = BabboNatale(600, 600, "Babbo Natale")
    arcade.run()


if __name__ == "__main__":
    main()