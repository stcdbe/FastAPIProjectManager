from src.domain.project.entities import ProjectReportData


class SendProjectAsReportUseCase:
    async def execute(self, send_data: ProjectReportData) -> None: ...
