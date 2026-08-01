import tests.u as u
import trelby.screenplay as scr
from trelby.line import Line


def _mksp(lines):
    sp = u.new()
    sp.lines = lines
    return sp


def testContinuedAddedAfterInterveningAction():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First line."),
            Line(scr.LB_LAST, scr.ACTION, "He sits."),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "Second line."),
        ]
    )

    assert not sp.shouldAddDialogueContinuedForCharacter(1)
    assert sp.shouldAddDialogueContinuedForCharacter(4)
    assert sp.getCharacterTextForDisplay(4) == "JOHN (cont'd)"


def testContinuedNotAddedWhenDifferentSpeakerInBetween():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First."),
            Line(scr.LB_LAST, scr.CHARACTER, "MARY"),
            Line(scr.LB_LAST, scr.DIALOGUE, "Second."),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
        ]
    )

    assert not sp.shouldAddDialogueContinuedForCharacter(5)


def testContinuedNotAddedAcrossSceneBoundary():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First."),
            Line(scr.LB_LAST, scr.SCENE, "EXT. STREET - NIGHT"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
        ]
    )

    assert not sp.shouldAddDialogueContinuedForCharacter(4)


def testContinuedNotDuplicatedIfAlreadyPresent():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First."),
            Line(scr.LB_LAST, scr.ACTION, "Pause."),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN (cont'd)"),
        ]
    )

    assert not sp.shouldAddDialogueContinuedForCharacter(4)
    assert sp.getCharacterTextForDisplay(4) == "JOHN (cont'd)"


def testStrictSpeakerMatchingWithVoiceModifier():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First."),
            Line(scr.LB_LAST, scr.ACTION, "Pause."),
            Line(scr.LB_LAST, scr.CHARACTER, "JOHN (V.O.)"),
        ]
    )

    assert not sp.shouldAddDialogueContinuedForCharacter(4)


def testDisplayTextUsesExportCapsWithoutUppercasingContinuation():
    sp = _mksp(
        [
            Line(scr.LB_LAST, scr.SCENE, "INT. ROOM - DAY"),
            Line(scr.LB_LAST, scr.CHARACTER, "john"),
            Line(scr.LB_LAST, scr.DIALOGUE, "First."),
            Line(scr.LB_LAST, scr.ACTION, "Pause."),
            Line(scr.LB_LAST, scr.CHARACTER, "john"),
        ]
    )

    assert sp.getCharacterTextForDisplay(4, True) == "JOHN (cont'd)"
