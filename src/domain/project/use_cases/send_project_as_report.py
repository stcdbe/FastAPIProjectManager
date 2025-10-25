from src.domain.project.entities.project import ProjectReportSendData


class SendProjectAsReportUseCase:
    __slots__ = ()

    def __init__(self) -> None: ...

    async def execute(self, send_data: ProjectReportSendData) -> None: ...
