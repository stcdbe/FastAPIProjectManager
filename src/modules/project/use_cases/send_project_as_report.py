from src.modules.project.entities.project import ProjectReportSendData
from src.modules.project.services.project_service import ProjectService


class SendProjectAsReportUseCase:
    def __init__(self) -> None:
        self._project_service = ProjectService()

    async def execute(self, send_data: ProjectReportSendData) -> None:
        await self._project_service.get_one_by_guid(send_data.project_guid)
