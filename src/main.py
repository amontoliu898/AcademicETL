from database import create_tables
from gui import App


def main():
    create_tables()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()