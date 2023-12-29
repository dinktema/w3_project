from typing import Union


def find_record_in_table(table: [dict], expected: dict) -> Union[dict, list]:
    output_records = []
    for key, value in expected.items():  # so, you can use several expected conditions
        for record in table:
            if record[key] == value:
                output_records.append(record)
    assert output_records, "There is no target record"
    return output_records


def check_errors(table: Union[list, str]):
    if type(table) == str:
        raise Exception(table)
