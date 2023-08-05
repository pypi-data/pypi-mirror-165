from glob import glob
from tads.actors.documents import DocumentProcessor, handle_data_file

import numpy as np


class App(object):
    payroll_kwargs: dict = dict(
        coi=dict(chargeTips="E Charge Tips Amount", regularHours="E Regular Hours", overtimeHours="E Overtime Hours"),
        pattern="*Payroll*.xl*"
    )
    time_kwargs: dict = dict(
        cols=["name", "minorJob", "regularMinutes", "overtimeMinutes"],
        pattern="EmployeeTimesheet_*",
        query="CostAnalysisDataset_GenerateCostAnalysisReport_LabourCosts"
    )
    tip_kwargs: dict = dict(
        cols=["firstName", "lastName", "chargeTips"],
        pattern="ServerTipDeclarations_*",
        query="ServerTipDeclarationDataSet_GenerateTipDeclaration"
    )

    def __init__(self, folder):
        self.folder: str = folder

    def combine(self):
        return self.timesheets().merge(right=self.tipsheets(), left_on=["name"], right_on=["name"], how="left")

    def payroll(self):
        reduced = self.combine()
        df = [handle_data_file(i) for i in glob(f"{self.folder}/{self.payroll_kwargs['pattern']}")][0]
        df = df.join(reduced.set_index(["name", "minorJob"]), on=["Name", "Default Job"])
        for k, c in self.payroll_kwargs['coi'].items():
            df[c] = df[k]
        df.drop(self.payroll_kwargs['coi'].keys(), axis=1, inplace=True)
        df.replace(np.nan, 0.0, inplace=True)
        df.drop_duplicates(["Name", "Default Job"], keep='first', inplace=False, ignore_index=False)
        df = df.round(2)
        return df

    def timesheets(self):
        timedoc = DocumentProcessor(
            actions={i: "sum" for i in ["regularMinutes", "overtimeMinutes"]},
            cols=["name", "minorJob", "regularMinutes", "overtimeMinutes"],
            groups=["minorJob", "name"],
            pattern=f"{self.folder}/{self.time_kwargs['pattern']}",
            query=self.time_kwargs["query"]
        )
        timedoc.clean()
        timedoc.df.name = timedoc.df.name.str.title()
        timedoc.divide([f"{i}Minutes" for i in ["regular", "overtime"]], 60.0)
        timedoc.rename({f"{i}Minutes": f"{i}Hours" for i in ["regular", "overtime"]})
        return timedoc.df

    def tipsheets(self):
        tipdoc = DocumentProcessor(
            cols=self.tip_kwargs["cols"],
            pattern=f"{self.folder}/{self.tip_kwargs['pattern']}",
            query=self.tip_kwargs['query']
        )
        tipdoc.clean()
        tipdoc.df["name"] = tipdoc.df["firstName"].str.title() + " " + tipdoc.df["lastName"].str.title()
        tipdoc.df.drop(["firstName", "lastName"], axis=1, inplace=True)
        return tipdoc.df
