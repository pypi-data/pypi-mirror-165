from json import JSONDecodeError

import dagster._check as check
from dagster._serdes import deserialize_json_to_dagster_namedtuple


def filter_dagster_events_from_cli_logs(log_lines):
    """
    Filters the raw log lines from a dagster-cli invocation to return only the lines containing json.

     - Log lines don't necessarily come back in order
     - Something else might log JSON
     - Docker appears to silently split very long log lines -- this is undocumented behavior

     TODO: replace with reading event logs from the DB

    """
    check.list_param(log_lines, "log_lines", str)

    coalesced_lines = []
    buffer = []
    in_split_line = False
    for line in log_lines:
        line = line.strip()
        if not in_split_line and line.startswith("{"):
            if line.endswith("}"):
                coalesced_lines.append(line)
            else:
                buffer.append(line)
                in_split_line = True
        elif in_split_line:
            buffer.append(line)
            if line.endswith("}"):  # Note: hack, this may not have been the end of the full object
                coalesced_lines.append("".join(buffer))
                buffer = []
                in_split_line = False

    events = []
    for line in coalesced_lines:
        try:
            events.append(deserialize_json_to_dagster_namedtuple(line))
        except JSONDecodeError:
            pass
        except check.CheckError:
            pass

    return events
