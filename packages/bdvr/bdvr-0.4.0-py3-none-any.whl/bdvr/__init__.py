__version__ = "0.4.0"
import os
from os import listdir
from os.path import isfile, join, exists
from turtle import color
import pandas
import argparse
import shutil
from pathlib import Path
import sys
from quo import echo
from startfile import startfile


def main():

    print = echo

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        help="Blackduck report folder is ex: D:\BD_REPORT\PROJECT_DATETIMESTAMP.zip",
        required=True,
    )
    parser.add_argument(
        "-o", action="store_true", help="(Optional) To automatically open the file"
    )

    args = parser.parse_args()
    bdreportszip = args.p
    open_file = args.o
    print(f"{bdreportszip=}", fg="vcyan")

    help_text = 'Go to Your Blackduck Project > Generate "Create Version detail report" > checkboxes "Source" and "Vulnerabilities" should be checked and Generate the report.'

    if not exists(bdreportszip):
        print("File not exists", bdreportszip, fg="red")
        sys.exit()
    if not isfile(bdreportszip):
        print(
            "Its a directory. Please give a zip file output of blackduck",
            bdreportszip,
            err=True,
        )
        print(help_text, fg="red")
        sys.exit()
    if ".zip" not in bdreportszip:
        print("Its not a zip file", bdreportszip, fg="red")
        sys.exit()
    this_dir = os.path.abspath(bdreportszip)
    filelocation = ""

    if "\\" in bdreportszip or "/" in bdreportszip:
        filelocation = (
            bdreportszip.rsplit("\\", 1)[0]
            if len(bdreportszip.rsplit("\\", 1)[0]) > 0
            else bdreportszip.rsplit("/", 1)[0]
        )
        filename = (
            bdreportszip.rsplit("\\", 1)[1]
            if len(bdreportszip.rsplit("\\", 1)[1]) > 0
            else bdreportszip.rsplit("/", 1)[1]
        )
    else:
        filelocation = this_dir.__str__()
        filename = bdreportszip

    filename = filename.replace(".zip", "")
    shutil.unpack_archive(bdreportszip, filelocation)

    mypath = filelocation + os.path.sep + filename

    print(f"{filelocation=}", fg="vgreen")
    print(f"{filename=}", fg="vgreen")
    print(f"{mypath=}", fg="vgreen")

    exit
    os.chdir(mypath)

    files_list = listdir(mypath)

    isSourcereportPresent = any(f for f in files_list if "source_" in f and ".csv" in f)
    isSecurityreportPresent = any(
        f for f in files_list if "security_" in f and ".csv" in f
    )
    print("Checking files source_ amd security_ prefix are present..", fg="vyellow")
    if isSourcereportPresent and isSecurityreportPresent:
        print("File with source_ amd security_ prefix are present", fg="vgreen")
    else:
        print(
            "File with either of source_ amd security_ prefix are not present", fg="red"
        )
        print(help_text)
        sys.exit()

    onlyfile1 = [
        f
        for f in listdir(mypath)
        if (
            isfile(join(mypath, f))
            and "source_" in join(mypath, f)
            and join(mypath, f).endswith(".csv")
        )
    ]
    onlyfile2 = [
        f
        for f in listdir(mypath)
        if (
            isfile(join(mypath, f))
            and "security_" in join(mypath, f)
            and join(mypath, f).endswith(".csv")
        )
    ]
    csv_f = filename + "-vulnerabilities.csv"
    xlsx_f = filename + "-vulnerabilities.xlsx"
    print(onlyfile1, fg="vgreen")
    print(onlyfile2, fg="vgreen")

    df1 = pandas.read_csv(onlyfile1[0])
    df2 = pandas.read_csv(onlyfile2[0])

    df = pandas.merge(
        df1, df2, how="inner", on=["Component id", "Version id", "Origin id"]
    )
    columns = [
        "Component id",
        "Version id",
        "Origin id",
        "Component origin version name_x",
        "Match content",
        "Usage",
        "Adjusted",
        "Component policy status",
        "Overridden By",
        "Origin name",
        "Origin name id",
        "Snippet Review status",
        "Scan",
        "Path",
        "Used by",
        "Component name_y",
        "Component version name_y",
        "Component origin name",
        "Component origin id",
        "Component origin version name_y",
        "Remediation status",
        "Remediation target date",
        "Remediation actual date",
        "Remediation comment",
        "URL",
        "Project path",
        "Overall score",
        "CWE Ids",
        "Reachable",
    ]
    df.drop(columns, inplace=True, axis=1)
    df = df[
        [
            "Component name_x",
            "Component version name_x",
            "Match type_x",
            "Match type_y",
            "Archive Context and Path",
            "Archive context",
            "Vulnerability id",
            "Security Risk",
            "Description",
            "Published on",
            "Updated on",
            "Base score",
            "Exploitability",
            "Impact",
            "Vulnerability source",
            "Solution available",
            "Workaround available",
            "Exploit available",
            "CVSS Version",
        ]
    ]

    def highlight_risk(row):
        if row["Security Risk"] == "HIGH":
            return ["background-color: red"] * len(row)
        elif row["Security Risk"] == "MEDIUM":
            return ["background-color: yellow"] * len(row)
        else:
            return ["background-color: white"] * len(row)

    df = df.style.apply(highlight_risk, axis=1)
    df.to_excel(xlsx_f)

    if not exists(xlsx_f):
        print("Output Excel File Not there", fg="red")
        sys.exit()
    output_file = join(mypath, xlsx_f)
    print("Check the output in: " + output_file, fg="vmagenta")

    if open_file:
        startfile(output_file)


if __name__ == "__main__":
    main()
