def main():
    choice = input("Do you want to use the GUI or CLI? (gui/cli): ").lower()

    if choice == "gui":
        from scripts.interface import gui
        gui.run_gui()
    elif choice == "cli":
        from scripts.interface import cli
        cli.run_cli()
    else:
        print("Invalid choice. Please choose either 'gui' or 'cli'.")
        main()

if __name__ == "__main__":
    main()
