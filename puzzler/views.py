import datetime
import hashlib
import random
from io import StringIO

import chess.pgn
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

import random

from puzzler.ChessAPI import AnnotatedVisitor, ChessAPI
from puzzler.models import Puzzle


def home(request):
    puzzles = list(Puzzle.objects.all())
    random.shuffle(puzzles)

    return render(request, 'puzzler.html', {'puzzles': puzzles})


def add_annotated_pgn(request):
    if request.method == 'GET':
        return render(request, 'add_annotated_pgn.html')

    pgn_str = request.POST['pgn']

    api = ChessAPI(settings.USERNAME, settings.PASSWORD)
    pgn = StringIO(pgn_str)
    game = chess.pgn.read_game(pgn)
    visitor = AnnotatedVisitor(api)
    game.accept(visitor)
    for severity, link in visitor.puzzles:
        print(severity, link)
        Puzzle(severity=severity, link=link).save()

    messages.success(request, "Puzzles added!")

    return redirect(to="/add", request=request)
