from t_bot import TBot


if __name__ == "__main__":
    game = TBot()
    game.start()
    print(game.world)
    input("")
    game.loop()
