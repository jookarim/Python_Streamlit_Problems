from repositories.attendance_repository import AttendanceRepository
from models.attendance import Attendance 
from exceptions.products_exceptions import NoProductsException

class AttendanceExplorer:
    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository 
    
    def get_first_record(self) -> Attendance:
        if not len(self.attendance_repository.get_all_records()):
            raise NoProductsException("No products to get the first product")
        
        return self.attendance_repository.get_all_records()[0]
    
    def get_last_record(self) -> Attendance:
        if not len(self.attendance_repository.get_all_records()):
            raise NoProductsException("No products to get the last product")
                
        return self.attendance_repository.get_all_records()[-1]

    def get_last_5(self) -> Attendance:
        count_records = len(self.attendance_repository.get_all_records())
        
        if not count_records:
            raise NoProductsException("No products to get the last product")
        
        if count_records < 5:
            return self.attendance_repository.get_all_records()[-count_records: ]
        
        return self.attendance_repository[-5: ] 
    