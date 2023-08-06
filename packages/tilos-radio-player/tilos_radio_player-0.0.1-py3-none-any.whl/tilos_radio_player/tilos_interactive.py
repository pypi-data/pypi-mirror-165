import os

filename = "tilos_shows.json"
script_folder = os.path.dirname(os.path.realpath(__file__))
SHOWS_FILE = os.path.join(script_folder, filename)

def main():
    if not "tilos_shows.json" in script_folder:
        from .tilos_api_shows import update_shows
        update_shows()
        
    from .tilos import Selector
    Selector.interactive()

if __name__=="__main__":
    main()