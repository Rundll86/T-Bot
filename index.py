from t_bot import TBot


if __name__ == "__main__":
    game = TBot()
    game.game_controller.wait_input()
    game.start()
    game.loop()
