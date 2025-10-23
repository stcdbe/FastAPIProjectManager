from src.domain.project.entities.project import ProjectReportSendData


class SendProjectAsReportUseCase:
    def __init__(self) -> None: ...

    async def execute(self, send_data: ProjectReportSendData) -> None: ...
