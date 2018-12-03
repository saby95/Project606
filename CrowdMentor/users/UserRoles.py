from enum import Enum

class UserRoles(Enum):
    ADMIN = 'admin'
    TASK_UPDATER = 'task_updater'
    AUDITOR = 'auditor'
    NORMAL_WORKER = 'worker'
    MENTOR = 'mentor'
    VIRTUAL_WORKER = 'virtual_worker'