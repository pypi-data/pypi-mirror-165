"""
This stand-alone module can be copied around as a single file for ease in
distribution (e.g., along with a notebook). It interfaces with `optimism`
test cases and provides machinery for sending the results of those test
cases to a `potluck_server` instance.

You will need to customize this file before distribution to embed the
correct server URL for submission, and the correct & current delivery key
for that server.

At this time, there are no security checks: anybody in the world with a
current delivery key can send uploads to a server under any username they
choose. We recommend that you at least cycle your delivery keys every so
often, but you will need to trust your users quite a bit. However,
submissions via `potluckDelivery` do not result in running submitted code
on the server, at least. Note that typos in usernames may result in
incorrect submissions.

`deliver` is the main function to use: it should be used after an
`optimism` test suite has been started using `optimism.startTestSuite`
and one or more outcomes have been registered in that test suite. All
outcomes registered in the current suite will be gathered and submitted.
The first time this happens the user will be asked for the username(s) of
each participating author; subsequently that information is stored
globally and re-used. If you need to change authorship, you can use the
`setAuthors` function or just restart your Python session (e.g., restart
the kernel if you're in a notebook, or stop and restart Python elsehow).
"""

import urllib, urllib.parse, urllib.request, urllib.error
import json, sys, datetime

try:
    import optimism
except ModuleNotFoundError:
    print(
        "Warning: The 'optimism' module is not available. We will not"
        " be able to check exercises or submit them.",
        file=sys.stderr
    )
    optimism = None

__version__ = 1.1
"""
Version number for this script, separate from the `potluck` and
`potluck_server` versions just in case it's useful.
"""

AUTHORS = None
"""
A pair including list of strings indicating which user account(s)
submissions should be assigned to, followed by a `datetime.datetime`
object indicating when that information was provided. Use `setAuthors`
and/or `collectAuthors` to update this; use `getAuthors` to retrieve
authors in a way that respects the timeout.
"""

AUTHORS_TIMEOUT = datetime.timedelta(hours=3)
"""
The duration after which we'll ask for authors again during a single
session. Author information is not cached between sessions.
"""

BASE_URL = "http://www.example.com/potluck/"
"""
This URL will form the base of the submission URL, and should point to
the root URL for the potluck server you want to submit to. You need to
edit this if you are setting up `potluckDelivery` for distribution to
students, but if you are a student who received a copy of this file, you
should NOT edit it unless your instructor specifically tells you to.
"""

COURSE = "example_class"
"""
This string should name the course you want to submit to, as set in the
`potluck_server` configuration. It will be used as part of the URL to
submit to. Editing this in a provided `potluckDelvery.py` file might
result in your submissions being ignored.
"""

SEMESTER = "fall22"
"""
This string should name the semester you want to submit to, as set in the
`potluck_server` configuration. It will be used as part of the URL to
submit to. Editing this in a provided `potluckDelvery.py` file might
result in your submissions being ignored.
"""

PREFIX = None
"""
A prefix to be used with optimism suite names to produce exercise names
(a dash is inserted between the prefix and the suite name). If left as
`None`, just optimism test suite names are used for submission.
"""

INCLUDED_CODE = {}
"""
A mapping from test suite names to lists of pairs, where each pair
contains a 'filename' string and a code string. This represents extra
code to be included with the submission, specified using `includeCode`.
"""

USERNAME_DESC = " (your username is your email without the '@' part)"
"""
A description of what a username is, to be included when asking for a
username. Set to an empty string if you don't want to include one.
"""


def setup(url=None, course=None, semester=None):
    """
    Changes the submission URL, course ID, and/or semester that will be
    used when `deliver` is called. Leave values as `None` (the default)
    to avoid changing them.
    """
    global BASE_URL, COURSE, SEMESTER
    if url is not None:
        BASE_URL = url

    if course is not None:
        COURSE = course

    if semester is not None:
        SEMESTER = semester


def deliver():
    """
    Collects outcomes registered with the current `optimism` test suite
    and sends an HTTP POST request to the configured potluck server with
    that information plus authorship information from the `AUTHORS`
    variable (see `setAuthors`). If `AUTHORS` hasn't yet been specified,
    asks for authors via `input` and stores that information for re-use.

    Collects code to submit alongside outcomes based on
    `optimism.TestManager` objects associated with `optimism.Trial`
    objects which have been created since the current test suite started.
    Additional code may be attached by using `includeCode`.

    Note that merely creating a manager won't add its code: you have to
    derive a test case or code check from it. Use `optimism.mark`

    Note that using `optimism.freshTestSuite` is recommended so that if
    code gets re-run within the same session (e.g., as a notebook cell
    often does) old outcomes will not accumulate.
    """
    global optimism

    authors = getAuthors()
    if authors is None:
        print(
            "Unable to submit without authorship information. Please"
            " try again."
        )
        return

    if optimism is None:
        try:
            import optimism
        except ModuleNotFoundError:
            raise RuntimeError(
                "Cannot submit results if the 'optimism' module is not"
                " available."
            )

    # Get relevant managers and associated code blocks from optimism,
    # derived from trials in the current test suite. Note that use of
    # `opitmism.expect` does not involve a trial, but in that case, we
    # don't actually know what code is being tested.
    suiteName = optimism.currentTestSuite()
    trials = optimism.listTrialsInSuite(suiteName)
    managers = []
    codeBlocks = []
    seenAlready = set()
    for trial in trials:
        manager = trial.manager
        if id(manager) not in seenAlready:
            seenAlready.add(id(manager))
            managers.append(manager)
            if manager.code is not None:
                codeBlocks.append((manager.codeFilename(), manager.code))

    # Attach any code blocks specified using `includeCode`.
    codeBlocks.extend(INCLUDED_CODE.get(suiteName, []))

    # Get outcomes from optimism
    outcomes = optimism.listOutcomesInSuite(suiteName)

    doDelivery(authors, suiteName, outcomes, codeBlocks)


class NoCondition:
    """
    Placeholder object for indicating absence of a condition in
    `deliverOutcome`.
    """
    pass


def deliverOutcome(
    suite=None,
    condition=NoCondition,
    note="✓ check succeeded",
    failNote="✗ check failed",
    grabCode=None
):
    """
    Delivers a result with a single artificial 'outcome' instead of
    gathering outcomes via `optimsim` like `deliver` does. This can be
    used even when optimism is not available, and should normally be put
    behind a conditional and/or after an assert so that it only runs
    when something is actually working. If a condition is given, it will
    be converted to a boolean to determine whether the artificial
    outcome is a success or a failure.

    Note that this doesn't print anything about success or failure of the
    condition: use `optimism` if you want to actually do testing, or at
    least add your own printing code along side th `deliverOutcome` call.

    Arguments can override various info that's normally collected
    automatically, so that a single call to this function can suffice
    for submission without needing to call other stuff beforehand:

    - `suite` will be used in place of the current optimism test
        suite name, with any prefix established by `prefix` still
        applied. In cases where `suite` is not set and `optimism` is not
        available, the string "default" will be used.
    - `grabCode` should be a list of strings; code marked using
        `optimism.mark` and those strings will be included in the
        submission. If optimism is not available, setting `grabCode` to
        anything other than `None` or an empty list will result in an
        error. Even when `grabCode` is set to None, if optimism is
        available and there's a marked code segment that shares the
        suite name provided, it will be included.

    The `note` and `failNote` arguments will be used as the outcome
    message value for the constructed outcome. Note that there is no way
    to submit a multi-outcome result using this function, and recorded
    optimism outcomes will NOT be submitted along with the artificial
    outcome.

    This function will prompt for authors if that information isn't yet
    available, and will use the global authors info if it is.
    """
    global optimism

    authors = getAuthors()
    if authors is None:
        print(
            "Unable to submit without authorship information. Please"
            " try again."
        )
        return

    if optimism is None:
        try:
            import optimism
        except ModuleNotFoundError:
            pass

    # Get test suite name from optimism or as specified
    if suite is None:
        if optimism is None:
            suite = "default"
        else:
            suite = optimism.currentTestSuite()

    # Grab code blocks if specified
    codeBlocks = []
    if grabCode is not None:
        if grabCode and optimism is None:
            raise ValueError(
                "grabCode cannot be used when optimism is not"
                " available."
            )
        for mark in grabCode:
            codeBlocks.append(
                [f"code marked '{mark}'", optimism.getMarkedCode(mark)]
            )
    elif optimism is not None:
        suiteBlock = optimism.getMarkedCode(suite)
        if suiteBlock is not None:
            codeBlocks.append([f"code marked '{suite}'", suiteBlock])

    # Construct our outcome
    outcomes = [
        [
            bool(condition),
            "custom outcome",
            note if condition else failNote
        ]
    ]

    doDelivery(authors, suite, outcomes, codeBlocks)


def doDelivery(authors, suiteName, outcomes, codeBlocks):
    """
    Handles delivery via an HTTP request once info is assembled,
    printing some messages about the process to notify of success or
    failure.

    This function applies any current prefix (see `prefix`) to the given
    suite name.

    It uses the `BASE_URL`, `COURSE`, and `SEMESTER` variables to figure
    out where to send the delivery (see `setup`).

    Error messages on failed delivery are printed to the error stream
    (stderr); other messages are printed to normal output (stdout).
    """
    # Figure out exercise name
    if PREFIX is not None:
        exercise = PREFIX + ':' + suiteName
    else:
        exercise = suiteName

    # Print submission info
    print(
        (
            f"Submitting {len(outcomes)} outcome(s) for exercise"
            f" '{exercise}' from authors:\n  "
        ) + '\n  '.join(authors)
    )

    # Figure out URL and data to send
    destination = '/'.join((BASE_URL, COURSE, SEMESTER)) + '/deliver'
    encoded = urllib.parse.urlencode(
        {
            "exercise": exercise,
            "authors": json.dumps(authors),
            "outcomes": json.dumps(outcomes),
            "code": json.dumps(codeBlocks),
        }
    )
    payload = bytes(encoded, encoding="utf-8")
    print(f"Submitting to {destination} ...")
    try:
        with urllib.request.urlopen(destination, payload) as response:
            result = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(
            (
                "Error: delivery of results failed. Message from"
                " server:\n"
            ) + e.read().decode(encoding="utf-8"),
            file=sys.stderr
        )
        return

    if result.startswith("Submission accepted:"):
        print(result)
    else:
        print(
            (
                "Error: delivery of results failed. Message from"
                " server:\n"
            ) + result,
            file=sys.stderr
        )


def prefix(pre=None):
    """
    Establishes a suite-name prefix that will be used with all
    submissions. The value should be a string, although using the
    default (`None`) will remove the prefix. This does not affect the
    identity of optimism test suites, but it does change the
    exercise name listed in the submission. A dash will be placed
    between the prefix (if there is one) and the optimism test suite
    name.
    """
    global PREFIX
    PREFIX = pre


def includeCode(filename, markName):
    """
    Grabs code from a marked block (see `opimism.mark`) to include in
    the submission sent by `deliver` for the current optimism test
    suite. Not usually necessary, as any code involved in test managers
    which are used to generate trials in the current suite will be
    included automatically, but if you use `optimism.expect` instead of
    using test manager(s), this may be useful.

    Note that this likely won't work in an interactive session, since
    the `optimism.mark` function may not be able to capture code in that
    case.

    The filename for the code being gathered is determined by the first
    argument here.
    """
    global INCLUDED_CODE
    code = optimism.getMarkedCode(markName)
    if code is None:
        print(
            (
                f"Warning: could not find code for mark '{markName}'."
                f" Have you run code which calls"
                f" optimism.mark('{markName}') yet?"
            ),
            file=sys.stderr
        )
    suiteName = optimism.currentTestSuite()
    INCLUDED_CODE.setdefault(suiteName, []).append([filename, code])


def setAuthors(*usernames):
    """
    Accepts any number of usernames and stores them as the list of
    authors that submissions will be assigned to. If you don't call this,
    authorship information will be asked for the first time it's needed
    and then re-used until this function is called.

    Each username provided must be a string, or a `TypeError` will be
    raised.
    """
    global AUTHORS
    if not all(isinstance(un, str) for un in usernames):
        raise TypeError("Each username must be a string.")
    AUTHORS = (usernames, datetime.datetime.now())


def collectAuthors():
    """
    Asks the user to enter authorship information, updating the `AUTHORS`
    global variable. Uses `USERNAME_DESC` as part of the prompt.
    """
    print(
        f"Please enter the username(s) of each author separated by"
        f" commas and/or spaces{USERNAME_DESC}."
    )
    unames = input("Enter usernames: ")
    bits = unames.split()
    allBits = []
    for bit in bits:
        allBits.extend(
            bit.strip() for bit in bit.split(',') if bit.strip()
        )

    if len(allBits) > 0:
        setAuthors(*allBits)
    else:
        print("You didn't enter any author names.")


def getAuthors():
    """
    Gets the current authors list, asking the user to enter that
    information if it's not set up yet, and/or if the existing
    information has expired.

    Returns `None` if the user enters invalid info.
    """
    global AUTHORS
    now = datetime.datetime.now()
    if AUTHORS is None or len(AUTHORS[0]) == 0:
        print(
            "You have not yet entered authorship information for this"
            " session."
        )
        collectAuthors()

    if AUTHORS is None or len(AUTHORS[0]) == 0:
        return None

    if AUTHORS[1] + AUTHORS_TIMEOUT < now:
        print(
            "The stored authors information has expired, please"
            " re-enter the authors list based on who you are working"
            " with now."
        )
        collectAuthors()

    if (
        AUTHORS is None
     or len(AUTHORS[0]) == 0
     or AUTHORS[1] + AUTHORS_TIMEOUT < now
    ):
        AUTHORS = None
        return None

    return AUTHORS[0]
