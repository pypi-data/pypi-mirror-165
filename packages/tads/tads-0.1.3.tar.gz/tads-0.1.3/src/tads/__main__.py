import os.path

from tads.core import App


def run():
    app = App(".artifacts/files")
    df = app.payroll()
    print(df)
    if input("Would you like to save this to a new csv file? [y/n]:\t").lower() == "y":
        save_as = input("Filename:\t")
        df.to_csv(os.path.expanduser("~/Desktop/{}.csv".format(save_as)))


run()
