from flask import Blueprint, render_template

from utils import cache

from data import scoreboard as scoreboard_
import config

scoreboard = Blueprint("scoreboard", __name__, template_folder="../templates/scoreboard")


@scoreboard.route('/scoreboard/')
def index():
    scoreboard_data = cache.get_complex("scoreboard")
    graph_data = cache.get_complex("graph")
    if scoreboard_data is None or graph_data is None:
        if config.immediate_scoreboard:
            scoreboard_data = scoreboard_.calculate_scores()
            graph_data = scoreboard_.calculate_graph(scoreboard_data)
            cache.set_complex("scoreboard", scoreboard_data, 120)
            cache.set_complex("graph", graph_data, 120)
        else:
            return "CTF hasn't started!"

    return render_template("scoreboard.html", data=scoreboard_data, graphdata=graph_data)
