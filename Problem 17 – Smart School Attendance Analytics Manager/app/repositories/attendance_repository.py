from models.attendance import Attendance

import pandas as pd

from datetime import date


class AttendanceRepository:
    def __init__(
        self,
        csv_path: str
    ):
        self.csv_path = csv_path

        self.attendance_df = pd.read_csv(
            csv_path,
            dtype={'Student ID': str},
            parse_dates=['Attendance Date']
        )

    def add_attendance(
        self,
        student_id: str,
        attendance_date: date,
        attendance_status: str
    ) -> None:
        count_records = len(self.attendance_df)

        self.attendance_df.loc[count_records, [
            'Student ID',
            'Attendance Date',
            'Attendance Status'
        ]] = [
            student_id,
            pd.Timestamp(attendance_date),
            attendance_status
        ]

        self.attendance_df.to_csv(
            self.csv_path,
            index=False
        )

    def correct_attendance(
        self,
        student_id: str,
        attendance_date: date,
        new_status: str
    ) -> None:
        mask = (
            (self.attendance_df['Student ID'] == student_id) &
            (self.attendance_df['Attendance Date'] == pd.Timestamp(attendance_date))
        )

        self.attendance_df.loc[
            mask, 'Attendance Status'
        ] = new_status

        self.attendance_df.to_csv(
            self.csv_path,
            index=False
        )

    def delete_attendance_history(
        self,
        student_id: str
    ) -> None:
        self.attendance_df = self.attendance_df[
            self.attendance_df['Student ID'] != student_id
        ]

        self.attendance_df.to_csv(
            self.csv_path,
            index=False
        )

    def attendance_already_recorded(
        self,
        student_id: str,
        attendance_date: date
    ) -> bool:
        return (
            (
                (self.attendance_df['Student ID'] == student_id) &
                (self.attendance_df['Attendance Date'] == pd.Timestamp(attendance_date))
            ).any()
        )

    def get_all_attendance_records(self) -> list[Attendance]:
        return [
            Attendance(
                row['Student ID'],
                row['Attendance Date'].date(),
                row['Attendance Status']
            )

            for _, row in self.attendance_df.iterrows()
        ]