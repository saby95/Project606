from enum import Enum

class UserRoles(Enum):
    ADMIN = 'admin'
    TASK_UPDATER = 'task_updater'
    AUDITOR = 'auditor'
    WORKER = 'worker'
    MENTOR = 'mentor'