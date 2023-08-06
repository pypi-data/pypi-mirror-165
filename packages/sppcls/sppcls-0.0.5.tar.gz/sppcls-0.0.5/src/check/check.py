from argparse import ArgumentParser
import csv


def read_tokens(token_file_path, has_header=True):
    result = []

    with open(token_file_path, 'r', encoding='utf-8') as token_file:
        reader = csv.reader(token_file, delimiter='\t')

        if has_header:
            next(reader, None)

        for row in reader:
            if len(row) == 1:
                result.append(row[0])
            else:
                result.append(row)

    return result


def check_for_issues(org_tokens, project_tokens, column_count):

    if len(org_tokens) != len(project_tokens):
        raise Exception("Token lists differ in length")

    for line, (org_token, project_token) in enumerate(zip(org_tokens, project_tokens)):
        if isinstance(org_token, str):
            if not isinstance(project_token, str):
                raise Exception(f"Tokens don't match (near line {line + 1})")

            continue

        if len(project_token) != column_count:
            raise Exception(f"Incorrect column count (near line {line + 1})")

        for i in range(0, len(org_token)):
            if org_token[i] != project_token[i]:
                raise Exception(f"Tokens don't match (near line {line + 1}, position {i})")


def main():
    argument_parser = ArgumentParser()

    argument_parser.add_argument("org_tokens_file_path", metavar="org-tokens-file-path",
                                 help="Path to the original tokens tsv file")
    argument_parser.add_argument("project_tokens_file_path", metavar="project-tokens-file-path",
                                 help="Path to the project tokens tsv file")
    argument_parser.add_argument("column_count", metavar="column-count", help="Expected number of columns", type=int)

    args = argument_parser.parse_args()

    org_tokens_file_path = args.org_tokens_file_path
    project_tokens_file_path = args.project_tokens_file_path
    column_count = args.column_count

    org_tokens = read_tokens(org_tokens_file_path, False)
    project_tokens = read_tokens(project_tokens_file_path)

    check_for_issues(org_tokens, project_tokens, column_count)

    print("No issues found")


if __name__ == '__main__':
    main()
