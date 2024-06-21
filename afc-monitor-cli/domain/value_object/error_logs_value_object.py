from typing import List


class ErrorLogsOverallValueObject():
    def __init__(self, total_pattern_count: int, total_logs_count: int) -> None:
        self.total_pattern_count = total_pattern_count
        self.total_logs_count = total_logs_count


class ErrorLogsPatternCountValueObject():
    def __init__(self, pattern: str, service: str, count: int) -> None:
        self.pattern = pattern
        self.service = service
        self.count = count


class ErrorLogsServiceCountValueObject():
    def __init__(self, service: str, count: int) -> None:
        self.service = service
        self.count = count


class ErrorLogsValueObject():
    def __init__(self, error_logs_overall: ErrorLogsOverallValueObject, error_logs_pattern_counts: List[ErrorLogsPatternCountValueObject], error_logs_service_counts: List[ErrorLogsServiceCountValueObject]):
        self.error_logs_overall = error_logs_overall
        self.error_logs_pattern_counts = error_logs_pattern_counts
        self.error_logs_service_counts = error_logs_service_counts
