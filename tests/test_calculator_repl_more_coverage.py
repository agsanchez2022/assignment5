# tests/test_calculator_repl_more_coverage.py
import builtins
from decimal import Decimal

import pytest
import app.calculator_repl as repl


# ----------------------------
# Dummy Observer Stubs
# ----------------------------

class DummyLoggingObserver:
    def update(self, calculation):
        return None


class DummyAutoSaveObserver:
    def __init__(self, calc):
        self.calc = calc

    def update(self, calculation):
        return None


# ----------------------------
# Dummy Calculator Stub
# ----------------------------

class DummyCalc:
    """
    Fake Calculator used only for REPL coverage tests.
    This avoids touching real history, files, or pandas.
    """

    def __init__(self):
        self._history = []
        self.save_raises = False
        self.load_raises = False
        self._undo_calls = 0
        self._redo_calls = 0

    # Observer hooks (needed at REPL startup)
    def add_observer(self, observer):
        return None

    def notify_observers(self, calculation=None):
        return None

    # History + persistence
    def save_history(self):
        if self.save_raises:
            raise RuntimeError("save failed")

    def load_history(self):
        if self.load_raises:
            raise RuntimeError("load failed")

    def show_history(self):
        return self._history

    def clear_history(self):
        self._history = []

    # Undo/redo behavior
    def undo(self):
        self._undo_calls += 1
        return self._undo_calls == 1

    def redo(self):
        self._redo_calls += 1
        return self._redo_calls == 1

    # Operation handling
    def set_operation(self, op):
        pass

    def perform_operation(self, a, b):
        # Decimal to hit normalize branch in REPL
        return Decimal("2.5000")


# ----------------------------
# Dummy Factory Stub
# ----------------------------

class DummyOpFactory:
    @staticmethod
    def create_operation(name):
        return object()


# ----------------------------
# Helper functions
# ----------------------------

def script_inputs(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(it))


def patch_repl(monkeypatch, dummy_calc):
    monkeypatch.setattr(repl, "Calculator", lambda: dummy_calc)
    monkeypatch.setattr(repl, "OperationFactory", DummyOpFactory)

    # Patch observers used during REPL initialization
    monkeypatch.setattr(repl, "LoggingObserver", DummyLoggingObserver)
    monkeypatch.setattr(repl, "AutoSaveObserver", DummyAutoSaveObserver)


# ----------------------------
# Tests
# ----------------------------

def test_repl_help_then_exit(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    script_inputs(monkeypatch, ["help", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "help" in out
    assert "goodbye" in out


def test_repl_history_clear_unknown(monkeypatch, capsys):
    dummy = DummyCalc()
    dummy._history = ["1 + 1 = 2", "2 * 3 = 6"]
    patch_repl(monkeypatch, dummy)

    script_inputs(monkeypatch, ["history", "clear", "history", "wat", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "calculation history" in out
    assert "history cleared" in out
    assert "no calculations" in out
    assert "unknown command" in out


def test_repl_undo_redo_branches(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    script_inputs(monkeypatch, ["undo", "undo", "redo", "redo", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "operation undone" in out
    assert "nothing to undo" in out
    assert "operation redone" in out
    assert "nothing to redo" in out


def test_repl_save_load_success_and_failure(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    def save_alt():
        if not dummy.save_raises:
            dummy.save_raises = True
        else:
            raise RuntimeError("save failed")

    def load_alt():
        if not dummy.load_raises:
            dummy.load_raises = True
        else:
            raise RuntimeError("load failed")

    dummy.save_history = save_alt
    dummy.load_history = load_alt

    script_inputs(monkeypatch, ["save", "save", "load", "load", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "saved" in out
    assert "error saving history" in out
    assert "loaded" in out
    assert "error loading history" in out


def test_repl_operation_cancel_and_success(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    script_inputs(
        monkeypatch,
        ["add", "cancel", "add", "5", "cancel", "add", "1", "2", "exit"]
    )

    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert out.count("operation cancelled") >= 2
    assert "result:" in out


def test_repl_keyboard_interrupt(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    calls = {"n": 0}

    def input_alt(prompt=""):
        calls["n"] += 1
        if calls["n"] == 1:
            raise KeyboardInterrupt
        return "exit"

    monkeypatch.setattr(builtins, "input", input_alt)
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "operation cancelled" in out


def test_repl_eof_exits(monkeypatch, capsys):
    dummy = DummyCalc()
    patch_repl(monkeypatch, dummy)

    monkeypatch.setattr(
        builtins, "input", lambda prompt="": (_ for _ in ()).throw(EOFError)
    )

    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "input terminated" in out