import re

class DateUtil:
    @staticmethod
    def extract_date_from_filename(filename):
        """从文件名提取[YYYY-MM]格式的日期"""
        pattern = r'^\[(\d{4})-(\d{1,2})\]'
        match = re.match(pattern, filename)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            return year, month
        return None

    @staticmethod
    def format_jellyfin_date(year, month):
        """格式化为Jellyfin API需要的ISO 8601格式"""
        return f"{year}-{month:02d}-01T00:00:00.0000000"