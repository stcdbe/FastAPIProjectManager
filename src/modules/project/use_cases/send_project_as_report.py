from src.modules.project.entities.project import ProjectReportSendData


class SendProjectAsReportUseCase:
    async def execute(self, send_data: ProjectReportSendData) -> None: ...
