#!/usr/bin/env python3
# Standard/external imports
from typing import *
import sqlite3
import dataclasses

# Module imports
from pyrsktools.readers import Reader
from pyrsktools.utils import semver2int, rsktime2datetime
from pyrsktools.datatypes import *


class RSKEPDesktopReader(Reader):
    TYPE: str = "EPdesktop"
    MIN_SUPPORTED_SEMVER: str = "1.13.4"
    MAX_SUPPORTED_SEMVER: str = "2.0.0"

    def calibrations(self: Reader) -> List[Calibration]:
        datatype, table = Calibration, "calibrations"

        # NOTE: below is a modified version of self._createDatatypesFromQuery()
        results = []
        datatypeFields: dict = {}
        commonFields: Set[str] = set()

        for row in self._query(table):
            if not datatypeFields:
                datatypeFields = {field.name: field.type for field in dataclasses.fields(datatype)}
                commonFields = set(row.keys()).intersection(datatypeFields.keys())

            fieldsDict = {
                field: row[field]
                if datatypeFields[field] != "datetime64"
                else rsktime2datetime(row[field])
                for field in commonFields
            }

            # In EPdesktop RSKs, there are a variable number of coefficient
            # columns in the calibrations table. The below grabs all that exist.
            # For dictionaries below, key is coefficient number and value are...coef value.
            for coefPrefix in ("c", "x", "n"):
                fieldsDict[coefPrefix] = {
                    int(field[1:]): np.nan
                    if row[field] is None
                    else (int(row[field]) if coefPrefix == "c" else float(row[field]))
                    for field in row.keys()
                    if field.startswith(coefPrefix) and field[1:].isnumeric()
                }

            instance = datatype(**fieldsDict)
            results.append(instance)

        return results
