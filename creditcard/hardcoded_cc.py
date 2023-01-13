import ast
import re

import bandit
from bandit.core import issue
from bandit.core import test_properties as test

RE_CANDIDATE_CC = re.compile(
    r"\b("
    + r"(?:4[0-9]{12}(?:[0-9]{3})?)"  # Visa
    + r"|(((?:5[1-5][0-9]{2})"
    + r"|"
    + r"(222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}))"  # MasterCard
    + r"|(3[47][0-9]{13})"  # American Express
    + r"|(3(?:0[0-5]|[68][0-9])[0-9]{11})"  # Diners Club
    + r"|(6(?:011|5[0-9]{2})[0-9]{12})"  # Discover
    + r"|((?:2131|1800|35\d{3})\d{11})"  # JCB
    + r")\b"
)


def _report(string, number):
    return bandit.Issue(
        severity=bandit.MEDIUM,
        confidence=bandit.MEDIUM,
        cwe=issue.Cwe.NOTSET,
        text=(
                "Possible hardcoded CreditCard Number: '%s' found in string literal '%s' "
                % (number, string)
        ),
    )


def substring_after(s, delim):
    return s.partition(delim)[2]

@test.checks("Str")
@test.test_id("B142")
def hardcoded_creditcard_string(context):
    """**B142: Hardcoded Creditcard Number**
    This check detects sequences of numbers used in string literals
    that look like credit card numbers.
    """
    node = context.node
    string_literal = "value"
    cc_number = "value"
    reports = []


    if isinstance(node._bandit_parent, ast.Assign):
        # looks for "candidate='some_string'"
        cut = substring_after(str(context), "str")[4:]
        import re
        CardNum = re.sub('[^A-Za-z0-9]+', '', cut)
        print(CardNum)

        for targ in node._bandit_parent.targets:
            if isinstance(targ, ast.Name) and RE_CANDIDATE_CC.search(targ.id):
                if str(CardNum[:3]) == "000":
                    pass
                else:
                    return _report(node.s)
            elif isinstance(targ, ast.Attribute) and RE_CANDIDATE_CC.search(targ.attr):
                if str(CardNum[:3]) == "000":
                    pass
                else:
                    return _report(node.s)

        reports.append(_report(CardNum, CardNum))

    elif isinstance(node._bandit_parent, ast.Subscript) and RE_CANDIDATE_CC.search(node.s):
        # Py39+: looks for "dict[candidate]='some_string'"
        # subscript -> index -> string
        cut = substring_after(str(context), "str")[4:]
        import re
        CardNum = re.sub('[^A-Za-z0-9]+', '', cut)
        print(CardNum)

        assign = node._bandit_parent._bandit_parent
        if isinstance(assign, ast.Assign) and isinstance(assign.value, ast.Str):
            if str(CardNum[:3]) == "000":
                pass
            else:
                return _report(assign.value.s)

        reports.append(_report(CardNum, CardNum))

    elif isinstance(node._bandit_parent, ast.Index) and RE_CANDIDATE_CC.search(node.s):
        # looks for "dict[candidate]='some_string'"
        # assign -> subscript -> index -> string
        cut = substring_after(str(context), "str")[4:]
        import re
        CardNum = re.sub('[^A-Za-z0-9]+', '', cut)
        print(CardNum)
        assign = node._bandit_parent._bandit_parent._bandit_parent
        if isinstance(assign, ast.Assign) and isinstance(assign.value, ast.Str):
            if str(CardNum[:3]) == "000":
                pass
            else:
                return _report(assign.value.s)

        reports.append(_report(CardNum, CardNum))

    elif isinstance(node._bandit_parent, ast.Compare):
        # looks for "candidate == 'some_string'"
        cut = substring_after(str(context), "str")[4:]
        import re
        CardNum = re.sub('[^A-Za-z0-9]+', '', cut)
        print(CardNum)

        comp = node._bandit_parent
        if isinstance(comp.left, ast.Name):
            if RE_CANDIDATE_CC.search(comp.left.id):
                if isinstance(comp.comparators[0], ast.Str):
                    if str(CardNum[:3]) == "000":
                        pass
                    else:
                        return _report(comp.comparators[0].s)

        elif isinstance(comp.left, ast.Attribute):
            if RE_CANDIDATE_CC.search(comp.left.attr):
                if isinstance(comp.comparators[0], ast.Str):
                    if str(CardNum[:3]) == "000":
                        pass
                    else:
                        return _report(comp.comparators[0].s)

        reports.append(_report(CardNum, CardNum))

    for o in range(len(reports)):
        return reports[o]
