from typing import Iterator, MutableSequence, Sequence, Tuple
import google.cloud.documentai_v1 as docai
from tabulate import tabulate
from config.processors import get_client_and_parent

def fetch_processor_types() -> MutableSequence[docai.ProcessorType]:
    client, parent = get_client_and_parent()
    response = client.fetch_processor_types(parent=parent)
    return response.processor_types

def print_processor_types(processor_types: Sequence[docai.ProcessorType]):
    def sort_key(pt):
        return (not pt.allow_creation, pt.category, pt.type_)

    sorted_processor_types = sorted(processor_types, key=sort_key)
    data = processor_type_tabular_data(sorted_processor_types)
    headers = next(data)
    colalign = next(data)

    print(tabulate(data, headers, tablefmt="pretty", colalign=colalign))
    print(f"→ Processor types: {len(sorted_processor_types)}")

def processor_type_tabular_data(
    processor_types: Sequence[docai.ProcessorType],
) -> Iterator[Tuple[str, str, str, str]]:
    def locations(pt):
        return ", ".join(sorted(loc.location_id for loc in pt.available_locations))

    yield ("type", "category", "allow_creation", "locations")
    yield ("left", "left", "left", "left")
    if not processor_types:
        yield ("-", "-", "-", "-")
        return
    for pt in processor_types:
        yield (pt.type_, pt.category, f"{pt.allow_creation}", locations(pt))
