from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import requests

class TvShowMixin(object):
    def get_show(self, imdb_id):
        # method to get a dictionary with
        # the show's name, previous and next episode date

        req = requests.get(
            'http://api.tvmaze.com/lookup/shows?imdb={}'.format(imdb_id),
        )
        if req.status_code != 200:
            print 'imdb id not good'
        show_info = req.json()
        try:
            prev_ep = requests.get(show_info['_links']['previousepisode']['href'])
            next_ep = requests.get(show_info['_links']['nextepisode']['href'])
            prev_ep = prev_ep.json()
            next_ep = next_ep.json()
        except KeyError:
            prev_ep = {'airdate': None, 'name': None}
            next_ep = {'airdate': None, 'name': None}

        return {
            'name': show_info['name'],
            'previous_date': prev_ep['airdate'],
            'previous_name': prev_ep['name'],
            'next_date': next_ep['airdate'],
            'next_name': next_ep['name'],
        }


    def get_tv_shows(self):
        # dictionary with all the tv shows as key: show name and
        # imdb id as value
        tv_shows = {
            'vampire_diaries': 'tt1405406',
            'the_flash': 'tt3107288',
            'frequency': 'tt5531470',
            'dark_matter': 'tt4159076',
            'killjoys': 'tt3952222',
            'rosewood': 'tt4465472',
            'second_chance': 'tt4378456',
            'blindspot': 'tt4474344',
            'suits': 'tt1632701',
            'lethal_weapon': 'tt5164196',
            'simpsons': 'tt0096697',
            'brooklyn_99': 'tt2467372',
            'teen_wold': 'tt1567432'
        }
        return [
            self.get_show(tv) for tv in tv_shows.values()
            ]


class TvShowsApp(App, TvShowMixin):
    def build(self):
        shows = self.get_tv_shows()
        number_shows = len(shows)
        layout = GridLayout(rows=number_shows)
        layout.bind(minimum_height=layout.setter('height'))
        for show in shows:
            if not show['next_date']:
                continue
            layout.add_widget(Label(
                text='[b]{name}[/b]\n'
                     '{next} {next_name}\n{prev} {prev_name}'.format(
                    name=show['name'], next=show['next_date'],
                    next_name=show['next_name'], prev_name=show['previous_name'],
                    prev=show['previous_date']
                ), markup=True, halign='left', valign='middle'
            ))
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        return root

if __name__ == '__main__':
    TvShowsApp().run()

