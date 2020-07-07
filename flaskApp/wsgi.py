import json
import os
import getopt
import sys
from flask import Flask, render_template, request, Response, redirect
from flaskApp.game.Board import Board
from flaskApp.gameData import GameData, GameDataEncoder


try:
    opts, args = getopt.getopt(sys.argv[1:], "c:h", ["help", "config="])
except getopt.GetoptError:
    print('Usage: wsgi.py -c <configObject>')
    sys.exit(2)

if not opts:
    opts.append(('--help', ''))

config = ''

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('Usage: wsgi.py -c || --config <configObject>')
        sys.exit()
    if opt in ("-c", "--config"):
        config = arg

app = Flask(__name__)
app.config.from_object(config)
data = {}


@app.route('/')
def menu():
    images = os.listdir(os.path.join(os.path.curdir, 'graphics'))
    return render_template('index.html', images=images)


@app.route('/start_game', methods=["POST"])
def start_game():
    id = os.urandom(6).hex()
    if app.config['IN_FILES']:
        if not os.path.exists(os.path.join(os.path.curdir, 'data')):
            os.mkdir('data')
        with open('data/'+id+'.json', 'w+') as file:
            file.write(json.dumps(GameData(Board(int(request.form['row']), int(request.form['column']), "graphics/" + request.form['image']), request.form['name']), indent=4, cls=GameDataEncoder))
            return Response(id)
    else:
        data[id] = GameData(Board(int(request.form['row']), int(request.form['column']), "graphics/" + request.form['image']), request.form['name'])
        return Response(id)


@app.route("/game/<game_id>")
def game(game_id):
    if app.config['IN_FILES']:
        if os.path.exists(os.path.join('data', game_id + '.json')):
            with open('data/'+game_id+'.json', 'r') as file:
                game_data = json.load(file)
                return render_template("board.html", board=json.dumps(game_data["board"]["complete_board"]), game_id=json.dumps(game_id), filled=json.dumps(game_data["current_state"]))
        return redirect('/')
    if game_id in data.keys():
        return render_template("board.html", board=json.dumps(data[game_id].get_board().complete_board), game_id=json.dumps(game_id), filled=json.dumps(data[game_id].current_state))
    return redirect('/')


@app.route("/check/<game_id>", methods=["POST"])
def check(game_id):
    if app.config['IN_FILES']:
        with open('data/'+game_id+'.json', 'r+') as file:
            game_data = json.load(file)
            if game_data["board"]["filled_board"][int(request.form['row'])][int(request.form['column'])]:
                game_data["current_state"][int(request.form['row'])][int(request.form['column'])] = 1
                file.seek(0)
                file.truncate(0)
                file.write(json.dumps(game_data, indent=4))
                if game_data["board"]["filled_board"] == game_data["current_state"]:
                    os.unlink(file.name)
                    return Response('WON')
                return Response('OK')
            return Response('NOT OK')
    else:
        current_data = data[game_id]
        if current_data.get_board().is_painted(int(request.form['column']), int(request.form['row'])):
            current_data.update(int(request.form['column']), int(request.form['row']))
            if current_data.finished():
                del data[game_id]
                return Response('WON')
            return Response('OK')
        return Response('NOT OK')


if __name__ == "__main__":
    app.run()
