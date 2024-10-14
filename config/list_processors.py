from typing import Iterator, MutableSequence, Optional, Sequence, Tuple
import google.cloud.documentai_v1 as docai
from tabulate import tabulate
from config.processors import get_client_and_parent

def list_processors() -> MutableSequence[docai.Processor]:
    client, parent = get_client_and_parent()
    response = client.list_processors(parent=parent)
    return list(response.processors)

def print_processors(processors: Optional[Sequence[docai.Processor]] = None):
    def sort_key(processor):
        return processor.display_name

    if processors is None:
        processors = list_processors()
    sorted_processors = sorted(processors, key=sort_key)
    data = processor_tabular_data(sorted_processors)
    headers = next(data)
    colalign = next(data)

    print(tabulate(data, headers, tablefmt="pretty", colalign=colalign))
    print(f"→ Processors: {len(sorted_processors)}")

def processor_tabular_data(
    processors: Sequence[docai.Processor],
) -> Iterator[Tuple[str, str, str]]:
    yield ("display_name", "type", "state")
    yield ("left", "left", "left")
    if not processors:
        yield ("-", "-", "-")
        return
    for processor in processors:
        yield (processor.display_name, processor.type_, processor.state.name)

def get_processor(
    display_name: str,
    processors: Optional[Sequence[docai.Processor]] = None,
) -> Optional[docai.Processor]:
    if processors is None:
        processors = list_processors()
    for processor in processors:
        if processor.display_name == display_name:
            return processor
    return None
