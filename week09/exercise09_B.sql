{
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "application/vnd.databricks.v1+cell": {
          "cellMetadata": {
            "byteLimit": 26214400,
            "rowLimit": 1000
          },
          "inputWidgets": {},
          "nuid": "027d8b95-8d9a-46c2-b997-d70da7def576",
          "showTitle": false,
          "tableResultSettingsMap": {},
          "title": ""
        },
        "language": "sql",
        "resultVariableName": "dataframe_1"
      },
      "source": "%%sql -r dataframe_1\ndrop temp table if exists patients;\ncreate temporary table patients (\n    patients_id int, \n    name varchar(255), \n    birth_year int \n);\ninsert into patients values (1, 'John', 1980), (2, 'Mary', 1975), (3, 'Sam', 1990);\n\ndrop temp table if exists visits; \ncreate temporary table visits (\n  visit_id int, \n  patient_id int, \n  visit_date date, \n  provider_id int\n);\ninsert into visits values (2001, 1, '2024-02-01', 10);\ninsert into visits values (2002, 2, '2024-02-03', 11);\n\ndrop temp table if exists providers; \ncreate temporary table providers (\n  provider_id int, \n  provider_name varchar(255),\n  speciality varchar(255)\n);\ninsert into providers values (10, 'Dr. Smith', \"cardiolgy\");\ninsert into providers values (11, 'Dr. Lee', 'primary care');\ninsert into providers values (11, 'Dr. Patel', 'oncology'); \n\n-- q1: show each visit with patient and provider details \nselect patients.name, providers.provider_name, visits.visit_date\nfrom  patients \n      join visits on patients.patients_id = visits.patient_id\n      join providers on visits.provider_id = providers.provider_id;\n\n-- q2: show all providers and any visistes they had: parient name visit id \nselect patients.name, visits.visit_id \nfrom  patients \n      join visits on patients.patients_id = visits.patient_id;\n\n-- q3: show all providers and any visits they had: provider name, visit id \nselect providers.provider_name, visits.visit_id \nfrom  providers \n      join visits on providers.provider_id = visits.provider_id;\n\n-- q4: find all patients who never had a visit \nselect  patients.name \nfrom    patients \nwhere   patients.patients_id not in (select patient_id from visits);\n\n-- q5: show visists handled by cardiology providers \nselect  patients.name, provider_name, visit_date \nfrom    patients \n        join visits on patients.patients_id = visits.patient_id\n        join providers on visits.provider_id = providers.provider_id\nwhere   providers.speciality = 'cardiolgy' ",
      "id": "884fe0b2-6e26-4e6b-a021-16493b946a13"
    }
  ],
  "metadata": {
    "application/vnd.databricks.v1+notebook": {
      "computePreferences": null,
      "dashboards": [],
      "environmentMetadata": null,
      "inputWidgetPreferences": null,
      "language": "sql",
      "notebookMetadata": {
        "sqlQueryOptions": {
          "applyAutoLimit": true,
          "catalog": "workspace",
          "schema": "default"
        }
      },
      "notebookName": "exercise09_B.sql.dbquery.ipynb",
      "widgets": {}
    },
    "language_info": {
      "name": "sql"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}