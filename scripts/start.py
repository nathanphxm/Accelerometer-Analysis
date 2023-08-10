import sys, process_to_csv

def main(): 
    while True:
        print("----------OPTIONS----------")
        print("1. Process raw .txt file to .csv")
        print("...")
        print("9. Information about each option")
        print("0. Exit")
        
        option = input("Please enter your desired option: ")
        
        if option == "1":
            filename = input("Please enter the path of the file: ").strip("'")
            print(f"Now processing {filename}...")
            process_to_csv.main(filename)
            break
        elif option == "9":
            print("Which option would you like to learn more about?")
            break
        elif option == "0":
            print("The script will now exit.")
            break
        else:
            print("Please enter a valid option.")
        
    
if __name__ == "__main__":
    main()