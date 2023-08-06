import json
import os
import requests
import subprocess
import urllib.parse
from datetime import timedelta, datetime, timezone
from simple_term_menu import TerminalMenu
from .tilos_shows import SHOWS

"""Notes:
Search API: https://tilos.hu/api/search?q=7terito
Episode API: https://tilos.hu/api/show/dawn-tempo/episodes?start=1544620400000&end=1654984800000
Episode API timestamp is ms since epoch
"""

SEARCH_API = "https://tilos.hu/api/search?q="
SELECTOR_MODES = [
    "[e] Listen live",
    "[f] Full search (search for a show and select which episode you want to play)",
    "[l] Play latest (select a show and the latest episode will play)",
]


class Selector:
    @staticmethod
    def interactive():
        clear_console()
        Selector.print_brand()

        mode = Selector.select_mode()

        if (
            mode
            == "[f] Full search (search for a show and select which episode you want to play)"
        ):
            selected_show = Selector.select_show()
            selected_episode = selected_show.select_episode()
            selected_episode.play()
        elif mode == "[l] Play latest (select a show and the latest episode will play)":
            show_list = Selector.get_show_list()
            terminal_menu = TerminalMenu(
                show_list,
                title=Formatter.instruction(
                    text="Select a show and listen to its latest episode",
                    help="Press Enter to select and '/' to search",
                ),
            )
            show_index = terminal_menu.show()

            selected_show = Selector.get_show_from_index(show_index, show_list)

            print(f"\nPlaying the latest episode of {selected_show.title}")
            selected_show.play_latest_episode()
        elif mode == "[e] Listen live":
            start_livestream()

    def get_show_from_index(index, show_list):
        show_builder = SHOWS[show_list[index]]

        return Show(show_builder)

    @staticmethod
    def get_show_list():
        return list(SHOWS.keys())

    @staticmethod
    def print_brand():
        print(Formatter.brand("Tilos Player Unofficial 0.2"))

    @staticmethod
    def select_mode():
        print(
            Formatter.instruction(
                text="Select how you want to use the app: ",
                help="Hint: Use the shortcuts in []\n",
            )
        )
        terminal_menu = TerminalMenu(SELECTOR_MODES)
        selected_index = terminal_menu.show()

        return SELECTOR_MODES[selected_index]

    @staticmethod
    def search_shows(search_string):
        request_target = SEARCH_API + urllib.parse.quote_plus(search_string)
        raw_response = requests.get(request_target)
        response = json.loads(raw_response.text)
        shows_only = Selector.keep_only_shows(response["elements"])

        return shows_only

    def keep_only_shows(elements):
        return list(filter(lambda x: "/show/" in x["uri"], elements))

    @staticmethod
    def select_show():
        query = input("Search for a show: ")
        shows = Selector.search_shows(query)

        query_results = [s["title"] for s in shows]
        if not len(query_results) == 0:
            print(f"\nResults for {query}")
            terminal_menu = TerminalMenu(query_results)
            selected_index = terminal_menu.show()

            return Show(valid_selection(selected_index, shows))
        else:
            print(
                Formatter.error(
                    text=f"No show matches your search '{query}'. Please try again: "
                )
            )
            return Selector.select_show()


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def valid_selection(selected_index, options):
    """Validates user input which is guaranteed to be provided as
    an int. Checks if the given index makes sense as a 0-based index
    in the context of the options array"""
    if selected_index >= len(options):
        print("No show/episode")
        exit()
    else:
        return options[selected_index]


class Show:
    def __init__(self, show_data):
        """Show_data should have keys 'title' and either an 'uri_name'
        or the 'uri' itself"""
        self.title = Show.get_name(show_data)
        self.uri = Show.get_uri(show_data)
        self.episodes_api = f"https://tilos.hu/api/show/{self.uri}/episodes?"

    @staticmethod
    def get_uri(show_data):
        try:
            if "score" in show_data.keys():
                # score key is present in API search results but its
                # alias is not set correctly
                raise KeyError

            return show_data["alias"]
        except KeyError:
            return show_data["uri"].split("/")[-1]

    @staticmethod
    def get_name(show_data):
        try:
            return show_data["name"]
        except:
            return show_data["title"]

    def get_episodes(self):
        end_date = datetime.now().replace(tzinfo=timezone.utc)
        start_date = end_date - timedelta(days=120)

        episode_api_target = self.create_episode_api_link(start_date, end_date)

        response = requests.get(episode_api_target)
        episodes = json.loads(response.text)

        return episodes

    def create_episode_api_link(self, start_date, end_date):
        start_timestamp = date_to_timestamp(start_date)
        end_timestamp = date_to_timestamp(end_date)

        request_target = self.episodes_api + f"start={start_timestamp}"
        request_target += f"&end={end_timestamp}"

        return request_target

    def select_episode(self):
        episodes = self.get_episodes()
        episode_options = [str(timestamp_to_date(ep["plannedFrom"])) for ep in episodes]
        print(Formatter.instruction(text="Select an episode to play"))
        terminal_menu = TerminalMenu(episode_options)
        selected_index = terminal_menu.show()

        return Episode(valid_selection(selected_index, episodes))

    def play_latest_episode(self):
        eps = self.get_episodes()
        latest_episode = valid_selection(0, eps)
        Episode(latest_episode).play()


class Episode:
    def __init__(self, episode_data):
        # episode_data must contain the .m3u of the episode under key m3uUrl
        # Generally the source of episode_data is the Tilos API
        # /api/show/<showN>/episodes?start=[...]&end=[...]
        self.url = episode_data["m3uUrl"]

    def play(self):
        bashCommand = f"vlc {self.url}"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

def start_livestream():
    bash_command = f"vlc https://stream.tilos.hu/tilos_128.mp3"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def timestamp_to_date(date):
    """Date is ms epoch time"""
    return datetime.fromtimestamp(date / 1000)


def date_to_timestamp(date):
    return int(date.timestamp() * 1000)


class Formatter:
    @staticmethod
    def brand(text):
        return f"{col.bg.white}{col.fg.blue}{col.bold}{text}{col.reset}"

    @staticmethod
    def instruction(text, help=None, input_indicator=None):
        formatted = f"\n{col.bold}{col.bg.white}{col.fg.blue}{text}{col.reset}\n"

        if help:
            formatted += f"{help}"

        if input_indicator:
            formatted += f"\n{input_indicator} "
        return formatted

    @staticmethod
    def error(text):
        return f"{col.fg.cred}{text}{col.reset}"


class col:
    # https://www.codegrepper.com/code-examples/python/reset+color+ascii+code+python
    reset = "\033[0m"
    bold = "\033[01m"
    underline = "\033[04m"

    class fg:
        blue = "\033[34m"
        cred = "\033[38;2;255;40;20m"

    class bg:
        white = "\033[48;2;255;255;255m"
