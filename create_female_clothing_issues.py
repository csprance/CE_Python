# bulk create issues for female character
import os
import csv

clothing_dict = {}


def write_header(writer):
    header = [
        "Summary",
        "Assignee",
        "Reporter",
        "Issue Type",
        "Description",
        "Priority",
    ]
    # write the header
    writer.writerow(header)


def put_item_in_dict(item):
    if clothing_dict.has_key(item[1]):
        clothing_dict[item[1]]["items"].append(item[0])
    else:
        clothing_dict[item[1]] = {"items": [item[0]]}


def convert_to_female(model_geo):
    if model_geo.endswith(".skin"):
        return model_geo.replace(".skin", "_female.skin")
    else:
        return model_geo.replace(".cgf", "_female.cgf")


def create_jira_issue(model_geo, item_names, writer):
    summary = "Female Clothing - %s" % model_geo
    assignee = "Unassigned"
    reporter = "Chris Sprance"
    issue_type = ""
    description = (
        "Skin the model %s to the female model it's final name should be %s The items it effects are: %s"
        % (model_geo, convert_to_female(model_geo), "\n".join(item_names))
    )
    priority = "High"
    writer.writerow([summary, assignee, reporter, issue_type, description, priority])


def main():
    with open("jira_female_issues.csv", "wb+") as female_issues_csv:
        writer = csv.writer(
            female_issues_csv, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        write_header(writer)
        # loop through all items
        with open("female_clothing.csv", "r") as csv_file:
            items = csv.reader(csv_file, delimiter=",", quotechar='"')
            for item in items:
                put_item_in_dict(item)
            for itm in clothing_dict:
                create_jira_issue(itm, clothing_dict[itm]["items"], writer)
            print(len(clothing_dict))


if __name__ == "__main__":
    main()
