import chess
import requests
from io import StringIO
from bs4 import BeautifulSoup
import chess.pgn
# import chess.uci
from chess.pgn import BaseVisitor


class ChessAPI:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.session.post('http://www.chess.com/login_check',
                          data={
                              '_username': username,
                              '_password': password,
                              '_timezone': 'America/Chicago',
                              '_target_path': 'https://www.chess.com/home'
                          })

    def create_puzzle(self, board, moves):
        game = chess.pgn.Game()
        game.setup(board)
        game.end().add_line(moves)

        last_move = game.move
        flip = game.board().turn is False  # is it black's turn
        exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=False)
        pgn_string = game.accept(exporter)
        data = """&-diagramtype:
chessProblem
&-colorscheme:
brown
&-piecestyle:
3dwood
&-float:
left
&-flip:
%s
&-prompt:
false
&-coords:
true
&-size:
200
&-lastmove:
%s
&-focusnode:
&-beginnode:
&-endnode:
&-hideglobalbuttons:
false
&-pgnbody:
%s""" % (str(flip).lower(), last_move, pgn_string)
        response = self.session.post("https://www.chess.com/tinymce/api/get_diagram?id=new", data={'textSetup': data})
        return 'http://www.chess.com/emboard?id=%s' % int(response.content)

    def get_games(self, member_name):
        pass


class Puzzle:
    def __init__(self, board, moves):
        self.game = chess.pgn.Game()
        self.game.setup(board)
        self.game.end().add_line(moves)


class AnnotatedVisitor(BaseVisitor):
    def __init__(self, api):
        self.puzzles = []
        self.api = api
        self.last_board = None
        self.moves = []
        self.in_variation = False
        self.severity = 0

    def visit_move(self, board, move):
        if not self.in_variation:
            self.last_board = board
            self.moves = []
        else:
            self.moves.append(move)

    def begin_variation(self):
        self.in_variation = True

    def end_variation(self):
        self.in_variation = False
        self.puzzles.append((self.severity, self.api.create_puzzle(self.last_board, self.moves)))

    def visit_comment(self, comment):
        if 'inaccuracy' in comment.lower():
            self.severity = 1
        elif 'mistake' in comment.lower():
            self.severity = 2
        elif 'blunder' in comment.lower():
            self.severity = 4
        elif 'missed mate' in comment.lower():
            self.severity = 4


class AnalysisVisitor(BaseVisitor):
    def __init__(self, stockfish_path, max_time_per_move=1000, max_depth_per_move=20):
        self.info_handler = chess.uci.InfoHandler()
        self.engine = chess.uci.popen_engine(stockfish_path)
        self.engine.info_handlers.append(self.info_handler)
        self.engine.uci()
        self.engine.ucinewgame()
        self.max_time_per_move = max_time_per_move
        self.max_depth_per_move = max_depth_per_move
        self.puzzles = []

    def visit_move(self, board, move):
        self.engine.ucinewgame()
        self.engine.position(board)
        best_move, _ = self.engine.go(depth=self.max_depth_per_move, movetime=self.max_time_per_move / 3)

        board.push(move)
        self.engine.ucinewgame()
        self.engine.position(board)
        self.engine.go(depth=self.max_depth_per_move, movetime=self.max_time_per_move / 3)
        your_score = self.info_handler.info["score"][1]
        board.pop()

        board.push(best_move)
        self.engine.ucinewgame()
        self.engine.position(board)
        self.engine.go(depth=self.max_depth_per_move, movetime=self.max_time_per_move / 3)
        ideal_score = self.info_handler.info["score"][1]
        board.pop()

        create_puzzle = False
        use_all_moves = False
        if ideal_score.cp and your_score.cp:
            # No mates detected, just compare the scores
            absolute_difference = abs(ideal_score.cp - your_score.cp)
            if absolute_difference > 200:
                create_puzzle = True
        elif ideal_score.mate and ideal_score.mate > 0 and your_score.cp:
            # Ideal solution has a mate and yours doesn't - BLUNDER
            create_puzzle = True
        elif ideal_score.mate and your_score.mate:
            absolute_difference = ideal_score.mate - your_score.mate
            if absolute_difference > 1 and ideal_score.mate > 0:
                create_puzzle = True
                use_all_moves = True

        if create_puzzle:
            moves = [best_move] + self.info_handler.info['pv'][1]
            if not use_all_moves:
                moves = moves[:min(len(moves), 5)]
            else:
                moves = moves[:min(len(moves), 14)]
            self.puzzles.append(Puzzle(board, moves))

