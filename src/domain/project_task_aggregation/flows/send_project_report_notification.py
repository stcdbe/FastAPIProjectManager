from src.domain.project.entities import ProjectReportData
from src.infra.notifications.smtp import SMTPNotificationClient
from src.services.project_task_aggregation_service import ProjectTaskAggregationService


class SendProjectReportNotificationFlow:
    def __init__(
        self,
        notification_client: SMTPNotificationClient,
        project_task_aggregation_service: ProjectTaskAggregationService,
    ) -> None:
        self._notification_client = notification_client
        self._project_task_aggregation_service = project_task_aggregation_service

    async def execute(self, project_report_data: ProjectReportData) -> None:
        aggregation = await self._project_task_aggregation_service.get_one_project_with_tasks_by_guid(
            project_report_data.project_guid,
        )
        await self._notification_client.send_notification(
            recipient_email=project_report_data.email,
            subject=f"Project {aggregation.project.guid} report",
            template_name="project_report_email.html",
            project=aggregation.project,
            tasks=aggregation.tasks,
        )
